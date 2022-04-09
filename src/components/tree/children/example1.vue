<template>
  <div>
  </div>
</template>

<script>
import P5 from 'p5'

export default {
  data () {
    return {
      p5Canvas1: null
    }
  },
  created () {
    const sketch = (p5) => {
      let PI = 3.1415926
      let maxLevel = 12
      let langle, rangle, len
      let w = 800
      let h = 600

      // let w = window.innerWidth;
      // let h = window.innerHeight;

      p5.setup = () => {
        let myCanvas1 = p5.createCanvas(w, h)
        myCanvas1.parent('p5Canvas1')
        p5.noLoop()
      }

      p5.draw = () => {
        p5.background(0, 0, 0, 30)
        langle = PI / 5
        rangle = PI / 5
        len = 200
        p5.stroke(255)
        p5.translate(w / 2, h)
        p5.scale(1, -1)
        p5.translate(0, 20)
        p5.branch(1, len)
      }

      // create methods:
      p5.branch = (level, len) => {
        p5.strokeWeight(10 * Math.pow((maxLevel - level + 1) / maxLevel, 2))
        p5.line(0, 0, 0, len)
        p5.translate(0, len)
        if (len > 4) {
          p5.push()
          p5.rotate(langle)
          p5.branch(level + 1, len * 0.67)
          p5.pop()
          p5.push()
          p5.rotate(-rangle)
          p5.branch(level + 1, len * 0.67)
          p5.pop()
        }
      }
    }

    this.p5Canvas1 = new P5(sketch, 'p5Canvas1')
  },
  unmounted () {
    this.p5Canvas1 = null
  }
}
</script>

<style scoped>
canvas {
  margin: auto;
}
</style>