<script setup>
import { onMounted } from 'vue'

const morris_id_list = [
  'morris-line-example',
  'morris-line-area-example',
  'morris-bar-example',
  'morris-donut-example'
]
const sparkline_id_list = ['sparkline01', 'sparkline02', 'sparkline03']
const easypie_item_list = [
  {
    percent: '30',
    size: '110',
    track_color: 'rgba(0,0,0,.2)',
    bar_color: '#16a085',
    scale_color: '#FFFFFF',
    line_cap: 'butt',
    line_width: '8',
    value: 30,
    content: 'test1'
  },
  {
    percent: '30',
    size: '110',
    track_color: 'rgba(0,0,0,.2)',
    bar_color: '#FF2233',
    scale_color: 'false',
    line_cap: 'round',
    line_width: '10',
    value: 30,
    content: 'test2'
  },
  {
    percent: '30',
    size: '110',
    track_color: 'rgba(0,0,0,.2)',
    bar_color: '#A40778',
    scale_color: '#D9AFD9',
    line_cap: 'butt',
    line_width: '8',
    value: 30,
    content: 'test3'
  }
]
const justgage_id_list = ['gauge01', 'gauge02', 'gauge03']
onMounted(() => {
  $('#morris-line-example').children().remove()
  $('#morris-line-area-example').children().remove()
  $('#morris-bar-example').children().remove()
  $('#morris-donut-example').children().remove()

  Morris.Line({
    element: 'morris-line-example',
    data: [
      { y: '2009', a: 15, b: 5 },
      { y: '2010', a: 20, b: 10 },
      { y: '2011', a: 35, b: 25 },
      { y: '2012', a: 40, b: 30 }
    ],
    xkey: 'y',
    ykeys: ['a', 'b'],
    labels: ['Series A', 'Series B'],
    lineColors: ['#16a085', '#FF0066']
  })
  Morris.Area({
    element: 'morris-line-area-example',
    data: [
      { y: '2009', a: 10, b: 3 },
      { y: '2010', a: 14, b: 5 },
      { y: '2011', a: 8, b: 2 },
      { y: '2012', a: 20, b: 15 }
    ],
    xkey: 'y',
    ykeys: ['a', 'b'],
    labels: ['Series A', 'Series B'],
    lineColors: ['#a2d200', '#d2d2d2'],
    lineWidth: '0',
    grid: false,
    fillOpacity: '0.5'
  })
  Morris.Bar({
    element: 'morris-bar-example',
    data: [
      { y: '2009', a: 75, b: 65 },
      { y: '2010', a: 50, b: 40 },
      { y: '2011', a: 75, b: 65 },
      { y: '2012', a: 100, b: 90 }
    ],
    xkey: 'y',
    ykeys: ['a', 'b'],
    labels: ['Series A', 'Series B'],
    barColors: ['#ff4a43', '#1693A5']
  })
  Morris.Donut({
    element: 'morris-donut-example',
    data: [
      { label: 'Download Sales', value: 12 },
      { label: 'In-Store Sales', value: 30 },
      { label: 'Mail-Order Sales', value: 20 }
    ],
    colors: ['#00a3d8', '#2fbbe8', '#72cae7']
  })

  $('#sparkline01').sparkline([15, 16, 18, 17, 16, 18, 25, 26, 23], {
    type: 'line',
    width: '100%',
    height: '250px',
    fillColor: 'rgba(34, 190, 239, .3)',
    lineColor: 'rgba(34, 190, 239, .5)',
    lineWidth: 2,
    spotRadius: 5,
    valueSpots: [5, 6, 8, 7, 6, 8, 5, 4, 7],
    minSpotColor: '#eaf9fe',
    maxSpotColor: '#00a3d8',
    highlightSpotColor: '#00a3d8',
    highlightLineColor: '#bec6ca',
    normalRangeMin: 0
  })
  $('#sparkline01').sparkline([1, 2, 1, 3, 1, 2, 4, 1, 3], {
    type: 'line',
    composite: true,
    width: '100%',
    height: '250px',
    fillColor: 'rgba(255, 74, 67, .6)',
    lineColor: 'rgba(255, 74, 67, .8)',
    lineWidth: 2,
    minSpotColor: '#ffeced',
    maxSpotColor: '#d90200',
    highlightSpotColor: '#d90200',
    highlightLineColor: '#bec6ca',
    spotRadius: 5,
    valueSpots: [2, 3, 4, 3, 1, 2, 4, 1, 3],
    normalRangeMin: 0
  })

  let values = [5, 6, 7, 2, 1, -4, -2, 4, 6, 8].map(parseFloat)
  let type = 'bar'
  let height = '250px'
  let parentWidth = $('#sparkline02').parent().width()
  let valueCount = values.length
  let barSpacing = 5
  let barWidth = Math.round(
    (parentWidth - (valueCount - 1) * barSpacing) / valueCount
  )
  $('#sparkline02').sparkline(values, {
    width: '100%',
    type: type,
    height: height,
    barWidth: barWidth,
    barSpacing: barSpacing,
    barColor: '#16a085',
    negBarColor: '#FF0066'
  })

  $('#sparkline03').sparkline([5, 10, 20, 15], {
    type: 'pie',
    width: 'auto',
    height: '250px',
    sliceColors: ['#22beef', '#a2d200', '#ffc100', '#ff4a43']
  })

  let charts = $('.easypiechart .percentage')
  charts.easyPieChart({
    animate: 2000,
    onStart: (value) => {
      $('.easypiechart .percentage')
        .find('span')
        .animateNumbers(Math.floor(100 * Math.random()))
    }
  })
  window.setInterval(() => {
    charts.each((index, item) => {
      $(item)
        .data('easyPieChart')
        .update(Math.floor(100 * Math.random()))
    })
  }, 2000)
  let g01 = new JustGage({
    id: 'gauge01',
    value: 67,
    min: 0,
    max: 100,
    title: '仪表盘1',
    titleFontColor: 'rgba(255,255,255,.6)',
    valueFontColor: 'rgba(255,255,255,.8)'
  })
  let g02 = new JustGage({
    id: 'gauge02',
    value: 72,
    title: '仪表盘2',
    min: 0,
    max: 100,
    donut: true,
    levelColors: ['#85FFBD', '#6284FF', '#FC00FF', '#F76B1C'],
    titleFontColor: 'rgba(255,255,255,.6)',
    valueFontColor: 'rgba(255,255,255,.8)'
  })
  let g03 = new JustGage({
    id: 'gauge03',
    value: 92,
    title: '仪表盘3',
    min: 0,
    max: 100,
    startAnimationType: 'bounce',
    refreshAnimationType: 'bounce',
    refreshAnimationTime: 2500,
    levelColors: ['#16a085', '#FF0066'],
    titleFontColor: 'rgba(255,255,255,.6)',
    valueFontColor: 'rgba(255,255,255,.8)'
  })
  window.setInterval(() => {
    g01.refresh(getRandomInt(0, 100))
    g02.refresh(getRandomInt(0, 100))
    g03.refresh(getRandomInt(0, 100))
  }, 2000)
})
</script>


