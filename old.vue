<script setup>
import { ref, onMounted, watch } from 'vue'
import P5 from 'p5'
import Axios from 'axios'
import exam1 from './components/tree/exam1.js'
import exam2 from './components/tree/exam2.js'
import wordtree from './components/wordtree/wordtree.js'
import his from './components/histogram/his.js'
import gpie from './components/pieChart/pie.js'

window.arc = {}
window.selectArc = {}
const body_background = ['bg-1', 'bg-2', 'bg-3', 'bg-4', 'bg-5', 'bg-6']
const top_list_thing = [
  { desc: 'c++', percent: '80%', color: 'progress-bar-green' },
  { desc: 'python', percent: '15%', color: 'progress-bar-cyan' },
  { desc: 'vue', percent: '5%', color: 'progress-bar-orange' },
  { desc: 'uniapp', percent: '30%', color: 'progress-bar-red' },
  { desc: 'java', percent: '60%', color: 'progress-bar-amethyst' }
]
const user = {
  name: 'snaketao'
}
let date = new Date()
const getdataApi = '/api/getdata'
const getcovieApi = '/api/getcovie'
const usefake = ref(false)
const tree1 = new P5(exam1, 'p5Canvas1')
const tree2 = new P5(exam2, 'p5Canvas2')
const tree3 = new P5(wordtree, 'p5Canvas3')
const component_name = ref(-1)
const his_svg1 = ref(0)
const his_svg2 = ref(0)
const svgRef1 = ref(null)
const svgRef2 = ref(null)
const svgRef3 = ref(null)
const svgRef4 = ref(null)
const svgRef5 = ref(null)
const status = ref('切换随机数据')
const pie1 = {
  title: `${date.getFullYear()}年${
    date.getMonth() + 1
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
const change_example = (index) => {
  component_name.value = index
}

const change_random = () => {
  if ($('#switch-on')[0]['checked']) {
    usefake.value = false
  } else {
    usefake.value = true
  }
}
const change_all = () => {
  if ($('#switch-off1')[0]['checked']) {
    his_svg1.value = 0
  } else {
    his_svg1.value = 1
  }
}
const change_his = () => {
  if ($('#switch-off2')[0]['checked']) {
    his_svg2.value = 0
  } else {
    his_svg2.value = 1
  }
}

let his_width = 1250,
  his_height = 650,
  pie_width = 1250,
  pie_height = 650

watch(component_name, (new_value, old_value) => {
  if (new_value === 3) {
    Axios.get(
      getdataApi + `?use_fake=${usefake.value ? 'true' : 'false'}`
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
          getdataApi + `?use_fake=${usefake.value ? 'true' : 'false'}`
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
  } else if (new_value === 4) {
    Axios.get(getcovieApi).then((response) => {
      let data = response.data
      const zdata1 = get_confirm(data, 'today_confirm').map((item) => {
        return {
          id: item['index'],
          name: item['name'],
          desc: '今日新增人数',
          value: item['value']
        }
      })
      const zdata2 = get_confirm(data, 'total_confirm').map((item) => {
        return {
          id: item['index'],
          name: item['name'],
          desc: '总感染人数',
          value: item['value']
        }
      })
      let opt1 = {
        xAxisLabel: `${date.getFullYear()}年${
          date.getMonth() + 1
        }月${date.getDate()}日各省新增疫情情况`,
        yAxisLabel: '根号下人数数',
        width: his_width,
        height: his_height
      }
      let opt2 = {
        xAxisLabel: '各省疫情总感染人数',
        yAxisLabel: '根号下人数数',
        width: his_width,
        height: his_height
      }
      gpie(1, svgRef2, get_confirm(data, 'today_confirm'), pie1)
      gpie(2, svgRef3, get_confirm(data, 'total_confirm'), pie2)
      his(3, svgRef4, zdata1, opt1)
      his(4, svgRef5, zdata2, opt2)
    })
  }
})
</script>

<template>
  <div>
    <div class="mask">
      <div id="loader"></div>
    </div>
    <div id="wrap">
      <div class="row">
        <div class="navbar navbar-default navbar-fixed-top navbar-transparent-black mm-fixed-top" role="navigation" id="navbar">

          <!-- 左上角组件 -->
          <div class="navbar-header col-md-2">
            <a class="navbar-brand" href="#">
              <strong>Snake</strong>Tao
            </a>
            <div class="sidebar-collapse">
              <a href="#">
                <i class="fa fa-bars"></i>
              </a>
            </div>
          </div>

          <!-- 顶部组件 -->
          <div class="navbar-collapse">

            <!-- 刷新 -->
            <ul class="nav navbar-nav refresh">
              <li class="divided">
                <a href="#" class="page-refresh"><i class="fa fa-refresh"></i></a>
              </li>
            </ul>

            <!-- 搜索 -->
            <div class="search" id="main-search">
              <i class="fa fa-search"></i> <input type="text" placeholder="不能搜索就是个样子">
            </div>

            <!-- 顶部右边组件 -->
            <ul class="nav navbar-nav quick-actions">
              <!-- 顶部下拉菜单 -->
              <li class="dropdown divided">

                <a class="dropdown-toggle button" data-toggle="dropdown" href="#">
                  <i class="fa fa-tasks"></i>
                  <span class="label label-transparent-black">2</span>
                </a>

                <ul class="dropdown-menu wide arrow nopadding bordered">
                  <li>
                    <h1>各语言使用情况(假的)</h1>
                  </li>
                  <li v-for="(item,index) in top_list_thing" :key="index">
                    <a href="#">
                      <div class="task-info">
                        <div class="desc">{{item.desc}}</div>
                        <div class="percent">{{item.percent}}</div>
                      </div>
                      <div class="progress progress-striped active progress-thin">
                        <div class="progress-bar" :class="item.color" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" :style="{'width': item.percent}">
                        </div>
                      </div>
                    </a>
                  </li>
                  <li><a href="https://github.com/17628279559" target="_blank">看看源码? <i class="fa fa-angle-right"></i></a></li>
                </ul>

              </li>

              <li class="dropdown divided">
                <a class="dropdown-toggle button" data-toggle="dropdown" href="#">
                  <i class="fa fa-envelope"></i>
                  <span class="label label-transparent-black">1</span>
                </a>
              </li>

              <!-- 右上角个人介绍 -->
              <li class="dropdown divided user" id="current-user">
                <div class="profile-photo">
                  <img src="./assets/images/img.jpg" />
                </div>
                <a class="dropdown-toggle options" data-toggle="dropdown" href="#">
                  {{user.name}} <i class="fa fa-caret-down"></i>
                </a>

                <ul class="dropdown-menu arrow settings">

                  <li>

                    <h3>更换背景:</h3>
                    <ul id="color-schemes">
                      <li v-for="(item,index) in body_background" :key="index"><a :class="item"></a></li>
                    </ul>

                  </li>

                  <li class="divider"></li>

                  <li>
                    <a href="https://zwt666.top/" target="_blank"><i class="fa fa-user"></i> 个人博客</a>
                  </li>

                  <li>
                    <a href="https://github.com/17628279559" target="_blank"><i class="fa fa-github"></i> 个人仓库</a>
                  </li>

                  <li>
                  </li>
                </ul>
              </li>
            </ul>

            <!-- 左边菜单 -->
            <ul class="nav navbar-nav side-nav" id="sidebar">

              <li class="collapsed-content">
                <ul>
                  <li class="search"></li>
                </ul>
              </li>

              <li class="navigation" id="navigation">
                <a href="#" class="sidebar-toggle" data-toggle="#navigation">成品样例 <i class="fa fa-angle-up"></i></a>

                <ul class="menu">

                  <li :class="{'active':component_name===-1}">
                    <a href="#" @click="change_example(-1)">
                      <i class="fa fa-home"></i> 首页
                      <span class="badge badge-red">1</span>
                    </a>
                  </li>

                  <li class="dropdown" :class="{'active':component_name===0 || component_name===1 || component_name===2,'open':component_name===0 || component_name===1 || component_name===2}">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                      <i class="fa fa-leaf"></i> 分形树 <b class="fa fa-plus dropdown-plus"></b>
                    </a>
                    <ul class="dropdown-menu">
                      <li :class="{'active':component_name===0}">
                        <a href="#" @click="change_example(0)">
                          <i class="fa fa-leaf"></i> 平平无奇普普通通树1
                        </a>
                      </li>
                      <li :class="{'active':component_name===1}">
                        <a href="#" @click="change_example(1)">
                          <i class="fa fa-leaf"></i> 平平无奇普普通通树2
                        </a>
                      </li>
                      <li :class="{'active':component_name===2}">
                        <a href="#" @click="change_example(2)">
                          <i class="fa fa-leaf"></i> 平平无奇普普通通树3
                        </a>
                      </li>
                    </ul>
                  </li>

                  <li :class="{'active':component_name===3}">
                    <a href="#" @click="change_example(3)">
                      <i class="fa fa-music"></i> 网易云飙升榜实时直方图
                    </a>
                  </li>

                  <li :class="{'active':component_name===4}">
                    <a href="#" @click="change_example(4)">
                      <i class="fa fa-shield"></i> 中国每日疫情新增
                    </a>
                  </li>

                  <li>
                    <a href="#">
                      <i class="fa fa-bar-chart-o"></i> 图表
                    </a>
                  </li>

                </ul>

              </li>

              <!-- 左边侧边栏按钮 -->
              <li v-if="component_name === 3 || component_name === 4" class="settings" id="general-settings">
                <a href="#" class="sidebar-toggle underline" data-toggle="#general-settings">设置 <i class="fa fa-angle-up"></i></a>

                <div v-if="component_name === 3" class="form-group">
                  <label class="col-xs-8 control-label">{{status}}</label>
                  <div class="col-xs-4 control-label">
                    <div class="onoffswitch greensea">
                      <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="switch-on">
                      <label class="onoffswitch-label" for="switch-on" @click="change_random()">
                        <span class="onoffswitch-inner"></span>
                        <span class="onoffswitch-switch"></span>
                      </label>
                    </div>
                  </div>
                </div>

                <div v-if="component_name === 4" class="form-group">
                  <label class="col-xs-8 control-label">切换为总数据</label>
                  <div class="col-xs-4 control-label">
                    <div class="onoffswitch greensea">
                      <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="switch-off1">
                      <label class="onoffswitch-label" for="switch-off1" @click="change_all()">
                        <span class="onoffswitch-inner"></span>
                        <span class="onoffswitch-switch"></span>
                      </label>
                    </div>
                  </div>
                </div>

                <div v-if="component_name === 4" class="form-group">
                  <label class="col-xs-8 control-label">切换为直方图</label>
                  <div class="col-xs-4 control-label">
                    <div class="onoffswitch greensea">
                      <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" id="switch-off2">
                      <label class="onoffswitch-label" for="switch-off2" @click="change_his()">
                        <span class="onoffswitch-inner"></span>
                        <span class="onoffswitch-switch"></span>
                      </label>
                    </div>
                  </div>
                </div>

              </li>

            </ul>

          </div>

        </div>
        <div id="content" class="col-md-12">
          <div class="main">
            <div class="row">
              <div id="his_message">
                <div class="meaasge-header">
                  <div id="music_title">text</div>
                  <div class="linediv"></div>
                  <div id="music_com">评论数:</div>
                  <div id="music_pubdate">发布时间</div>
                  <div id="music_desc">desc</div>
                </div>

              </div>
              <div :style="{'display':component_name === 0 ? 'block':'none'}" id="p5Canvas1">
              </div>
              <div :style="{'display':component_name === 1 ? 'block':'none'}" id="p5Canvas2">
              </div>
              <div :style="{'display':component_name === 2 ? 'block':'none'}" id="p5Canvas3">
              </div>
              <div v-if="component_name === 3">
                <svg class="center" :width="his_width" :height="his_height" ref="svgRef1" style="background-color: rgba(255, 255, 255, 0.15);border-radius: 10px;">
                </svg>
              </div>
              <div v-if="component_name === 4">
                <svg :style="{'display':his_svg1 === 0 && his_svg2 === 0 ? 'block':'none'}" class="center" :width="pie_width" :height="pie_height" ref="svgRef2" style="background-color: rgba(255, 255, 255, 0.15);border-radius: 10px;">
                </svg>
                <svg :style="{'display':his_svg1 === 1 && his_svg2 === 0 ? 'block':'none'}" class="center" :width="pie_width" :height="pie_height" ref="svgRef3" style="background-color: rgba(255, 255, 255, 0.15);border-radius: 10px;">
                </svg>
                <svg :style="{'display':his_svg1 === 0 && his_svg2 === 1 ? 'block':'none'}" class="center" :width="pie_width" :height="pie_height" ref="svgRef4" style="background-color: rgba(255, 255, 255, 0.15);border-radius: 10px;">
                </svg>
                <svg :style="{'display':his_svg1 === 1 && his_svg2 === 1 ? 'block':'none'}" class="center" :width="pie_width" :height="pie_height" ref="svgRef5" style="background-color: rgba(255, 255, 255, 0.15);border-radius: 10px;">
                </svg>
              </div>
              <section class="tile color transparent-white">

                <!-- tile header -->
                <div class="tile-header">
                  <h1><strong>Pie</strong> Chart</h1>
                  <span class="note">Custom Labels</span>
                  <div class="controls">
                    <a href="#" class="refresh"><i class="fa fa-refresh"></i></a>
                    <a href="#" class="remove"><i class="fa fa-times"></i></a>
                  </div>
                </div>

              </section>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
</style>
