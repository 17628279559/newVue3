<script setup>
import { onMounted } from 'vue'
import Tidy from './tidy.js'
import data from './tidy.json'
const his_width = 1250
const his_height = 1250


const chart = Tidy(data, {
  label: d => d.name,
  link: (d, n) => `https://ourworldindata.org/global-education${d.value}`,
  width: his_width,
  height: his_width,
  margin: 100
})


onMounted(() => {
  $("#tidy").append(chart)
})
</script>

<template>
  <header-box section_class="tile color transparent-white">
    <template v-slot:title>
      <h1><a href="https://ourworldindata.org/global-education" target="_blank"><strong>全球教育</strong></a></h1>
    </template>
    <template v-slot:content>
      <div id="tidy" :width="his_width" :height="his_height" ref="svgRef1" style="background-color: rgba(0, 0, 0, 0);"></div>
    </template>
  </header-box>
</template>

<style scoped>
a {
  color: #fff;
}
</style>
