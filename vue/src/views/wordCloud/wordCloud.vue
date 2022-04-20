<script setup>
import { onMounted, ref, getCurrentInstance } from 'vue'
import { Check, PictureFilled, EditPen, MostlyCloudy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import * as d3 from 'd3';
import cloud from 'd3-cloud'
import Axios from 'axios'

const { proxy } = getCurrentInstance() //以proxy形式获取全局变量
const layout = cloud() //d3.layout.cloud.js

const sleep = (time) => {
  return new Promise((resolve) => setTimeout(resolve, time));
}
//数据区域

const python_background_img_list = [  //python词云的背景图选择项
  { id: 0, url: "/src/assets/images/words_back/loving_heart.jpg", true_name: "loving_heart.jpg", name: "爱心" },
  { id: 1, url: "/src/assets/images/words_back/winnie_the_pooh.jpg", true_name: "winnie_the_pooh.jpg", name: "小熊维尼" },
  { id: 2, url: "/src/assets/images/words_back/apple.png", true_name: "apple.png", name: "苹果logo" },
  { id: 3, url: "/src/assets/images/words_back/girl.png", true_name: "girl.png", name: "追兔子的女孩" },
]
const python_background_font_list = [ //python词云的字体选择项
  { id: 0, url: "/src/assets/images/fontimg/dnxdcbz.png", true_name: "dnxdcbz.ttf", name: "对你心动藏不住" },
  { id: 1, url: "/src/assets/images/fontimg/fzgsdxhh.png", true_name: "fzgsdxhh.ttf", name: "方正故事的小黄花" },
  { id: 2, url: "/src/assets/images/fontimg/nswddrnc.png", true_name: "nswddrnc.ttf", name: "你是我的冬日奶茶" },
  { id: 3, url: "/src/assets/images/fontimg/wdkaymgd.png", true_name: "wdkaymgd.ttf", name: "我的可爱有目共睹" },
  { id: 4, url: "/src/assets/images/fontimg/zsxhhbsa.png", true_name: "zsxhhbsa.ttf", name: "只是喜欢何必说爱" },
  { id: 5, url: "/src/assets/images/fontimg/ppttwryh.png", true_name: "ppttwryh.ttf", name: "普普通通微软雅黑" },
]

const d3_svg_element = ref(null) //d3词云图的DOM元素
const python_image_element = ref(null) //python词云图image的DOM元素
const python_input_textarea = ref("") //python词云图输入的文本框内容
const python_alert1_text = ref("")  //检查输入框是否满足字数要求的弹窗  的中间文字内容
const python_alert1_title = ref("") //检查输入框是否满足字数要求的弹窗  的题目文字内容
const python_alert1_makeSure = ref("") //检查输入框是否满足字数要求的弹窗  的确认按钮文字内容
const send_massage_to_python_message1 = ref("") //点击确认的弹窗 的背景确认的文字内容
const send_massage_to_python_message2 = ref("") //点击确认的弹窗 的字体确认的文字内容
const send_massage_to_python_message3 = ref("") //点击确认的弹窗 的字体确认的文字内容
const python_selected_background_img = ref(0) //选择的背景图的index（对应上方python_background_img_list）
const python_selected_background_font = ref(0) //选择的字体样式的index（对应上方python_background_font_list）
const python_is_transparent = ref("False")
const python_background_color = ref("#FFFFFF")
const image_is_null = ref(true)  // 图片是否为空（是否生成图片）
const python_alert1_show = ref(false)  //检查输入框是否满足字数要求的弹窗 是否显示
const python_alert2_show = ref(false)  //选择背景图片的弹窗 是否显示
const python_alert3_show = ref(false)  //选择字体样式的弹窗 是否显示
const python_alert4_show = ref(false)  //发送内容到服务器的确认信息的弹窗 是否显示
const get_jieba_cut_word_List_api = '/api/getwords'  //获取d3词云图的词语列表统计信息
const get_python_jieba_cut_word_List_api = '/api/getpythonwords'  //获取python词云图的词云图url（前端发送文字，字体，背景，后端生成图片且返回url路径）
const word_cloud_color = d3.scaleOrdinal(d3.schemeCategory10);  //d3词云图颜色信息
//函数区域
const draw = (words) => {  //画词云图函数
  d3.select(d3_svg_element.value)
    .append("svg")
    .attr("width", layout.size()[0])
    .attr("height", layout.size()[1])
    .style("background-color", "#FFFFFF")
    .append("g")
    .attr("transform", `translate(${layout.size()[0] / 2},${layout.size()[1] / 2})`)
    .selectAll("text")
    .data(words)
    .enter().append("text")
    .style("font-size", (item) => item.size + "px")
    .style("font-family", "dnxdcbz")
    .style("cursor", "pointer")
    .style("fill", (item, index) => word_cloud_color(index))
    .attr("text-anchor", "middle")
    .attr("transform", item => `translate(${item.x},${item.y}) rotate(${item.rotate})`)
    .text(item => item.text)
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
const change_python_alert1 = (title, text, makeSure) => { //改变不同字数弹出的提示
  python_alert1_title.value = title
  python_alert1_text.value = text
  python_alert1_makeSure.value = makeSure
  python_alert1_show.value = true
}
const send_massage_to_python_and_get_img_url = () => {  //提交信息到服务器并返回图片链接 （同时也是确认选择的按钮的确认事件）
  $("#loader").fadeIn(300);
  $(".mask").fadeIn(300)
  let data = new FormData()
  data.append('text', python_input_textarea.value)
  data.append('background_img', python_background_img_list[python_selected_background_img.value].true_name)
  data.append('font_style', python_background_font_list[python_selected_background_font.value].true_name)
  data.append('is_transparent', python_is_transparent.value)
  Axios.post(get_python_jieba_cut_word_List_api, data).then((response) => {
    image_is_null.value = false
    $(python_image_element.value).attr('src', response.data.name)
    $("#loader").fadeOut(300);
    $(".mask").fadeOut(300)
  })
}
const submit = () => {  //检查字数是否满足要求
  python_alert4_show.value = false
  if (python_input_textarea.value.length < 20) {
    change_python_alert1("(╬◣д◢)", `${python_input_textarea.value.length}个字，来搞笑吗，还想生成词云图`, "我错了")
  }
  else if (python_input_textarea.value.length < 100) {
    change_python_alert1("￣へ￣", `才${python_input_textarea.value.length}个字，这么点字够谁用？让隔壁计科看见还以为我们没文化呢,给我写够200字`, "好的好的我再写点")
  }
  else if (python_input_textarea.value.length < 200) {
    change_python_alert1("〒▽〒", `${python_input_textarea.value.length}个字啦，加油加油，再写点`, "没问题")
  } else {
    send_massage_to_python_and_get_img_url()
  }
}
const send_massage_to_python_check = () => { //确认选择的按钮的点击事件
  python_alert4_show.value = true
  send_massage_to_python_message1.value = `当前背景图片：${python_background_img_list[python_selected_background_img.value].name}`
  send_massage_to_python_message2.value = `当前字体样式：${python_background_font_list[python_selected_background_font.value].name}`
  send_massage_to_python_message3.value = `当前背景颜色：${python_is_transparent.value == "True" ? "透明" : "白色"}`
}
const select_back_img_make_sure = () => {  //切换图片按钮的确认事件
  python_alert2_show.value = false
  for (let i = 0; i < python_background_img_list.length; i++) {
    if ($(`#background_img_choose_${i}`).parent().css('transform') == "matrix(1, 0, 0, 1, 0, 0)") {
      python_selected_background_img.value = i
    }
  }
}
const select_back_font_make_sure = () => {  //切换字体按钮的确认事件
  python_alert3_show.value = false
  for (let i = 0; i < python_background_font_list.length; i++) {
    if ($(`#background_font_choose_${i}`).parent().css('transform') == "matrix(1, 0, 0, 1, 0, 0)") {
      python_selected_background_font.value = i
    }
  }
}
const switch_background = () => {
  if (python_is_transparent.value == "False") {
    python_is_transparent.value = "True"
    python_background_color.value = "rgba(0,0,0,0)"
    ElMessage({
      message: '现在会生成透明背景哦！'
    })
  }
  else {
    python_is_transparent.value = "False"
    python_background_color.value = "#FFFFFF"
    ElMessage({
      message: '现在会生成白色背景哦！',
      type: 'success',
    })
  }
}
//生命周期函数
onMounted(() => {
  Axios.get(get_jieba_cut_word_List_api).then((response) => {
    let jieba_cut_word_List = response.data
    layout
      .size([1000, 540])
      .words(jieba_cut_word_List.map(item => {
        return { text: item.text, size: item.size * 1.8 }
      }))
      .padding(5)
      .rotate(() => ~~(Math.random() * 3) * 30)
      .font("Impact")
      .fontSize((item) => item.size)
      .on("end", draw)
    layout.start()
  })
})

</script>

<template>
  <div>
    <header-box v-show="!proxy.$wordCloudPython.show" section_class="tile color transparent-black">
      <template v-slot:title>
        <h1><a href="http://www.93.gov.cn/bsjs-ldcy-zxfzx-cbfzx-wdjh/768551.html" target="_blank"><strong>全国人大十三届五次全会精神文稿</strong></a>词云图</h1>
      </template>
      <template v-slot:content>
        <div ref="d3_svg_element"></div>
      </template>
    </header-box>
    <header-box v-show="proxy.$wordCloudPython.show" section_class="tile color transparent-black">
      <template v-slot:title>
        <h1>基于python的<a href="http://amueller.github.io/word_cloud/references.html" target="_blank"><strong>wordCloud</strong></a>的词云图</h1>
      </template>
      <template v-slot:content>
        <el-input style="width:1200px;margin:20px" v-model="python_input_textarea" :autosize="{ minRows: 3, maxRows: 999 }" type="textarea" placeholder="请输入你想进行词云生成的一段文字文字（建议400字以上）,可以点击云生成透明的背景，点完之后图标会变透明，但是它还在编辑字体样式旁边" />
        <div style="display:flex;justify-content:flex-end;margin:0px 30px">
          <el-button :color="python_background_color" size="large" :icon="MostlyCloudy" circle @click="switch_background" />
          <el-button type="primary" size="large" :icon="EditPen" circle @click="python_alert3_show = true" />
          <el-button type="primary" size="large" :icon="PictureFilled" circle @click="python_alert2_show = true" />
          <el-button type="success" size="large" :icon="Check" circle @click="send_massage_to_python_check" />
        </div>
        <img v-show="!image_is_null" ref="python_image_element" style="width:1200px;height:auto;margin:20px" src="" />
        <el-empty v-show="image_is_null" description="快快输入文字测试一下吧~" />
      </template>
    </header-box>
    <el-dialog v-model="python_alert1_show" :title="python_alert1_title" width="30%">
      <span>{{python_alert1_text}}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="python_alert1_show = false">{{python_alert1_makeSure}}</el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog v-model="python_alert2_show" title="选择背景图片" width="25%">
      <el-carousel :autoplay="false" height="100px">
        <el-carousel-item v-for="(item,index) in python_background_img_list" :key="index">
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
    <el-dialog v-model="python_alert3_show" title="选择字体" width="25%">
      <el-carousel :autoplay="false" height="80px">
        <el-carousel-item v-for="(item,index) in python_background_font_list" :key="index">
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
    <el-dialog v-model="python_alert4_show" title="确定好了吗？" width="30%">
      <div>{{send_massage_to_python_message1}}</div>
      <div>{{send_massage_to_python_message2}}</div>
      <div>{{send_massage_to_python_message3}}</div>
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