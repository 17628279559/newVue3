<script setup>
import { ref, onMounted } from 'vue';
import * as d3 from 'd3';
import Axios from 'axios';

const getdataApi = "/api/getdata"
const switchApi = "/api/switch"
const svgRef = ref(null);
const margin = { top: 100, left: 100, bottom: 100, right: 100 };
const width = document.documentElement.clientWidth - 16.8;
const height = document.documentElement.clientHeight - 32 - 16.8;
const ratio = 1;
const innerwidth = width - margin.left - margin.right;
const innerheight = height - margin.top - margin.bottom;
const xAxisLabel = '网易云实时飙升榜榜单';
const yAxisLabel = '根号下评论数';
let colors;
let time;
let data = [];
let xScale, yScale;
let xAxis, yAxis;
let yAxisGroup, xAxisGroup;
let min, max;
let canvas;
let svg;
let status = ref("切换随机数据");

const switch_use_fake = () => {
  Axios.get(switchApi).then(response => {
    console.log(response.data.data.use_fake);
    if (response.data.data.use_fake) {
      status.value = "切换真实数据";
    } else {
      status.value = "切换随机数据"
    }
  })

}

const scale = () => {
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
}

const update = (response) => {
  data = response.data.data;
  time = response.data.time;
  max = d3.max(data, item => Math.floor(Math.sqrt(item.value)));

  scale(); // 数据排名可能发生变化,更新xy轴比例尺

  canvas.select("#xx")
    .transition()
    .duration(500)
    .call(xAxis)
  canvas.select("#yy")
    .transition()
    .duration(500)
    .call(yAxis)


  canvas.selectAll('.dataRect')
    .data(data, item => item.id)
    .transition()
    .duration(500)
    .attr('fill', item => colors(item.id))
    .attr('height', item => innerheight - yScale(Math.floor(Math.sqrt(item.value))));

  canvas.selectAll('.value')
    .data(data, item => item.id)
    .text(item => item.value)
    .transition()
    .duration(500)
    .attr('y', item => yScale(Math.floor(Math.sqrt(item.value))))

  canvas.select("#time")
    .transition()
    .duration(500)
    .text(time)
}


onMounted(() => {

  Axios.get(getdataApi).then(response => {
    data = response.data.data;
    time = response.data.time;

    min = 0;
    max = d3.max(data, item => Math.floor(Math.sqrt(item.value)));
    svg = d3.select(svgRef.value);

    canvas = svg.append('g')
      .attr('id', 'maingroup')
      .attr('transform', `translate(${margin.left},${margin.top})`)


    scale();

    // 使用比例尺画x轴
    xAxisGroup = canvas.append('g')
      .call(xAxis)
      .attr('id', 'xx')
      .attr('transform', `translate(0,${innerheight})`)
    // 添加x轴信息
    xAxisGroup.append('text')
      .attr('font-size', `${3 * ratio}em`)
      .attr('y', 50 * ratio)
      .attr('x', innerwidth / 2)
      .attr('fill', '#333333')
      .text(xAxisLabel);

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
      .text(yAxisLabel)
      .attr('text-anchor', 'middle')

    // 调整 x轴y轴字体大小
    d3.selectAll('.tick')
      .attr('font-size', `${1.3 * ratio}em`);

    //   data.forEach(item => {
    //     g.append('rect')
    //       .attr('height', innerheight - yScale(Math.floor(Math.sqrt(item.value))))
    //       .attr('width', xScale.bandwidth())
    //       .attr('fill', 'green')
    //       .attr('opacity', 0.8)
    //       .attr('x', xScale(item.name))
    //       .attr('y', yScale(Math.floor(Math.sqrt(item.value))))
    //   })

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
      .attr('font-size', `${1 * ratio}em`)
      .attr("dx", xScale.bandwidth() / 2)
      .attr('text-anchor', 'middle');


    // 添加学号信息
    canvas.append('text')
      .text('赵文韬-2019302120066')
      .attr('font-size', `${1.5 * ratio}em`)
      .attr('transform', `translate(${innerwidth / (1.1 * ratio)},${innerheight + margin.bottom / 2})`)
      .attr('text-anchor', 'middle');

    // 添加日期 
    canvas.append('text')
      .attr("id", "time")
      .text(time)
      .attr('font-size', `${1.5 * ratio}em`)
      .attr('transform', `translate(0,-25)`)

    // 每两秒更新一次
    window.setInterval(() => {
      setTimeout(() => {
        Axios.get(getdataApi).then(response => {
          update(response);
        })
      }, 1000);
    }, 1000);
  })

});

</script>

<template>
  <div id="all">
    <el-row class="mb-4 center">
      <el-button @click="switch_use_fake"
                 type="success"
                 plain>{{status}}</el-button>
    </el-row>
    <svg class="center"
         :width=width
         :height=height
         ref="svgRef">
    </svg>
  </div>

</template>

<style scoped>
#resizediv {
  padding: 0;
  border: 0;
  margin: 0, auto;
}
#all {
  width: 100%;
  height: 100%;
}
.center {
  display: block;
}
</style>
