<script setup>
</script>

<template>
  <div id="his_message">
    <div class="meaasge-header">
      <div id="music_title">这里是标题</div>
      <div class="linediv"></div>
      <div id="music_com">这里是数量</div>
      <div id="music_pubdate">这里是时间</div>
      <div id="music_desc">这里是信息</div>
    </div>
  </div>
</template>

<style scoped>
div {
  margin: 0;
}
.meaasge-header {
  display: flex;
  flex-wrap: wrap;
  margin: 10px;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}
.linediv {
  border-bottom: 1px solid #666;
  width: 100%;
}
#his_message {
  display: flex;
  width: 200px;
  height: auto;
  position: absolute !important;
  background-color: rgba(255, 255, 255, 0.7);
  color: #222;
  border-radius: 8px !important;
  box-shadow: 0 3px 0 rgb(0 0 0 / 5%);
  display: none;
  z-index: 99;
}
#music_com {
  font-size: 0.8em;
}
#music_desc {
  font-size: 0.8em;
}
#music_pubdate {
  font-size: 0.8em;
}
</style>