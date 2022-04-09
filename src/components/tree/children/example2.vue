<template>
  <div>
    <div id="p5Canvas"></div>
  </div>
</template>

<script>
import P5 from 'p5'

export default {
  data() {
    return {
      p5Canvas: null
    }
  },
  created() {
    const sketch = (p5) => {
      let w = 800,
        h = 600
      var slider_size,
        slider_level,
        slider_rot,
        slider_lenRand,
        slider_branchProb,
        slider_rotRand,
        slider_leafProb
      var size, maxLevel, rot, lenRand, branchProb, rotRand, leafProb
      var prog = 1,
        growing = false,
        mutating = false,
        randSeed = 80,
        paramSeed = Math.floor(Math.random() * 1000),
        randBias = 0,
        PI = 3.1415926

      p5.setup = () => {
        let myCanvas = p5.createCanvas(w, h)
        myCanvas.parent('p5Canvas')
        slider_size = 125
        slider_level = 12
        slider_rot = PI / 2 / 5
        slider_lenRand = 1
        slider_branchProb = 0.92
        slider_rotRand = 0.1
        slider_leafProb = 0.5

        readInputs(false)
        startGrow()
      }

      function readInputs(updateTree) {
        size = slider_size
        maxLevel = slider_level
        rot = slider_rot
        lenRand = slider_lenRand
        branchProb = slider_branchProb
        rotRand = slider_rotRand
        leafProb = slider_leafProb

        if (updateTree && !growing) {
          prog = maxLevel + 1
          p5.loop()
        }
      }

      p5.mutate = () => {
        if (!mutating) return

        var startTime = p5.millis()
        p5.randomSeed(paramSeed)

        var n = p5.noise(startTime / 20000) - 0.5

        randBias = 4 * Math.abs(n) * n

        paramSeed = 1000 * p5.random()
        p5.randomSeed(randSeed)
        readInputs(true)

        var diff = p5.millis() - startTime

        if (diff < 20) setTimeout(p5.mutate, 20 - diff)
        else setTimeout(p5.mutate, 1)
      }

      p5.draw = () => {
        p5.stroke(255, 255, 255)
        p5.background(0, 0, 0, 0)
        p5.translate(w / 2, h)
        p5.scale(1, -1)
        p5.translate(0, 20)
        p5.branch(1, randSeed)
        p5.noLoop()
      }

      p5.branch = (level, seed) => {
        if (prog < level) return

        p5.randomSeed(seed)

        var seed1 = p5.random(1000),
          seed2 = p5.random(1000)

        var growthLevel =
          prog - level > 1 || prog >= maxLevel + 1 ? 1 : prog - level

        p5.strokeWeight(12 * Math.pow((maxLevel - level + 1) / maxLevel, 2))

        var len = growthLevel * size * (1 + rand2() * lenRand)

        p5.line(0, 0, 0, len / level)
        p5.translate(0, len / level)

        var doBranch1 = rand() < branchProb
        var doBranch2 = rand() < branchProb

        var doLeaves = rand() < leafProb

        if (level < maxLevel) {
          var r1 = rot * (1 + rrand() * rotRand)
          var r2 = -rot * (1 - rrand() * rotRand)

          if (doBranch1) {
            p5.push()
            p5.rotate(r1)
            p5.branch(level + 1, seed1)
            p5.pop()
          }
          if (doBranch2) {
            p5.push()
            p5.rotate(r2)
            p5.branch(level + 1, seed2)
            p5.pop()
          }
        }

        if ((level >= maxLevel || (!doBranch1 && !doBranch2)) && doLeaves) {
          var p = Math.min(1, Math.max(0, prog - level))

          var flowerSize = (size / 100) * p * (1 / 6) * (len / level)

          p5.strokeWeight(1)
          p5.stroke(240 + 15 * rand2(), 140 + 15 * rand2(), 140 + 15 * rand2())

          p5.rotate(-PI)
          for (var i = 0; i <= 8; i++) {
            p5.line(0, 0, 0, flowerSize * (1 + 0.5 * rand2()))
            p5.rotate((2 * PI) / 8)
          }
        }
      }

      function startGrow() {
        growing = true
        prog = 1
        grow()
      }

      function grow() {
        if (prog > maxLevel + 3) {
          prog = maxLevel + 3
          p5.loop()
          growing = false
          return
        }

        var startTime = p5.millis()
        p5.loop()
        var diff = p5.millis() - startTime

        prog += ((maxLevel / 8) * Math.max(diff, 20)) / 300
        setTimeout(grow, Math.max(1, 20 - diff))
      }

      function rand() {
        return p5.random(1000) / 1000
      }

      function rand2() {
        return p5.random(2000) / 1000 - 1
      }

      function rrand() {
        return rand2() + randBias
      }
    }

    this.p5Canvas = new P5(sketch, 'p5Canvas')
  },
  unmounted() {
    this.p5Canvas = null
  }
}
</script>

<style>
canvas {
  margin: auto;
}
span {
  color: white;
}

main {
  margin: 0 auto;
}
</style>