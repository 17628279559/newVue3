<script setup>
import P5 from 'p5'
import { onMounted } from 'vue'
import exam3 from './exam3.js'

onMounted(() => {
  const tree1 = new P5(exam3, 'p5Canvas3')
})
</script>

<template>
  <header-box section_class="tile color transparent-white">
    <template v-slot:title>
      <h1>我是一颗丑陋的文字的树<a href="https://p5js.org/reference/" target="_blank"><strong>(p5.js)</strong></a></h1>
    </template>
    <template v-slot:content>
      <div id="p5Canvas3"></div>
    </template>
  </header-box>

</template>

<style scoped>
a {
  color: #fff;
}
</style>