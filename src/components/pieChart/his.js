import * as d3 from 'd3';

let his = (id, svgRef, data, options) => {
    const margin = { top: 60, left: 80, bottom: 120, right: 80 };
    const width = 1000;
    const height = 550;
    const ratio = 1;
    const innerwidth = width - margin.left - margin.right;
    const innerheight = height - margin.top - margin.bottom;
    let colors;
    let time;
    let xScale, yScale;
    let xAxis, yAxis, parameter;
    let yAxisGroup, xAxisGroup;
    let min, max;
    let canvas;
    let svg = d3.select(svgRef.value);

    let settings = {
        xAxisLabel: "每日疫情新增",
        yAxisLabel: "新增数量",
    };

    min = 0;
    max = d3.max(data, item => Math.floor(Math.sqrt(item.value)));

    for (parameter in options)
        settings[parameter] = options[parameter];

    colors = d3.scaleLinear()
        .domain([0, 15])
        .range(['#FF0000', '#6284FF'])
    xScale = d3.scaleBand()
        .domain(data.map(item => item.id + item.name))
        .range([0, innerwidth])
        .padding(0.2);
    yScale = d3.scaleLinear()
        .domain([max, min])
        .range([0, innerheight])
    yAxis = d3.axisLeft(yScale)
        .tickSize(0);
    xAxis = d3.axisBottom(xScale)
        .tickSize(0);




    canvas = svg.append('g')
        .attr('id', 'maingroup')
        .attr('transform', `translate(${margin.left},${margin.top})`)



    // 使用比例尺画x轴
    xAxisGroup = canvas.append('g')
        .call(xAxis)
        .attr('id', 'xx')
        .attr('transform', `translate(0,${innerheight})`)
        .selectAll("text")
        .attr('text-anchor', 'start')
        .attr('transform', 'rotate(45 -10 10)');



    // 使用比例尺画y轴
    yAxisGroup = canvas.append('g')
        .attr('id', 'yy')
        .call(yAxis)
    // 添加y轴信息
    yAxisGroup.append('text')
        .attr('font-size', `${1.5 * ratio}em`)
        .attr('transform', `rotate(-90)`)
        .attr('x', -innerheight / 2)
        .attr('y', -30 * ratio)
        .attr('fill', '#333333')
        .text(settings.yAxisLabel)
        .attr('text-anchor', 'middle')

    // 调整 x轴y轴字体大小
    d3.selectAll('.tick')
        .attr('font-size', `${1.1 * ratio}em`);

    // 使用enter添加矩形
    canvas.selectAll('.dataRect')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'dataRect')
        .attr('width', xScale.bandwidth())
        .attr('fill', item => colors(item.id))
        .attr('opacity', 0.8)
        .attr('x', item => xScale(item.id + item.name))
        .attr('y', -innerheight)
        .attr('transform', 'scale(1, -1)')
        .transition()
        .duration(500)
        .attr('height', item => innerheight - yScale(Math.floor(Math.sqrt(item.value))))


    // 添加数值
    canvas.selectAll('.value')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'value')
        .text(item => item.value)
        .attr('x', item => xScale(item.id + item.name))
        .attr('y', item => yScale(Math.floor(Math.sqrt(item.value))))
        .attr('font-size', `${0.8 * ratio}em`)
        .attr("dx", xScale.bandwidth() / 2)
        .attr('text-anchor', 'middle');


    // 添加学号信息
    canvas.append('text')
        .text(settings.xAxisLabel)
        .attr('font-size', `${1.5 * ratio}em`)
        .attr('transform', `translate(${innerwidth / 2},${innerheight + margin.bottom / 2})`)
        .attr('text-anchor', 'middle');

}

export default his;