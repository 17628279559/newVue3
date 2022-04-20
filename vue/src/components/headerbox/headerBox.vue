<script setup>
const props = defineProps({
  section_class: {
    type: String,
    default: 'tile color transparent-white'
  }
})
</script>

<template>
  <section :class="section_class">
    <div class="tile-header">
      <slot name="title"></slot>
      <div class="controls">
        <a href="#" class="refresh"><i class="fa fa-refresh"></i></a>
        <a href="#" class="remove"><i class="fa fa-times"></i></a>
      </div>
    </div>
    <div class="tile-body text-center">
      <slot name="content"></slot>
    </div>
  </section>
</template>

<style scoped>
</style>