<script setup>
import { useRouter } from 'vue-router'
import { ref, getCurrentInstance } from 'vue'

const router = useRouter()
const { proxy } = getCurrentInstance()
window.arc = {}
window.selectArc = {}
const his_svg1 = ref(0)
const his_svg2 = ref(0)
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
const page_list = {
  page_0_0: '/',
  page_1_0: '/tree1',
  page_1_1: '/tree2',
  page_1_2: '/tree3',
  page_2_0: '/his',
  page_3_0: '/pie',
  page_4_0: '/wordCloud',
  page_5_0: '/normaltype',
  page_6_0: '/force',
  page_7_0: '/tidy'
}
const change_example = (ind1, ind2 = 0) => {
  component_name.value = ind1
  sub_component_name.value = ind2
}
const component_name = ref(0)
const sub_component_name = ref(0)
const sidebar_list = [
  { id: 0, class: 'fa-home', dropdown: false, name: '首页', news: 1 },
  {
    id: 1,
    class: 'fa-tree',
    dropdown: true,
    name: '分形树',
    subitems: [
      { id: 0, class: 'fa-leaf', name: '平平无奇普普通通分形树1', news: 0 },
      { id: 1, class: 'fa-leaf', name: '平平无奇普普通通分形树2', news: 0 },
      { id: 2, class: 'fa-leaf', name: '平平无奇普普通通分形树3', news: 0 }
    ],
    news: 0
  },
  {
    id: 2,
    class: 'fa-music',
    dropdown: false,
    name: '网易云飙升榜实时直方图',
    news: 0
  },
  {
    id: 3,
    class: 'fa-shield',
    dropdown: false,
    name: '中国每日疫情新增',
    news: 0
  },
  {
    id: 4,
    class: 'fa-cloud',
    dropdown: false,
    name: '全国人大十三届五次全会词云图',
    news: 0
  },
  {
    id: 5,
    class: 'fa-circle-o',
    dropdown: false,
    name: '正规式->NFA->DFA->最简DFA',
    news: 0
  },
  {
    id: 6,
    class: 'fa-share-alt',
    dropdown: false,
    name: '力导向图',
    news: 0
  },
  {
    id: 7,
    class: 'fa-circle-o-notch',
    dropdown: false,
    name: '全球教育',
    news: 0
  }
]
const sidebar_list_setting = [
  {
    id: 0,
    fatherid: 2,
    name: '切换随机数据',
    func: () => {
      if ($(`#switch-0-2`)[0]['checked']) {
        proxy.$usefake.value = false
      } else {
        proxy.$usefake.value = true
      }
    }
  },
  {
    id: 1,
    fatherid: 3,
    name: '切换总数据',
    func: () => {
      if ($(`#switch-1-3`)[0]['checked']) {
        proxy.$piesetting.showall = false
      } else {
        proxy.$piesetting.showall = true
      }
    }
  },
  {
    id: 2,
    fatherid: 3,
    name: '切换直方图',
    func: () => {
      if ($(`#switch-2-3`)[0]['checked']) {
        proxy.$piesetting.showhis = false
      } else {
        proxy.$piesetting.showhis = true
      }
    }
  },
  {
    id: 3,
    fatherid: 4,
    name: '切换python词云',
    func: () => {
      if ($(`#switch-3-4`)[0]['checked']) {
        proxy.$wordCloudPython.show = false
      } else {
        proxy.$wordCloudPython.show = true
      }
    }
  },
  {
    id: 4,
    fatherid: 6,
    name: '切换透明背景',
    func: () => {
      if ($(`#switch-4-6`)[0]['checked']) {
        proxy.$force.value = 0
      } else {
        proxy.$force.value = 1
      }
    }
  }
]
</script>

