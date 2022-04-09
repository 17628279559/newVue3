<script setup>
import { ref, onMounted } from 'vue'
import Tree1 from './components/tree/children/example1.vue'
import Tree2 from './components/tree/children/example2.vue'
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

const component_name = ref(1)
const change_example = index => {
  component_name.value = index;
}
onMounted(() => { })
</script>

<template>
  <div class="mask">
    <div id="loader"></div>
  </div>
  <div id="wrap">
    <div class="row">
      <div class="navbar navbar-default navbar-fixed-top navbar-transparent-black mm-fixed-top"
           role="navigation"
           id="navbar">

        <!-- 左上角组件 -->
        <div class="navbar-header col-md-2">
          <a class="navbar-brand"
             href="#">
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
              <a href="#"
                 class="page-refresh"><i class="fa fa-refresh"></i></a>
            </li>
          </ul>

          <!-- 搜索 -->
          <div class="search"
               id="main-search">
            <i class="fa fa-search"></i> <input type="text"
                   placeholder="不能搜索就是个样子">
          </div>

          <!-- 顶部右边组件 -->
          <ul class="nav navbar-nav quick-actions">
            <!-- 顶部下拉菜单 -->
            <li class="dropdown divided">

              <a class="dropdown-toggle button"
                 data-toggle="dropdown"
                 href="#">
                <i class="fa fa-tasks"></i>
                <span class="label label-transparent-black">2</span>
              </a>

              <ul class="dropdown-menu wide arrow nopadding bordered">
                <li>
                  <h1>各语言使用情况(假的)</h1>
                </li>
                <li v-for="(item,index) in top_list_thing"
                    :key="index">
                  <a href="#">
                    <div class="task-info">
                      <div class="desc">{{item.desc}}</div>
                      <div class="percent">{{item.percent}}</div>
                    </div>
                    <div class="progress progress-striped progress-thin">
                      <div class="progress-bar"
                           :class="item.color"
                           role="progressbar"
                           aria-valuenow="45"
                           aria-valuemin="0"
                           aria-valuemax="100"
                           :style="{'width': item.percent}">
                      </div>
                    </div>
                  </a>
                </li>
                <li><a href="https://github.com/17628279559">看看源码? <i class="fa fa-angle-right"></i></a></li>
              </ul>

            </li>

            <li class="dropdown divided">
              <a class="dropdown-toggle button"
                 data-toggle="dropdown"
                 href="#">
                <i class="fa fa-envelope"></i>
                <span class="label label-transparent-black">1</span>
              </a>
            </li>

            <!-- 右上角个人介绍 -->
            <li class="dropdown divided user"
                id="current-user">
              <div class="profile-photo">
                <img src="./assets/images/img.jpg" />
              </div>
              <a class="dropdown-toggle options"
                 data-toggle="dropdown"
                 href="#">
                {{user.name}} <i class="fa fa-caret-down"></i>
              </a>

              <ul class="dropdown-menu arrow settings">

                <li>

                  <h3>更换背景:</h3>
                  <ul id="color-schemes">
                    <li v-for="(item,index) in body_background"
                        :key="index"><a :class="item"></a></li>
                  </ul>

                </li>

                <li class="divider"></li>

                <li>
                  <a href="https://zwt666.top/"><i class="fa fa-user"></i> 个人博客</a>
                </li>

                <li>
                  <a href="https://github.com/17628279559"><i class="fa fa-github"></i> 个人仓库</a>
                </li>

                <li>
                </li>
              </ul>
            </li>
          </ul>

          <!-- 左边菜单 -->
          <ul class="nav navbar-nav side-nav"
              id="sidebar">

            <li class="collapsed-content">
              <ul>
                <li class="search"></li>
              </ul>
            </li>

            <li class="navigation"
                id="navigation">
              <a href="#"
                 class="sidebar-toggle"
                 data-toggle="#navigation">成品样例 <i class="fa fa-angle-up"></i></a>

              <ul class="menu">

                <li class="active">
                  <a href="#">
                    <i class="fa fa-tachometer"></i> 首页
                    <span class="badge badge-red">1</span>
                  </a>
                </li>

                <li class="dropdown">
                  <a href="#"
                     class="dropdown-toggle"
                     data-toggle="dropdown">
                    <i class="fa fa-th-large"></i> 分形树 <b class="fa fa-plus dropdown-plus"></b>
                  </a>
                  <ul class="dropdown-menu">
                    <li>
                      <a href="#"
                         @click="change_example(0)">
                        <i class="fa fa-caret-right"></i> 平平无奇普普通通树1
                      </a>
                    </li>
                    <li>
                      <a href="#"
                         @click="change_example(1)">
                        <i class="fa fa-caret-right"></i> 平平无奇普普通通树2
                      </a>
                    </li>
                  </ul>
                </li>

                <li>
                  <a href="#">
                    <i class="fa fa-tint"></i> 留一个例子
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
            <li class="settings"
                id="general-settings">
              <a href="#"
                 class="sidebar-toggle underline"
                 data-toggle="#general-settings">设置 <i class="fa fa-angle-up"></i></a>

              <div class="form-group">
                <label class="col-xs-8 control-label">干啥没想好1</label>
                <div class="col-xs-4 control-label">
                  <div class="onoffswitch greensea">
                    <input type="checkbox"
                           name="onoffswitch"
                           class="onoffswitch-checkbox"
                           id="switch-on">
                    <label class="onoffswitch-label"
                           for="switch-on">
                      <span class="onoffswitch-inner"></span>
                      <span class="onoffswitch-switch"></span>
                    </label>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="col-xs-8 control-label">干啥没想好2</label>
                <div class="col-xs-4 control-label">
                  <div class="onoffswitch greensea">
                    <input type="checkbox"
                           name="onoffswitch"
                           class="onoffswitch-checkbox"
                           id="switch-off">
                    <label class="onoffswitch-label"
                           for="switch-off">
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

    </div>
    <div id="content"
         class="col-md-12">
      <div class="main">
        <div class="row">
          <div :style="{'display':component_name === 0 ? 'block':'none'}"
               id="p5Canvas1">
            <Tree1></Tree1>
          </div>
          <div :style="{'display':component_name === 1 ? 'block':'none'}"
               id="p5Canvas2">
            <Tree2></Tree2>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style>
</style>
