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

      <table class="table mt-5">
        <thead>
          <tr>
            <th scope="col"
              v-for="(column_name, index) in bestTicks.state.list[0]"
              :key="index">
              {{ column_name }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in bestTicks.state.list.slice(1)" :key="index">
            <td v-for="(value, idx) in row" :key="idx">{{ value }}</td>
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
  bestTicks = setup(() => useArtists());

  created() {
    this.bestTicks.get();
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
</style>
