<template>
  <h2>赵文韬-2019302120066</h2>
  <p>本站由vue搭建</p>
  <div id="nav">
    <router-link to="/tree/example1">简单分形树(p5.js)</router-link> |
    <router-link to="/tree/example2">好看分形树(p5.js)</router-link> |
    <a href="https://code.zwt666.top/wordtree"
       target="_blank">文字树(p5.js)</a> |
    <a href="https://code.zwt666.top/histogram"
       target="_blank">动态更新的直方图(d3.js)</a> |
    <a href="https://code.zwt666.top/piechart"
       target="_blank">疫情饼图(d3.js)</a> |
    <a href="https://github.com/17628279559/tree"
       target="_blank">git仓库</a>
  </div>
  <router-view :key="$route.fullPath" />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

canvas {
  display: block;
  margin: auto;
}
h2 {
  margin: 0;
  padding: 10px;
}
#nav {
  border-top: 10px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
