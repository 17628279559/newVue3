<script setup>
import P5 from 'p5'
import { onMounted } from 'vue'
import exam1 from './exam1.js'

onMounted(() => {
  const tree1 = new P5(exam1, 'p5Canvas1')
})
</script>


<template>
  <header-box section_class="tile color transparent-white">
    <template v-slot:title>
      <h1>我只是一颗普普通通的树<a href="https://p5js.org/reference/" target="_blank"><strong>(p5.js)</strong></a></h1>
    </template>
    <template v-slot:content>
      <div id="p5Canvas1"></div>
    </template>
  </header-box>
</template>

<style scoped>
a {
  color: #fff;
}
</style>