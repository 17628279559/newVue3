<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue'
import { Check, PictureFilled, EditPen } from '@element-plus/icons-vue'
import * as d3 from 'd3';
import cloud from 'd3-cloud'
import Axios from 'axios'
import { Eleme } from '@element-plus/icons-vue'

const sleep = (time) => {
  return new Promise(resolve => {
    setTimeout(resolve, time)
  }
  )
}
const alert_text = ref("")
const alert_title = ref("")
const alert_make_sure = ref("")
const send_massage_to_python_message1 = ref("")
const send_massage_to_python_message2 = ref("")
const background_img = ref(0)
const background_font = ref(0)
const getWordsApi = '/api/getwords'
const getPythonWords = '/api/getpythonwords'
const { proxy } = getCurrentInstance()
const layout = cloud()
const theSize = [1000, 540]
let theWordList = [ //默认的，后面用api内容替换
  { text: 'vue', size: 20 },
  { text: 'html', size: 25 },
  { text: 'js', size: 30 },
]

const show_img = ref(false)
const send_massage_to_python = ref(false)
const textarea = ref("")
const theSvgElement = ref(null)
const background_img_choose = ref(null)
const pythonCy = ref(null)
const background_img_list = [
  { id: 0, url: "/src/assets/images/words_back/loving_heart.jpg", true_name: "loving_heart.jpg", name: "爱心" },
  { id: 1, url: "/src/assets/images/words_back/winnie_the_pooh.jpg", true_name: "winnie_the_pooh.jpg", name: "小熊维尼" },
  { id: 2, url: "/src/assets/images/words_back/apple.png", true_name: "apple.png", name: "苹果logo" },
]
const background_font_list = [
  { id: 0, url: "/src/assets/images/fontimg/dnxdcbz.png", true_name: "dnxdcbz.ttf", name: "对你心动藏不住" },
  { id: 1, url: "/src/assets/images/fontimg/fzgsdxhh.png", true_name: "fzgsdxhh.ttf", name: "方正故事的小黄花" },
  { id: 2, url: "/src/assets/images/fontimg/nswddrnc.png", true_name: "nswddrnc.ttf", name: "你是我的冬日奶茶" },
  { id: 3, url: "/src/assets/images/fontimg/wdkaymgd.png", true_name: "wdkaymgd.ttf", name: "我的可爱有目共睹" },
  { id: 4, url: "/src/assets/images/fontimg/zsxhhbsa.png", true_name: "zsxhhbsa.ttf", name: "只是喜欢何必说爱" },
  { id: 5, url: "/src/assets/images/fontimg/ppttwryh.png", true_name: "ppttwryh.ttf", name: "普普通通微软雅黑" },
]
const dialogVisible = ref(false)
const select_back_img = ref(false)
const select_back_font = ref(false)
const draw = (words) => {
  let color = d3.scaleOrdinal(d3.schemeCategory10);
  d3.select(theSvgElement.value)
    .append("svg")
    .attr("width", layout.size()[0])
    .attr("height", layout.size()[1])
    .append("g")
    .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
    .selectAll("text")
    .data(words)
    .enter().append("text")
    .style("font-size", function (d) { return d.size + "px"; })
    .style("font-family", "Impact")
    .style("cursor", "pointer")
    .style("fill", function (d, i) { return color(i); })
    .attr("text-anchor", "middle")
    .attr("transform", function (d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
    .text(function (d) { return d.text; })
    // 添加点击的回调方法
    .on("mouseover", (index, item) => {
      d3.select(index.target)
        .transition()
        .duration(100)
        .style('opacity', 0.7)
        .style('font-size', item.size + 20 + 'px')
    })
    .on("mouseout", (index, item) => {
      d3.select(index.target)
        .transition()
        .duration(100)
        .style('opacity', 1)
        .style('font-size', item.size + 'px')
    });
}

const submit = () => {
  send_massage_to_python.value = false
  if (textarea.value.length < 20) {
    alert_title.value = "(╬◣д◢)"
    alert_text.value = `${textarea.value.length}个字，来搞笑吗，还想生成词云图`
    alert_make_sure.value = "我错了"
    dialogVisible.value = true
  }
  else if (textarea.value.length < 100) {
    alert_title.value = "￣へ￣"
    alert_text.value = `才${textarea.value.length}个字，这么点字够谁用？让隔壁计科看见还以为我们没文化呢,给我写够200字`
    alert_make_sure.value = "好的好的我再写点"
    dialogVisible.value = true
  }
  else if (textarea.value.length < 200) {
    alert_title.value = "〒▽〒"
    alert_text.value = `${textarea.value.length}个字啦，加油加油，再写点`
    alert_make_sure.value = "好的好的我再写点"
    dialogVisible.value = true
  } else {
    $("#loader").fadeIn(300);
    $(".mask").fadeIn(300)
    let data = new FormData()
    data.append('text', textarea.value)
    data.append('background_img', background_img_list[background_img.value].true_name)
    data.append('font_style', background_font_list[background_font.value].true_name)
    Axios.post(getPythonWords, data).then((response) => {
      show_img.value = true
      $(pythonCy.value).attr('src', response.data.name)
      $("#loader").fadeOut(300);
      $(".mask").fadeOut(300)
    })
  }
}

const send_massage_to_python_check = () => {
  send_massage_to_python.value = true
  send_massage_to_python_message1.value = `当前背景图片：${background_img_list[background_img.value].name}`
  send_massage_to_python_message2.value = `当前字体样式：${background_font_list[background_font.value].name}`
}

const select_back_img_make_sure = () => {
  select_back_img.value = false
  for (let i = 0; i < background_img_list.length; i++) {
    if ($(`#background_img_choose_${i}`).parent().css('transform') == "matrix(1, 0, 0, 1, 0, 0)") {
      background_img.value = i
    }
  }
}
const select_back_font_make_sure = () => {
  select_back_font.value = false
  for (let i = 0; i < background_font_list.length; i++) {
    if ($(`#background_font_choose_${i}`).parent().css('transform') == "matrix(1, 0, 0, 1, 0, 0)") {
      background_font.value = i
    }
  }
}

onMounted(() => {
  Axios.get(getWordsApi).then((response) => {
    theWordList = response.data
    layout
      .size(theSize)
      .words(theWordList)
      .padding(5)
      .rotate(function () { return ~~(Math.random() * 3) * 30; })
      .font("Impact")
      .fontSize(function (d) { return d.size; })
      .on("end", draw)
    layout.start()
  })
})

</script>

<template>
  <div>
    <header-box :style="{'display':!proxy.$wordCloudPython.show ? 'block':'none'}" section_class="tile color transparent-black">
      <template v-slot:title>
        <h1><a href="http://www.93.gov.cn/bsjs-ldcy-zxfzx-cbfzx-wdjh/768551.html" target="_blank"><strong>全国人大十三届五次全会精神文稿</strong></a>词云图</h1>
      </template>
      <template v-slot:content>
        <div ref="theSvgElement"></div>
      </template>
    </header-box>
    <header-box :style="{'display':proxy.$wordCloudPython.show ? 'block':'none'}" section_class="tile color transparent-black">
      <template v-slot:title>
        <h1>基于python的<a href="https://github.com/amueller/word_cloud" target="_blank"><strong>wordCloud</strong></a>的词云图</h1>
      </template>
      <template v-slot:content>
        <el-input style="width:1200px;margin:20px" v-model="textarea" :autosize="{ minRows: 3, maxRows: 999 }" type="textarea" placeholder="请输入你想进行词云生成的文字（字数越多越好，建议400字以上,英文的话加空格才算一个单词哦）" />
        <div style="display:flex;justify-content:flex-end;margin:0px 30px">
          <el-button type="primary" size="large" :icon="EditPen" circle @click="select_back_font = true" />
          <el-button type="primary" size="large" :icon="PictureFilled" circle @click="select_back_img = true" />
          <el-button type="success" size="large" :icon="Check" circle @click="send_massage_to_python_check" />
        </div>
        <img v-show="show_img" ref="pythonCy" style="width:1200px;height:auto;margin:20px" src="" />
        <el-empty v-show="!show_img" description="快快输入文字测试一下吧~" />
      </template>
    </header-box>
    <el-dialog v-model="dialogVisible" :title="alert_title" width="30%">
      <span>{{alert_text}}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">{{alert_make_sure}}</el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog v-model="select_back_img" title="选择背景图片" width="25%">
      <el-carousel :autoplay="false" height="100px">
        <el-carousel-item v-for="(item,index) in background_img_list" :key="index">
          <div :id="`background_img_choose_${item.id}`" style="width:100%;display:flex;justify-content:center">
            <el-image style="width: 150px; height: 100px;" :src="item.url" fit="scale-down" />
          </div>
        </el-carousel-item>
      </el-carousel>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="select_back_img_make_sure">确定</el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog v-model="select_back_font" title="选择字体" width="25%">
      <el-carousel :autoplay="false" height="80px">
        <el-carousel-item v-for="(item,index) in background_font_list" :key="index">
          <div :id="`background_font_choose_${item.id}`" style="width:100%;display:flex;justify-content:center">
            <el-image style="width: 150px; height: 100px;" :src="item.url" fit="scale-down" />
          </div>
        </el-carousel-item>
      </el-carousel>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="select_back_font_make_sure">确定</el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog v-model="send_massage_to_python" title="确定好了吗？" width="30%">
      <div>{{send_massage_to_python_message1}}</div>
      <div>{{send_massage_to_python_message2}}</div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="submit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
a {
  color: #fff;
}
</style>