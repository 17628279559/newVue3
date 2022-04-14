<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue'
import his from './his.js'
import Axios from 'axios'

const getdataApi = '/api/getdata'
const { proxy } = getCurrentInstance()
const svgRef1 = ref(null)
const his_width = 1250
const his_height = 650
const get_confirm = (data, field) => {
  let i = 0
  let tmpdata = data.map((item) => {
    return { index: 0, name: item['name'], value: item[field] }
  })
  tmpdata.sort((a, b) => b.value - a.value)
  return tmpdata.map((item) => {
    return { index: i++, name: item['name'], value: item['value'] }
  })
}
onMounted(() => {
  Axios.get(
    getdataApi + `?use_fake=${proxy.$usefake.value ? 'true' : 'false'}`
  ).then((response) => {
    let data = response.data
    let his_options = {
      xAxisLabel: '网易云实时飙升榜榜单',
      yAxisLabel: '根号下评论数',
      width: his_width,
      height: his_height
    }
    his(0, svgRef1, data, his_options)
  })

  window.setInterval(() => {
    setTimeout(() => {
      Axios.get(
        getdataApi + `?use_fake=${proxy.$usefake.value ? 'true' : 'false'}`
      ).then((response) => {
        let data = response.data
        let his_options = {
          xAxisLabel: '网易云实时飙升榜榜单',
          yAxisLabel: '根号下评论数',
          width: his_width,
          height: his_height
        }
        his(0, svgRef1, data, his_options, true)
      })
    }, 1000)
  }, 1000)
})
</script>


<template>
  <svg class="center" :width="his_width" :height="his_height" ref="svgRef1" style="background-color: rgba(255, 255, 255, 0.15);border-radius: 10px;">
  </svg>
</template>

<style scoped>
</style>