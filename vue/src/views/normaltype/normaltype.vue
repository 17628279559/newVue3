<script setup>
import { ref } from 'vue'
import { Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import Axios from 'axios'


const sleep = (time) => {
  return new Promise((resolve) => setTimeout(resolve, time));
}
//数据区域
const getDFAapi = "/api/getDFA"
const image_is_null = ref(true)
const python_alert_show = ref(false)
const python_image_element = ref(null)
const python_input_textarea = ref("")
const send_massage_to_python_message = ref("")
//函数区域


const send_massage_to_python_and_get_img_url = () => {  //提交信息到服务器并返回图片链接 （同时也是确认选择的按钮的确认事件）
  $("#loader").fadeIn(300);
  $(".mask").fadeIn(300)
  let data = new FormData()

  Axios.get(getDFAapi + `?normaltype=${python_input_textarea.value}`, data).then((response) => {
    let name = response.data.name
    python_alert_show.value = false
    if (name == "extra words") {
      ElMessage({
        message: response.data.wrong,
        type: 'error',
      })

    }
    else {
      $(python_image_element.value).attr('src', name)
      image_is_null.value = false
    }
    $("#loader").fadeOut(300);
    $(".mask").fadeOut(300)
  })
}
const send_massage_to_python_check = () => { //确认选择的按钮的点击事件
  python_alert_show.value = true
  send_massage_to_python_message.value = `您输入的正规式为:${python_input_textarea.value}`
}


</script>

<template>
  <div>
    <header-box section_class="tile color transparent-white">
      <template v-slot:title>
        <h1>python算法之正规式转NFA转DFA转最小化DFA</h1>
      </template>
      <template v-slot:content>
        <el-input style="width:1200px;margin:20px" v-model="python_input_textarea" :autosize="{ minRows: 3, maxRows: 999 }" type="textarea" placeholder="正规式转NFA转DFA转最小化DFA,请输入不含有“+”的正规式,例如“a(b*|c)|(abc*)”,节点请输入a-n的任意小写字符" />
        <div style="display:flex;justify-content:flex-end;margin:0px 80px">
          <el-button type="success" size="large" :icon="Check" circle @click="send_massage_to_python_check" />
        </div>
        <img v-show="!image_is_null" ref="python_image_element" style="width:600px;height:auto;margin:0 auto" src="" />
        <el-empty v-show="image_is_null" description="快快输入正规式测试一下吧~" />
      </template>
    </header-box>
    <el-dialog v-model="python_alert_show" title="确定好了吗？" width="30%">
      <div>{{send_massage_to_python_message}}</div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="send_massage_to_python_and_get_img_url">确定</el-button>
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