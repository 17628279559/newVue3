<script setup>
import P5 from 'p5'
import { onMounted } from 'vue'
import exam2 from './exam2.js'

onMounted(() => {
  const tree1 = new P5(exam2, 'p5Canvas2')
})
</script>

<template>
  <header-box section_class="tile color transparent-white">
    <template v-slot:title>
      <h1>我是一颗好看的树<a style="color:#FFF" href="https://p5js.org/reference/" target="_blank"><strong>(p5.js)</strong></a></h1>
    </template>
    <template v-slot:content>
      <div id="p5Canvas2"></div>
    </template>
  </header-box>
</template>

<style scoped>
</style>