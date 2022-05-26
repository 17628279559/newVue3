<script setup>
import { onMounted, watch, getCurrentInstance } from "vue"
import * as d3 from 'd3'
import miserables from './data2.json'
import ForceGraph from './ForceGraph'
const { proxy } = getCurrentInstance()

const chart1 = ForceGraph(miserables, {
  nodeId: d => d.id,
  nodeGroup: d => d.group,
  nodeTitle: d => `${d.id}\n${d.group}`,
  width: 1000,
  height: 540,
})

watch(proxy.$force, (newValue, oldValue) => {
  if (newValue == 1) {
    d3.selectAll("circle")
      .style("fill", "url(#image)")
  } else {
    d3.selectAll("circle")
      .style("fill", item => `url(#catpattern_${item.id})`)
  }
})

onMounted(() => {
  $("#force").children().remove()
  $("#force").append(chart1)
})
</script>

<template>
  <div>
    <div id="force_message">
      <div class="message-header">
        <div id="force_name">这里是名字</div>
        <div class="linediv"></div>
        <div id="force_des">这里是介绍</div>
      </div>
    </div>
    <header-box section_class="tile color transparent-black">
      <template v-slot:title>
        <h1><a href="https://observablehq.com/@d3/force-directed-graph?collection=@d3/d3-force" target="_blank"><strong>人民的名义人物关系图</strong></a></h1>
      </template>
      <template v-slot:content>
        <div id="force">
        </div>
      </template>
    </header-box>
  </div>
</template>

<style scoped>
a {
  color: #fff;
}
.message-header {
  display: flex;
  flex-wrap: wrap;
  margin: 10px;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}
.linediv {
  border-bottom: 1px solid #666;
  width: 100%;
}
#force_message {
  display: flex;
  width: 200px;
  height: auto;
  position: absolute !important;
  background-color: rgba(255, 255, 255, 0.7);
  color: #222;
  border-radius: 8px !important;
  box-shadow: 0 3px 0 rgb(0 0 0 / 5%);
  display: none;
  z-index: 99;
}
#force_des {
  font-size: 0.8em;
}
#force {
  height: 540px;
}
</style>
