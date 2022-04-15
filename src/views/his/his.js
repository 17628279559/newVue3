import * as d3 from 'd3'


let settings = {
  margin: { top: 50, left: 50, bottom: 80, right: 50 },
  width: 1300,
  height: 500,
  xAxisLabel: 'x轴',
  yAxisLabel: 'y轴',
  colors: d3.scaleLinear().domain([0, 15]).range(['#FF0000', '#6284FF'])
}




const his = (id, svgRef1, res_data, options, update = false) => {

  //更新settings
  if (update) {
    const data = res_data.data,
      time = res_data.time,
      innerwidth = settings.width - settings.margin.left - settings.margin.right,
      innerheight = settings.height - settings.margin.top - settings.margin.bottom;

    let xScale = d3.scaleBand().domain(data.map((item) => item.id + item.name)).range([0, innerwidth]).padding(0.2)
    let yScale = d3.scaleLinear().domain([d3.max(data, (item) => Math.floor(Math.sqrt(item.value))), 0]).range([0, innerheight])
    let xAxis = d3.axisBottom(xScale).tickSize(0)
    let yAxis = d3.axisLeft(yScale).tickSize(0)  // 数据排名可能发生变化,更新xy轴比例尺
    let canvas = d3.select(svgRef1.value).select('#maingroup')
    canvas.select('#xx')
      .transition()
      .duration(500)
      .call(xAxis)
      .selectAll("text")
      .attr('text-anchor', 'start')
      .attr('transform', 'rotate(30 -10 10)');
    canvas.select('#yy').transition().duration(500).call(yAxis)

    canvas
      .selectAll('.dataRect')
      .data(data, (item) => item.id)
      .transition()
      .duration(500)
      .attr('fill', (item) => settings.colors(item.id))
      .attr(
        'height',
        (item) => innerheight - yScale(Math.floor(Math.sqrt(item.value)))
      )

    canvas
      .selectAll('.value')
      .data(data, (item) => item.id)
      .text((item) => item.value)
      .transition()
      .duration(500)
      .attr('y', (item) => yScale(Math.floor(Math.sqrt(item.value))))
    d3.selectAll('.tick').attr('font-size', '1.3em')
    canvas.select('#time').transition().duration(500).text(time)
  }
  else {
    for (let parameter in options)
      settings[parameter] = options[parameter];

    let data = res_data.data,
      time = res_data.time

    if (!data) {
      data = res_data
    }
    const innerwidth = settings.width - settings.margin.left - settings.margin.right,
      innerheight = settings.height - settings.margin.top - settings.margin.bottom;

    let svg = d3.select(svgRef1.value)

    let canvas = svg
      .append('g')
      .attr('id', 'maingroup')
      .attr('transform', `translate(${settings.margin.left},${settings.margin.top})`)


    let xScale = d3.scaleBand().domain(data.map((item) => item.id + item.name)).range([0, innerwidth]).padding(0.2)
    let yScale = d3.scaleLinear().domain([d3.max(data, (item) => Math.floor(Math.sqrt(item.value))), 0]).range([0, innerheight])
    let xAxis = d3.axisBottom(xScale).tickSize(0)
    let yAxis = d3.axisLeft(yScale).tickSize(0)

    // 使用比例尺画x轴
    let xAxisGroup = canvas
      .append('g')
      .call(xAxis)
      .attr('id', 'xx')
      .attr('transform', `translate(0,${innerheight})`)

    xAxisGroup.selectAll("text")
      .attr('text-anchor', 'start')
      .attr('transform', 'rotate(30 -10 10)');
    // 添加x轴信息


    // 使用比例尺画y轴
    let yAxisGroup = canvas.append('g').attr('id', 'yy').call(yAxis)
    // 添加y轴信息
    yAxisGroup
      .append('text')
      .attr('font-size', '1.5em')
      .attr('transform', `rotate(-90)`)
      .attr('x', -innerheight / 2)
      .attr('y', -30)
      .text(settings.yAxisLabel)
      .attr('text-anchor', 'middle')

    // 调整 x轴y轴字体大小
    d3.selectAll('.tick').attr('font-size', '1.3em')

    canvas
      .selectAll('.dataRect')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'dataRect')
      .attr('id', (item) => `_${id}_rect_${item.id}`)
      .attr('width', xScale.bandwidth())
      .attr('fill', (item) => settings.colors(item.id))
      .attr('opacity', 0.8)
      .attr('x', (item) => xScale(item.id + item.name))
      .attr('y', -innerheight)
      .attr('transform', 'scale(1, -1)')
      .on('mouseover', (item, index) => {
        d3.select(`#_${id}_rect_${index.id}`)
          .attr('fill-opacity', 0.5)
        $('#his_message').css({ display: 'block' })
        $('#music_title').text(index.name)
        if (index.pubdate) {
          $('#music_com').text(`评论数: ${index.value}`)
          $('#music_pubdate').text(`发布时间:${index.pubdate}`)
          $('#music_desc').text(index.descrip)
        }
        else {
          $('#music_com').text(`${index.desc}: ${index.value}`)
          $('#music_pubdate').text("")
          $('#music_desc').text("")
        }

      })
      .on('mouseout', (item, index) => {
        d3.select(`#_${id}_rect_${index.id}`)
          .attr('fill-opacity', 1)
        $('#his_message').css({ display: 'none' })
      })
      .on('mousemove', (ev) => {
        $('#his_message').css({ left: ev.clientX + 5 + 'px', top: (ev.clientY - 40.4) + 'px' })
      })
      .transition()
      .duration(500)
      .attr(
        'height',
        (item) => innerheight - yScale(Math.floor(Math.sqrt(item.value)))
      )

    // 添加数值
    canvas
      .selectAll('.value')
      .data(data)
      .enter()
      .append('text')
      .attr('class', 'value')
      .text((item) => item.value)
      .attr('x', (item) => xScale(item.id + item.name))
      .attr('y', (item) => yScale(Math.floor(Math.sqrt(item.value))))
      .attr('font-size', '1em')
      .attr('dx', xScale.bandwidth() / 2)
      .attr('text-anchor', 'middle')

    // 添加学号信息

    // 添加日期
    if (time) {
      canvas
        .append('text')
        .attr('id', 'time')
        .text(time)
        .attr('font-size', '1.5em')
        .attr('transform', `translate(0,-25)`)
    }



    canvas.selectAll('text').attr('fill', '#F5F5F5')
    canvas.selectAll('line').attr('fill', '#F5F5F5')

  }
}
export default his;