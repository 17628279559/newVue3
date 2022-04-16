<script setup>
import { onMounted } from 'vue'
import echartExample1 from '../../components/echart/echart1.vue'
import echartExample2 from '../../components/echart/echart2.vue'

const morris_item_list = [
  { id: 'morris-line-example', content: '中日韩1980-2020人均GDP增速对比', url: "https://www.kylc.com/stats/global/yearly_per_country/g_gdp_per_capita/chn-jpn-kor.html" },
  { id: 'morris-line-area-example', content: '中日韩1980-2020总GDP增速对比', url: "https://www.kylc.com/stats/global/yearly_per_country/g_gdp/chn-jpn-kor.html" },
  { id: 'morris-bar-example', content: '中日韩2004-2020年制造业增加值', url: "https://www.kylc.com/stats/global/yearly_per_country/g_industry_value_added/chn-jpn-kor.html" },
  { id: 'morris-donut-example', content: '中日韩2020年人口统计', url: "https://www.kylc.com/stats/global/yearly_per_country/g_population_total/chn-jpn-kor.html" }
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
    content: '仪表盘1'
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
    content: '仪表盘2'
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
    content: '仪表盘3'
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
      { y: '1980', a: 194, b: 9463, c: 1715 },
      { y: '1984', a: 250, b: 10978, c: 2413 },
      { y: '1988', a: 283, b: 25059, c: 4748 },
      { y: '1992', a: 366, b: 31414, c: 8126 },
      { y: '1996', a: 709, b: 39150, c: 13403 },
      { y: '2000', a: 959, b: 39169, c: 12256 },
      { y: '2004', a: 1508, b: 38298, c: 16496 },
      { y: '2008', a: 3468, b: 39876, c: 21350 },
      { y: '2012', a: 6300, b: 49145, c: 25466 },
      { y: '2016', a: 8094, b: 39400, c: 29288 },
      { y: '2020', a: 10434, b: 40193, c: 31631 },
    ],
    xkey: 'y',
    ykeys: ['a', 'b', 'c'],
    hideHover: 'auto',
    preUnits: '$',
    labels: ['中国人均GDP(美元)', '日本人均GDP(美元)', '韩国人均GDP(美元)'],
    lineColors: ['#d9544f', '#1693A5', '#ffc100']
  })
  Morris.Area({
    element: 'morris-line-area-example',
    data: [
      { y: '1980', a: 191149211575, b: 1105385973763, c: 65398646757 },
      { y: '1984', a: 259946510957, b: 1318381627003, c: 97510235986 },
      { y: '1988', a: 312353631207, b: 3071683013178, c: 199590823957 },
      { y: '1992', a: 426915712715, b: 3908809463463, c: 355525267405 },
      { y: '1996', a: 863746717507, b: 4923391533851, c: 610169556840 },
      { y: '2000', a: 1211346869600, b: 4968359075956, c: 576178114168 },
      { y: '2004', a: 1955347004965, b: 4893116005656, c: 793175007858 },
      { y: '2008', a: 4594307032667, b: 5106679115127, c: 1047339010225 },
      { y: '2012', a: 8532229986993, b: 6272362996105, c: 1278427634342 },
      { y: '2016', a: 11233276536744, b: 5003677627544, c: 1500111596236 },
      { y: '2020', a: 14722730697890, b: 5057758958706, c: 1637895802792 },
    ],
    xkey: 'y',
    ykeys: ['a', 'b', 'c'],
    ymax: 15000000000000,
    labels: ['中国总GDP(美元)', '日本总GDP(美元)', '韩国总GDP(美元)'],
    lineColors: ['#d9544f', '#1693A5', '#ffc100'],
    lineWidth: '0',
    preUnits: '$',
    hideHover: 'auto',
    fillOpacity: '0.5',
    behaveLikeLine: true,
  })
  Morris.Bar({
    element: 'morris-bar-example',
    data: [
      { y: '2004', a: 625223572999, b: 1033455029438, c: 207164722522 },
      { y: '2008', a: 1475664386144, b: 1086396509271, c: 268350787675 },
      { y: '2012', a: 2690090775153, b: 1233567341928, c: 355810643294 },
      { y: '2016', a: 3153118068885, b: 1015148046907, c: 395395892603 },
      { y: '2020', a: 3853808254115, b: 0, c: 406373293202 }
    ],
    xkey: 'y',
    ykeys: ['a', 'b', 'c'],
    hideHover: 'auto',
    preUnits: '$',
    labels: ['中国年制造业增加值(美元)', '日本年制造业增加值(美元)', '韩国年制造业增加值(美元)'],
    barColors: ['#d9544f', '#1693A5', '#ffc100'],
  })
  Morris.Donut({
    element: 'morris-donut-example',
    data: [
      { label: "中国总人口", value: 1410929362 },
      { label: "日本总人口", value: 125836021 },
      { label: "韩国总人口", value: 51780579 }
    ],
    colors: ['#d9544f', '#1693A5', '#ffc100'],
  });

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
          <h1>使用<a style="color:#FFF" href="http://rendro.github.io/easy-pie-chart/" target="_blank"><strong>EasyPie</strong></a>的仪表盘</h1>
        </template>
        <template v-slot:content>
          <div class="easypiechart inline easypiee" v-for="(item,p_index) in easypie_item_list" :key="p_index">
            <div class="percentage" :data-percent="item.percent" :data-size="item.size" :data-track-color="item.track_color" :data-bar-color="item.bar_color" :data-scale-color="item.scale_color" :data-line-cap="item.line_cap" :data-line-width="item.line_width"><span>{{item.value}}</span>%</div>
            <div class="label">{{item.content}}</div>
          </div>
        </template>
      </header-box>
    </div>
    <div class="col-md-6">
      <header-box section_class="tile color transparent-white">
        <template v-slot:title>
          <h1>使用<a style="color:#FFF" href="https://github.com/toorshia/justgage" target="_blank"><strong>JustGage</strong></a>的仪表盘</h1>
        </template>
        <template v-slot:content>
          <div v-for="(id,j_index) in justgage_id_list" :key="j_index" class="inline-block justgage-box" :id="id"></div>
        </template>
      </header-box>
    </div>
    <div class="col-md-12">
      <header-box section_class="tile color transparent-black">
        <template v-slot:title>
          <h1>使用<a style="color:#FFF" href="https://morrisjs.github.io/morris.js/" target="_blank"><strong>Morris</strong></a>的中日韩数据对比图</h1>
        </template>
        <template v-slot:content>
          <div class="row">
            <div class="col-md-6" v-for="(item,m_index) in morris_item_list" :key="m_index">
              <h3><a style="color:#FFF" :href="item.url" target="_blank">{{item.content}}</a></h3>
              <div :id="item.id" class="morris-chart" style="height: 250px;"></div>
              <ul v-if="item.id === 'morris-donut-example'" class="inline text-center chart-legend">
                <li><span class="badge badge-outline" style="border-color: #d9544f"></span> 中国总人口 <small>18.18%</small></li>
                <li><span class="badge badge-outline" style="border-color: #1693A5"></span> 日本总人口 <small>1.62%</small></li>
                <li><span class="badge badge-outline" style="border-color: #ffc100"></span> 韩国总人口 <small>0.67%</small></li>
              </ul>
            </div>
          </div>
        </template>
      </header-box>
      <header-box section_class="tile color transparent-white">
        <template v-slot:title>
          <h1>使用<a style="color:#FFF" href="https://omnipotent.net/jquery.sparkline/#s-docs" target="_blank"><strong>Sparkline</strong></a>的各种图表</h1>
        </template>
        <template v-slot:content>
          <div class="row">
            <div class="col-md-4 text-center" v-for="(id,s_index) in sparkline_id_list" :key="s_index">
              <span :id="id"></span>
            </div>
          </div>
        </template>
      </header-box>
      <header-box section_class="tile color transparent-black">
        <template v-slot:title>
          <h1>使用<a style="color:#FFF" href="https://echarts.apache.org/" target="_blank"><strong>Echarts</strong></a>的饼图(搬移的)</h1>
        </template>
        <template v-slot:content>
          <echart-example1></echart-example1>
        </template>
      </header-box>
      <header-box section_class="tile color transparent-white">
        <template v-slot:title>
          <h1>使用<a style="color:#FFF" href="https://echarts.apache.org/" target="_blank"><strong>Echarts</strong></a>的k线图(福田汽车)</h1>
        </template>
        <template v-slot:content>
          <echart-example2></echart-example2>
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