<script setup>
import { ref, onMounted } from 'vue'
import Axios from 'axios'
import pie from './pie.js'
import his from './his.js'

let co2 = [
  { name: 'Road', value: 11.9 },
  { index: 1, name: 'Aviation', value: 1.9 },
  { index: 2, name: 'Rail', value: 0.4 },
  { index: 3, name: 'Pipeline', value: 0.3 },
  { index: 4, name: 'Ship', value: 1.7 },
  { index: 5, name: 'Residential', value: 10.9 },
  { index: 6, name: 'Commercial', value: 6.6 },
  { index: 7, name: 'Iron&Steel', value: 7.2 },
  { index: 8, name: 'Non-ferousmetals', value: 0.7 },
  { index: 9, name: 'Machinery', value: 0.5 },
  { index: 10, name: 'Foodandtobacco', value: 1 },
  { index: 11, name: 'Paper,pulp&printing', value: 0.6 },
  { index: 12, name: 'Chemical&petrochemical(energy)', value: 3.6 },
  { index: 13, name: 'Otherindustry', value: 10.6 },
  { index: 14, name: 'EnergyinAgri&Fishing', value: 1.7 },
  { index: 15, name: 'Unallocatedfuelcombustion', value: 7.8 },
  { index: 16, name: 'Coal', value: 1.9 },
  { index: 17, name: 'Oil&NaturalGas', value: 3.9 },
  { index: 18, name: 'Cement', value: 3 },
  { index: 19, name: 'Chemical&petrochemical(industrial)', value: 2.2 },
  { index: 20, name: 'Livestock&Manure', value: 5.8 },
  { index: 21, name: 'RiceCultivation', value: 1.3 },
  { index: 22, name: 'AgriculturalSoils', value: 4.1 },
  { index: 23, name: 'CropBurning', value: 3.5 },
  { index: 24, name: 'ForestLand', value: 2.2 },
  { index: 25, name: 'Cropland', value: 1.4 },
  { index: 26, name: 'Grassland', value: 0.1 },
  { index: 27, name: 'Landfills', value: 1.9 },
  { index: 28, name: 'Wastewater', value: 1.3 }
]

window.arc = {}
window.selectArc = {}
const svgRef1 = ref(null)
const svgRef2 = ref(null)
const svgRef3 = ref(null)
const svgRef4 = ref(null)
const svgRef5 = ref(null)
const svgRef6 = ref(null)
const svgRef7 = ref(null)
const svgRef8 = ref(null)
const getdataApi = '/api/getcovie'

let get_random_data = (limit) => {
  let data = []
  let getRandomInt = (min, max) =>
    Math.floor(Math.random() * (max - min + 1)) + min
  for (let i = 0; i < limit; i++) {
    data.push({
      index: i,
      name: `test${i + 1}`,
      value: getRandomInt(0, 500)
    })
  }
  return data
}

let data

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

const pie1 = {
  title: '各省今日新增',
  group_data: 0,
  use_const_color: false,
  radius_inner: 0,
  gradient_color: ['#FF2525', '#FFE53B', '#FAD961'],
  domain_gradient_color: [0, 4, 34],
  stroke_width: 2,
  stroke: '#FFF'
}

const pie2 = {
  title: '各省总数据',
  group_data: 0.2,
  use_const_color: false,
  gradient_color: ['#FF2525', '#FFE53B', '#FAD961'],
  domain_gradient_color: [0, 5, 34],
  radius_inner: 150
}
const pie3 = {
  title: '随机渐变',
  group_data: 0,
  radius_inner: 0,
  text_anchor: 'left',
  is_rotate: true
}
const pie4 = {
  title: '随机圆环',
  padAngle: 0.005,
  group_data: 0,
  radius_inner: 180,
  is_rotate: true,
  stroke_width: 3,
  text_anchor: 'left',
  stroke: '#DCF'
}

const pie5 = {
  show_lable_text: false,
  use_const_color: false,
  radius_outer: 160,
  gradient_color: ['#3EECAC', '#EE74E7', '#FA8BFF', '#74EBD5', '#3EECAC']
}

const pie6 = {
  title: '双重圆环',
  padAngle: 0.005,
  group_data: 0,
  use_const_color: false,
  radius_inner: 190,
  is_rotate: true,
  text_anchor: 'left',
  gradient_color: ['#3EECAC', '#EE74E7', '#FA8BFF', '#74EBD5', '#3EECAC']
}

const pie7 = {
  title: '二氧化碳排放量占比',
  padAngle: 0.005,
  group_data: 0,
  radius_inner: 100,
  radius_outer: 200,
  lable_text_size: '0.8em',
  radius_label: 220,
  is_rotate: true,
  text_anchor: 'left'
}

const opt1 = { xAxisLabel: '每日疫情情况' }
const opt2 = {
  xAxisLabel: '总疫情情况'
}

const constdata = get_random_data(40)

onMounted(() => {
  Axios.get(getdataApi).then((response) => {
    data = response.data
    const zdata1 = get_confirm(data, 'today_confirm').map((item) => {
      return { id: item['index'], name: item['name'], value: item['value'] }
    })
    const zdata2 = get_confirm(data, 'total_confirm').map((item) => {
      return { id: item['index'], name: item['name'], value: item['value'] }
    })
    pie(1, svgRef1, get_confirm(data, 'today_confirm'), pie1)
    pie(2, svgRef2, get_confirm(data, 'total_confirm'), pie2)
    his(3, svgRef3, zdata1, opt1)
    his(4, svgRef4, zdata2, opt2)
    pie(5, svgRef5, co2, pie7)
    pie(6, svgRef6, get_random_data(30), pie3)
    pie(7, svgRef7, get_random_data(17), pie4)
    pie(8, svgRef8, constdata, pie5)
    pie(9, svgRef8, constdata, pie6)
  })
})
</script>

<template>
  <div id="all">
    <h1>中国各省疫情实时饼图</h1>
    <h3>赵文韬-2019302120066</h3>
    <div style="clear:both"></div>
    <svg class="center" width=1000 height=550 ref="svgRef1">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef2">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef3">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef4">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef5">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef6">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef7">
    </svg>
    <svg class="center" width=1000 height=550 ref="svgRef8">
    </svg>
  </div>

</template>

<style scoped>
h1 {
  text-align: center;
}
h3 {
  margin-right: 160px;
  float: right;
}
#all {
  width: 100%;
  height: 100%;
}
.center {
  display: block;
  background: #f5f5f5;
  margin: 10px;
  float: left;
}
</style>