<template>
  <div class="mm-page">
    <div class="mask">
      <div id="loader"></div>
    </div>
    <div id="wrap">
      <div class="row">
        <div class="navbar navbar-default navbar-fixed-top navbar-transparent-black mm-fixed-top" role="navigation" id="navbar">
          <!-- 左上角组件 -->
          <div class="navbar-header col-md-2">
            <a class="navbar-brand" href="#"> <strong>Snake</strong>Tao </a>
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
            <div class="search" id="main-search"><i class="fa fa-search"></i> <input type="text" placeholder="不能搜索就是个样子" /></div>

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
                  <li v-for="(item, index) in top_list_thing" :key="index">
                    <a href="#">
                      <div class="task-info">
                        <div class="desc">{{ item.desc }}</div>
                        <div class="percent">{{ item.percent }}</div>
                      </div>
                      <div class="progress progress-striped active progress-thin">
                        <div class="progress-bar" :class="item.color" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" :style="{ width: item.percent }"></div>
                      </div>
                    </a>
                  </li>
                  <li>
                    <a href="https://github.com/17628279559" target="_blank">看看源码? <i class="fa fa-angle-right"></i></a>
                  </li>
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
                <a class="dropdown-toggle options" data-toggle="dropdown" href="#"> {{ user.name }} <i class="fa fa-caret-down"></i> </a>

                <ul class="dropdown-menu arrow settings">
                  <li>
                    <h3>更换背景:</h3>
                    <ul id="color-schemes">
                      <li v-for="(item, index) in body_background" :key="index"><a :class="item"></a></li>
                    </ul>
                  </li>
                  <li class="divider"></li>
                  <li>
                    <a href="https://zwt666.top/" target="_blank"><i class="fa fa-user"></i> 个人博客</a>
                  </li>
                  <li>
                    <a href="https://github.com/17628279559" target="_blank"><i class="fa fa-github"></i> 个人仓库</a>
                  </li>
                  <li></li>
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
                <a href="#" class="sidebar-toggle" data-toggle="#navigation">成品样例<i class="fa fa-angle-up"></i></a>
                <ul class="menu">
                  <li v-for="(item, findex) in sidebar_list" :key="findex" :class="{ active: component_name === item.id, dropdown: item.dropdown, open: item.dropdown && component_name === item.id }">
                    <a v-if="item.dropdown" href="#" class="dropdown-toggle" data-toggle="dropdown">
                      <i class="fa" :class="item.class"></i> {{ item.name }}
                      <span v-if="item.news > 0" class="badge badge-red">{{ item.news }}</span>
                      <b class="fa fa-plus dropdown-plus"></b>
                    </a>
                    <router-link v-else :to="page_list[`page_${item.id}_0`]" @click="change_example(item.id)">
                      <i class="fa" :class="item.class"></i> {{ item.name }}
                      <span v-if="item.news > 0" class="badge badge-red">{{ item.news }}</span>
                    </router-link>
                    <ul v-if="item.dropdown" class="dropdown-menu">
                      <li v-for="(sub_item, sindex) in item.subitems" :key="sindex" :class="{ active: component_name === item.id && sub_component_name === sub_item.id }">
                        <router-link :to="page_list[`page_${item.id}_${sub_item.id}`]" @click="change_example(item.id, sub_item.id)"> <i class="fa" :class="sub_item.class"></i> {{ sub_item.name }} </router-link>
                      </li>
                    </ul>
                  </li>
                </ul>
              </li>

              <!-- 左边侧边栏按钮 -->
              <li class="settings" id="general-settings">
                <a href="#" class="sidebar-toggle underline" data-toggle="#general-settings">设置 <i class="fa fa-angle-up"></i></a>
                <div v-for="(item, stindex) in sidebar_list_setting" :key="stindex">
                  <div v-if="component_name === item.fatherid" class="form-group">
                    <label class="col-xs-8 control-label">{{ item.name }}</label>
                    <div class="col-xs-4 control-label">
                      <div class="onoffswitch greensea">
                        <input type="checkbox" name="onoffswitch" class="onoffswitch-checkbox" :id="`switch-${item.id}-${item.fatherid}`" />
                        <label class="onoffswitch-label" :for="`switch-${item.id}-${item.fatherid}`" @click="item.func">
                          <span class="onoffswitch-inner"></span>
                          <span class="onoffswitch-switch"></span>
                        </label>
                      </div>
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
              <prompt></prompt>
              <router-view></router-view>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
a {
  color: #fff;
}
.main-comtent {
  height: 2000px;
}
</style>