<template>
  <div>
    <div class="col-md-6">
      <header-box section_class="tile color transparent-black">
        <template v-slot:title>
          <h1>使用<strong>Easy Pie</strong>的饼图</h1>
        </template>
        <template v-slot:content>
          <div class="easypiechart inline easypiee" v-for="(item,pindex) in easypie_item_list" :key="pindex">
            <div class="percentage" :data-percent="item.percent" :data-size="item.size" :data-track-color="item.track_color" :data-bar-color="item.bar_color" :data-scale-color="item.scale_color" :data-line-cap="item.line_cap" :data-line-width="item.line_width"><span>{{item.value}}</span>%</div>
            <div class="label">{{item.content}}</div>
          </div>
        </template>
      </header-box>
    </div>
    <div class="col-md-6">
      <header-box section_class="tile color transparent-white">
        <template v-slot:title>
          <h1>使用<strong>JustGage</strong>的饼图</h1>
        </template>
        <template v-slot:content>
          <div v-for="(id,jindex) in justgage_id_list" :key="jindex" class="inline-block justgage-box" :id="id"></div>
        </template>
      </header-box>
    </div>
    <div class="col-md-12">
      <header-box section_class="tile">
        <template v-slot:title>
          <h1>使用<strong>Morris.js</strong>的图表</h1>
        </template>
        <template v-slot:content>
          <div class="row">
            <div class="col-md-3" v-for="(id,mindex) in morris_id_list" :key="mindex">
              <div :id="id" style="height: 250px;"></div>
            </div>
          </div>
        </template>
      </header-box>
      <header-box section_class="tile color transparent-black">
        <template v-slot:title>
          <h1>使用<strong>Sparkline</strong>的图表</h1>
        </template>
        <template v-slot:content>
          <div class="row">
            <div class="col-md-4 text-center" v-for="(id,sindex) in sparkline_id_list" :key="sindex">
              <span :id="id"></span>
            </div>
          </div>
        </template>
      </header-box>
    </div>
  </div>
</template>

<style scoped>
.easypiee {
  width: 110px;
  height: 142px;
  line-height: 110px;
}
.justgage-box {
  width: 180px;
  height: 165px;
}
</style>