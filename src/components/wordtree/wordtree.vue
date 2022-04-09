<template>
  <div class="container">
    <div class="p5Canvas"></div>
  </div>
</template>

<script>
import P5 from 'p5';

export default {
  data () {
    return {
      p5Canvas: null,
    }
  },
  created () {
    const sketch = p5 => {
      let lsilder, rsilder, len_slider, button_seed, label, lo = true;
      let PI = 3.1415926;
      let maxLevel = 12;
      let r = 250;
      let rot = PI / 10;
      let langle, rangle, len, i = 0;
      let w = window.innerWidth;
      let h = window.innerHeight;
      let randBias;
      let words = ["苦心竭力", "慷慨激昂", "勉力", "勃然奋励", "悬梁刺股孜", "竭力", "闻起舞", "精诚至", "奋勉", "破釜沉舟"]

      words.sort(function () { return 0.5 - Math.random() })
      // let w = window.innerWidth;
      // let h = window.innerHeight;

      p5.setup = () => {
        p5.createCanvas(w, h);
        lsilder = p5.createSlider(0, PI, PI / 5, 0.01);
        lsilder.position(40, 60);
        rsilder = p5.createSlider(0, PI, PI / 5, 0.01);
        rsilder.position(40, 85);
        len_slider = p5.createSlider(150, 250, 180, 1);
        len_slider.position(40, 110);
        button_seed = p5.createButton('loop');
        button_seed.position(40, 140);

        label = p5.createSpan('赵文韬-2019302120066');
        label.position(w / 2 - 150, 50);

        let startTime = p5.millis();
        let n = p5.noise(startTime / 20000) - 0.5;
        randBias = 4 * Math.abs(n) * n;

        button_seed.mousePressed(function () {
          if (lo) {
            p5.noLoop();
            lo = false;
          }
          else {
            startTime = p5.millis();
            n = p5.noise(startTime / 20000) - 0.5;
            randBias = 4 * Math.abs(n) * n;
            p5.loop();
            lo = true;
          }
        });
      };

      p5.draw = () => {
        p5.background(189, 193, 255);
        langle = lsilder.value();
        rangle = rsilder.value();
        len = len_slider.value();
        p5.stroke(255);
        p5.translate(w / 2, h);
        p5.scale(1, -1);
        p5.translate(0, 25);
        p5.branch(1, len, 0);
      };

      // create methods:
      p5.branch = (level, len) => {
        i = Math.floor(Math.random() * 9);
        let words_len = words[i].length
        let textSize = 32 * Math.pow((maxLevel - level + 1) / maxLevel, 2)
        let strokeWeight = 10 * Math.pow((maxLevel - level + 1) / maxLevel, 2)
        p5.rotate(PI / 2)
        p5.strokeWeight(strokeWeight);
        p5.textSize(textSize);
        p5.noStroke();
        r = 255 - 4 * len;
        p5.fill(150, r, 190);
        p5.text(words[i], 0, 0);

        p5.translate((words_len + 0.5) * textSize, 0);





        if (len > 10) {
          let r1 = rot * (1 + rrand() * rangle) - PI / 2;
          let r2 = -rot * (1 - rrand() * langle) - PI / 2;
          p5.push();
          p5.rotate(r1);
          p5.branch(level + 1, len * 0.67);
          p5.pop();
          p5.push();
          p5.rotate(r2);
          p5.branch(level + 1, len * 0.67);
          p5.pop();
        }
      }
      function rand2 () { return p5.random(2000) / 1000 - 1; }

      function rrand () {
        return rand2() + randBias;
      }
    }

    this.p5Canvas = new P5(sketch, 'p5Canvas');
  },
  unmounted () {
    this.p5Canvas = null;
  },
}
</script>

<style>
span {
  font-size: 30px;
  color: white;
  font-weight: bold;
}
</style>