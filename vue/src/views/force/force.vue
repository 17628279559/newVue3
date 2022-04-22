<script setup>
import { onMounted, watch, getCurrentInstance } from "vue"
import miserables from './data1.json'
import ForceGraph from './ForceGraph'
const { proxy } = getCurrentInstance()

const chart2 = ForceGraph(miserables, {
  nodeId: d => d.id,
  nodeGroup: d => d.group,
  width: 1000,
  height: 540,
  //   invalidation // a promise to stop the simulation when the cell is re-run
})

onMounted(() => {
  //   $("#force").append(chart)
  $("#force").append(chart2)
})
</script>

<template>
  <div>
    <div id="force_message">
    </div>
    <header-box section_class="tile color transparent-black">
      <template v-slot:title>
        <h1><a href="https://observablehq.com/@d3/force-directed-graph?collection=@d3/d3-force" target="_blank"><strong>力导向图</strong></a></h1>
      </template>
      <template v-slot:content>
        <div id="force"></div>
      </template>
    </header-box>
  </div>
</template>

<style scoped>
a {
  color: #fff;
}
#force_message {
  position: absolute !important;
  display: none;
  z-index: 9999;
  color: #fff;
  font-size: 20px;
}
#force {
  height: 540px;
}
</style>
