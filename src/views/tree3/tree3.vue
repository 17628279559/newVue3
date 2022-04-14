<script setup>
import P5 from 'p5'
import { onMounted } from 'vue'
import exam3 from './exam3.js'

onMounted(() => {
  const tree1 = new P5(exam3, 'p5Canvas3')
})
</script>

<template>
  <div id="p5Canvas3"></div>
</template>

<style scoped>
</style>