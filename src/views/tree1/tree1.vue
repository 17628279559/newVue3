<script setup>
import P5 from 'p5'
import { onMounted } from 'vue'
import exam1 from './exam1.js'

onMounted(() => {
  const tree1 = new P5(exam1, 'p5Canvas1')
})
</script>


<template>
  <div>
    <div id="p5Canvas1"></div>
  </div>
</template>

<style scoped>
</style>