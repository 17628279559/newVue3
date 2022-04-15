<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue'
import { Check, FolderAdd } from '@element-plus/icons-vue'
import * as d3 from 'd3';
import cloud from 'd3-cloud'
import Axios from 'axios'
import { Eleme } from '@element-plus/icons-vue'

const getWordsApi = '/api/getwords'
const getPythonWords = '/api/getpythonwords'
const { proxy } = getCurrentInstance()
let layout = cloud()
const theSize = [1000, 540]
let theWordList = [
  { text: 'vue', size: 20 },
  { text: 'html', size: 25 },
  { text: 'js', size: 30 },
]

let textarea = ref("")
const theSvgElement = ref(null)
const pythonCy = ref(null)
const draw = (words) => {
  let color = d3.scaleOrdinal(d3.schemeCategory10);
  d3.select(theSvgElement.value)
    .append("svg")
    .attr("width", layout.size()[0])
    .attr("height", layout.size()[1])
    .append("g")
    .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
    .selectAll("text")
    .data(words)
    .enter().append("text")
    .style("font-size", function (d) { return d.size + "px"; })
    .style("font-family", "Impact")
    .style("cursor", "pointer")
    .style("fill", function (d, i) { return color(i); })
    .attr("text-anchor", "middle")
    .attr("transform", function (d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
    .text(function (d) { return d.text; })
    // 添加点击的回调方法
    .on("mouseover", (index, item) => {
      d3.select(index.target)
        .transition()
        .duration(100)
        .style('opacity', 0.7)
        .style('font-size', item.size + 20 + 'px')
    })
    .on("mouseout", (index, item) => {
      d3.select(index.target)
        .transition()
        .duration(100)
        .style('opacity', 1)
        .style('font-size', item.size + 'px')
    });
}


onMounted(() => {
  Axios.get(getWordsApi).then((response) => {
    theWordList = response.data
    console.log(theWordList)
    layout
      .size(theSize)
      .words(theWordList)
      .padding(5)
      .rotate(function () { return ~~(Math.random() * 3) * 30; })
      .font("Impact")
      .fontSize(function (d) { return d.size; })
      .on("end", draw);

    layout.start();
  })

  const img = "/api/static/1650027230.856627_demo.jpg"
  $(pythonCy.value).attr('src', img)
})

</script>

<template>
  <header-box :style="{'display':!proxy.$wordCloudPython.show ? 'block':'none'}" section_class="tile color transparent-black">
    <template v-slot:title>
      <h1><a style="color:#FFF" href="http://www.93.gov.cn/bsjs-ldcy-zxfzx-cbfzx-wdjh/768551.html" target="_blank"><strong>全国人大十三届五次全会精神文稿</strong></a>词云图</h1>
    </template>
    <template v-slot:content>
      <div ref="theSvgElement"></div>
    </template>
  </header-box>
  <header-box :style="{'display':proxy.$wordCloudPython.show ? 'block':'none'}" section_class="tile color transparent-black">
    <template v-slot:title>
      <h1>基于python wordCloud的词云图</h1>
    </template>
    <template v-slot:content>
      <el-input style="width:1200px;margin:20px" v-model="textarea" :autosize="{ minRows: 3, maxRows: 999 }" type="textarea" placeholder="请输入你想进行词云生成的文字（字数越多越好，建议400字以上）" />
      <div style="display:flex;justify-content:flex-end;margin:0px 30px">
        <el-button type="success" size="large" :icon="Check" circle />
        <el-button type="primary" size="large" :icon="FolderAdd" circle />
      </div>
      <img ref="pythonCy" style="width:1200px;height:700px;margin:20px" src="" />
    </template>
  </header-box>
</template>

<style scoped>
</style>