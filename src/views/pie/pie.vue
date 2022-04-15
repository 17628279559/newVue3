<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue'
import his from '../his/his.js'
import pie from './pie.js'
import Axios from 'axios'
const { proxy } = getCurrentInstance()
const date = new Date()
const getcovieApi = '/api/getcovie'
const svgRef1 = ref(null)
const svgRef2 = ref(null)
const svgRef3 = ref(null)
const svgRef4 = ref(null)
const pie1 = {
  title: `${date.getFullYear()}年${date.getMonth() + 1
    }月${date.getDate()}日各省新增疫情情况`,
  group_data: 0.01,
  use_const_color: false,
  gradient_color: ['#789DB7', '#FEE5A5', '#486D87', '#FFB838'],
  domain_gradient_color: [0, 5, 34],
  radius_inner: 150
}
const pie2 = {
  title: '各省疫情总感染人数',
  group_data: 0.1,
  use_const_color: false,
  radius_inner: 0,
  gradient_color: ['#8474A1', '#CCABDB', '#6EC6CA', '#08979D', '#055B5C'],
  domain_gradient_color: [0, 4, 34],
  stroke_width: 1,
  stroke: '#FFF'
}
const his1 = {
  xAxisLabel: `${date.getFullYear()}年${date.getMonth() + 1
    }月${date.getDate()}日各省新增疫情情况`,
  yAxisLabel: '根号下人数数',
  width: 1250,
  height: 540
}
const his2 = {
  xAxisLabel: '各省疫情总感染人数',
  yAxisLabel: '根号下人数数',
  width: 1250,
  height: 540
}
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
  Axios.get(getcovieApi).then((response) => {
    let data = response.data
    const his_data1 = get_confirm(data, 'today_confirm').map((item) => {
      return {
        id: item['index'],
        name: item['name'],
        desc: '今日新增人数',
        value: item['value']
      }
    })
    const his_data2 = get_confirm(data, 'total_confirm').map((item) => {
      return {
        id: item['index'],
        name: item['name'],
        desc: '总感染人数',
        value: item['value']
      }
    })
    pie(1, svgRef1, get_confirm(data, 'today_confirm'), pie1)
    pie(2, svgRef2, get_confirm(data, 'total_confirm'), pie2)
    his(3, svgRef3, his_data1, his1)
    his(4, svgRef4, his_data2, his2)
  })
})
</script>
<template>
  <header-box section_class="tile color transparent-white">
    <template v-slot:title>
      <h1 :style="{'display':!proxy.$piesetting.showall  ? 'block':'none'}"><a style="color:#FFF" href="http://news.163.com/special/epidemic/" target="_blank">{{pie1.title}}</a></h1>
      <h1 :style="{'display':proxy.$piesetting.showall  ? 'block':'none'}"><a style="color:#FFF" href="http://news.163.com/special/epidemic/" target="_blank">{{pie2.title}}</a></h1>
    </template>
    <template v-slot:content>
      <svg :style="{'display':!proxy.$piesetting.showall && !proxy.$piesetting.showhis ? 'block':'none'}" class="center" width="1250" height="540" ref="svgRef1" style="background-color: rgba(255, 255, 255, 0);">
      </svg>
      <svg :style="{'display':proxy.$piesetting.showall && !proxy.$piesetting.showhis ? 'block':'none'}" class="center" width="1250" height="540" ref="svgRef2" style="background-color: rgba(255, 255, 255, 0);">
      </svg>
      <svg :style="{'display':!proxy.$piesetting.showall && proxy.$piesetting.showhis ? 'block':'none'}" class="center" width="1250" height="540" ref="svgRef3" style="background-color: rgba(255, 255, 255, 0);">
      </svg>
      <svg :style="{'display':proxy.$piesetting.showall && proxy.$piesetting.showhis ? 'block':'none'}" class="center" width="1250" height="540" ref="svgRef4" style="background-color: rgba(255, 255, 255, 0);">
      </svg>
    </template>
  </header-box>
</template>

<style scoped>
</style>