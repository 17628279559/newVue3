<script setup>
import P5 from 'p5'
import { onMounted } from 'vue'
import exam2 from './exam2.js'

onMounted(() => {
  const tree1 = new P5(exam2, 'p5Canvas2')
})
</script>

<template>
  <div id="p5Canvas2"></div>
</template>

<style scoped>
</style>