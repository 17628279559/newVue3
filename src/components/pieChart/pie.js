import * as d3 from 'd3';
let const_color = ['#FFFF33', '#FFFF00', '#CCFF33', '#BBFF00', '#99FF33', '#77FF00', '#FF3333', '#FF0000', '#FF44AA', '#FF0088', '#33FF33', '#00FF00', '#33FFAA', '#00FF99', '#33FFDD', '#00FFCC', '#33FFFF', '#00FFFF', '#33CCFF', '#00BBFF', '#5599FF', '#0066FF', '#5555FF', '#0000FF', '#7744FF', '#5500FF', '#9955FF', '#7700FF', '#B94FFF', '#9900FF', '#E93EFF', '#CC00FF', '#FF3EFF', '#FF00FF']

Array.prototype.shuffle = function () {
    let array = this;
    let len = array.length;
    for (let i = len - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}


let pie = (id, svgRef, data, options) => {
    let svg = d3.select(svgRef.value);

    const_color.shuffle();

    let settings = {
        title: "",
        chart_height: 550,
        show_lable_text: true,
        raised: 20,
        chart_height: 550,
        text_anchor: "middle",
        pad_angle: 0,
        introduce_backguound_color: '#8EC5FC',
        is_rotate: false,
        stroke_width: 0,
        stroke: '#fff',
        radius_inner: 0,
        radius_outer: 220,
        radius_label: 240,
        use_const_color: true,
        label_margin: 10,
        group_data: 0,
        lable_text_size: "1.1em",
        gradient_color: ['#4158D0', '#C850C0', '#FFCC70', '#4158D0'],
        domain_gradient_color: [],
        name: item => item.name,
        get_value: item => item.value,
        color: (item, index) => colorScale(index)
    };

    // 更新settings
    for (parameter in options)
        settings[parameter] = options[parameter];


    const chart_size = d3.min([settings.chart_width, settings.chart_height]),
        PI = 3.1415926;

    if (settings.domain_gradient_color.length == 0) {
        for (let i = 0; i < settings.gradient_color.length; i++) {
            settings.domain_gradient_color.push(data.length * (i / (settings.gradient_color.length - 1)))
        }
    }

    let colorScale = d3.scaleLinear().domain(settings.domain_gradient_color).range(settings.gradient_color),
        donut, piee, parameter, scale, introduce_g,
        data_size = 0;


    data.forEach(e => {
        data_size += settings.get_value(e)
    });




    // 合并data中占比小于group_data的元素
    const group_data = data => {
        let removed_data_size = 0;

        for (let i = data.length - 1; i >= 0; i--) {
            if (settings.get_value(data[i]) === 0) {
                data.splice(i, 1);
            }
            else if ((settings.get_value(data[i]) / data_size) * 100 < settings.group_data) {
                removed_data_size += settings.get_value(data.splice(i, 1)[0]);
            }
        }


        if (removed_data_size > 0)
            data.push({ index: 35, name: 'Other', value: removed_data_size });
        return data;
    };


    data = group_data(data);


    let nowAngle = 0;
    for (let i = 0; i < data.length; i++) {
        data[i]['lableAngle'] = nowAngle + ((settings.get_value(data[i]) / data_size) * 100 / 100) * PI;
        nowAngle += ((settings.get_value(data[i]) / data_size) * 100 / 100) * PI * 2;
    }

    const text_over = item => {
        if (settings.is_rotate) {
            return `translate(0,5) rotate(${(item.lableAngle - PI / 2) * (180 / PI)}) translate(${settings.radius_label - 10 + settings.raised},0)`
        } else return `translate(${Math.sin(item.lableAngle) * (settings.radius_label + settings.raised)},${-(Math.cos(item.lableAngle) * (settings.radius_label + settings.raised))})`;
    };

    const text_out = item => {
        if (settings.is_rotate) {
            return `translate(0,5) rotate(${(item.lableAngle - PI / 2) * (180 / PI)}) translate(${settings.radius_label - 10},0)`
        } else return `translate(${Math.sin(item.lableAngle) * settings.radius_label},${-(Math.cos(item.lableAngle) * settings.radius_label) + 8})`
    };

    const over = (item, index) => {
        d3.select(`#_${id}_path${index.data.index}`)
            .transition()
            .duration(50)
            .attr('fill-opacity', 0.5)
            .attr('d', window.selectArc[`arc${id}`]);
        d3.select(`#_${id}_text${index.data.index}`)
            .transition()
            .duration(50)
            .text(index.data.value)
            .attr('transform', text_over);
        d3.select(`#_${id}_introduce${index.data.index}`)
            .transition()
            .duration(50)
            .style('fill', settings.introduce_backguound_color);
    };

    const out = (item, index) => {
        d3.select(`#_${id}_path${index.data.index}`)
            .transition()
            .duration(200)
            .attr('fill-opacity', 1)
            .attr('d', window.arc[`arc${id}`]);
        d3.select(`#_${id}_text${index.data.index}`)
            .transition()
            .duration(50)
            .text(index.data.name)
            .attr('transform', text_out);
        d3.select(`#_${id}_introduce${index.data.index}`)
            .transition()
            .duration(50)
            .style('fill', '#f5f5f5');
    };

    const introduce_rect_fillcolor = (item, index) => {
        if (settings.use_const_color)
            return const_color[item.index];
        else return settings.color(item.data, index);
    }

    donut = svg
        .append('g')
        .attr('class', 'donut')
        .attr('transform', `translate(${chart_size / 2},${chart_size / 2})`);

    introduce_g = svg
        .append('g')
        .attr('class', 'introduce_g')
        .attr('transform', `translate(${chart_size},20)`);

    window.arc[`arc${id}`] = d3.arc()
        .innerRadius(settings.radius_inner)
        .outerRadius(settings.radius_outer);

    window.selectArc[`arc${id}`] = d3.arc()
        .innerRadius(settings.radius_inner)
        .outerRadius(settings.radius_outer + settings.raised);

    piee = d3.pie()
        .value(settings.get_value)
        .padAngle(settings.pad_angle)
        .sort((a, b) => a.index - b.index)(data);


    donut.selectAll('path')
        .data(piee)
        .enter()
        .append('path')
        .attr('id', item => `_${id}_path${item.data.index}`)
        .style('fill', introduce_rect_fillcolor)
        .attr('d', window.arc[`arc${id}`])
        .attr('stroke-width', settings.stroke_width)
        .attr('stroke', settings.stroke)
        .on('mouseover', over)
        .on('mouseout', out);

    if (settings.show_lable_text) {
        donut.selectAll('text')
            .data(data)
            .enter()
            .append('text')
            .text(item => item.name)
            .attr('id', item => `_${id}_text${item.index}`)
            .attr('transform', text_out)
            .attr('font-size', settings.lable_text_size)
            .attr('text-anchor', settings.text_anchor)
            .attr('fill', 'rgb(90,90,90)');

        donut.append('text')
            .text(settings.title)
            .attr('transform', `translate(0,${settings.radius_label + 25})`)
            .attr('font-size', `1.3em`)
            .attr('text-anchor', 'middle');

        scale = d3.scaleLinear()
            .domain([0, 12])
            .range([0, 510])

        introduce_g.selectAll('.introduce')
            .data(piee)
            .enter()
            .append('rect')
            .attr('class', 'introduce')
            .attr('id', item => `_${id}_introduce${item.data.index}`)
            .attr('width', 100)
            .attr('height', 510 / 12)
            .attr('transform', item => `translate(${(item.index % 4) * 100},${scale(Math.floor(item.index / 4))})`)
            .style('fill', '#f5f5f5')
            .on('mouseover', over)
            .on('mouseout', out);



        introduce_g.selectAll('.introduce_rect')
            .data(piee)
            .enter()
            .append('rect')
            .attr('class', 'introduce_rect')
            .attr('width', 22)
            .attr('height', 22)
            .attr('transform', item => `translate(${(item.index % 4) * 100 + 10.25},${scale(Math.floor(item.index / 4)) + 10.25})`)
            .style('fill', introduce_rect_fillcolor)
            .on('mouseover', over)
            .on('mouseout', out);

        introduce_g.selectAll('.introduce_text')
            .data(piee)
            .enter()
            .append('text')
            .attr('class', 'introduce_text')
            .text(item => item.data.name)
            .attr('transform', item => `translate(${(item.index % 4) * 100 + 10.25 + 32},${scale(Math.floor(item.index / 4)) + 10.25 + 17})`)
            .attr('font-size', settings.lable_text_size)
            .on('mouseover', over)
            .on('mouseout', out);
    }
};

export default pie;