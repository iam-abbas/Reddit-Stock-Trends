<template>
  <div>
    <div class="container">
      <div class="row justify-content-md-center mt-5">
        <div class="col-md-auto">
          <avatar
            size="xlarge"
            :image="require('@/assets/logo.png')"
            shape="circle" />
        </div>
      </div>

      <div class="noHeight">
        <button class="floatLeft"
                @click="prev"
                :disabled="currPage == 1">
          prev
        </button>
        <button class="floatRight"
                @click="next"
                :disabled="bestTicks.state.listLength < pageSize">
          next
        </button>
      </div>

      <table class="table mt-5">
        <thead>
          <tr>
            <th scope="col">Ticker</th>
            <th scope="col">Mentions</th>
            <th scope="col">Name</th>
            <th scope="col">Industry</th>
            <th scope="col">Previous Close</th>
            <th scope="col">5d Low</th>
            <th scope="col">5d High</th>
            <th scope="col">1d Change</th>
            <th scope="col">5d Change</th>
            <th scope="col">1mo Change</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(tData, index) in bestTicks.state.list" :key="index">
            <td>{{tData.Ticker}}</td>
            <td>{{tData.Mentions}}</td>
            <td>{{tData.Name}}</td>
            <td>{{tData.Industry}}</td>
            <td>${{tData.PreviousClose}}</td>
            <td>${{tData.Low5d}}</td>
            <td>${{tData.High5d}}</td>
            <td v-bind:class="getTextColor(tData.ChangePercent1d)">
              {{tData.ChangePercent1d}}%
            </td>
            <td v-bind:class="getTextColor(tData.ChangePercent5d)">
              {{tData.ChangePercent5d}}%
            </td>
            <td v-bind:class="getTextColor(tData.ChangePercent1mo)">
              {{tData.ChangePercent1mo}}%
            </td>
          </tr>
        </tbody>
        <tbody>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import Avatar from 'primevue/avatar';
import { Options, Vue, setup } from 'vue-class-component';
import { useArtists } from '../composables/use-ticks';

@Options({
  components: {
    Avatar,
  },
})
export default class App extends Vue {
  currPage = 1;

  pageSize = 10;

  bestTicks = setup(() => useArtists());

  created() {
    this.bestTicks.get(this.currPage);
  }

  next() {
    this.bestTicks.get(this.currPage += 1);
  }

  prev() {
    this.currPage -= 1;
    if (this.currPage < 1) {
      this.currPage = 1;
    }
    this.bestTicks.get(this.currPage);
  }

  getTextColor(val: number) {
    return {
      greenX: val >= 250,
      greenH: val < 250 && val >= 100,
      greenM: val < 100 && val >= 50,
      greenL: val < 50 && val > 0,
      redL: val <= 0 && val > -50,
      redM: val <= -50 && val > -100,
      redH: val <= -100 && val > -250,
      redX: val < -250,
    };
  }
}
</script>

<style lang="scss">
.p-avatar-circle {
  overflow: hidden;
}

table {
  color: var(--text-color) !important;
}
table>:not(:last-child)>:last-child>* {
    border-bottom-color: inherit !important;
}

button {
  border: 1px solid #0066cc;
  background-color: #0099cc;
  color: #ffffff;
  padding: 5px 10px;
}

button:hover {
  border: 1px solid #0099cc;
  background-color: #00aacc;
  color: #ffffff;
  padding: 5px 10px;
}

button:disabled,
button[disabled]{
  border: 1px solid #999999;
  background-color: #cccccc;
  color: #666666;
}

.noHeight {
  height: 0;
}

.floatLeft {
  float: left;
}
.floatRight {
  float: right;
}

.greenL {
  color: rgb(0, 150, 0);
}
.greenM {
  color: rgb(0, 185, 0);
}
.greenH {
  color: rgb(0, 220, 0);
}
.greenX {
  color: rgb(0, 255, 0);
}

.redL {
  color: rgb(150, 0, 0);
}
.redM {
  color: rgb(185, 0, 0);
}
.redH {
  color: rgb(220, 0, 0);
}
.redX {
  color: rgb(255, 0, 0);
}
</style>
