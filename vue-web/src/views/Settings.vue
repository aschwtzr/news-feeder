<template>
  <div>
    <label class="checkbox">
      <input type="checkbox" v-model="smmry">
      Include SMMRY <a href="#">warning: paid service</a>
    </label>
    <div>
      <strong>Available Sources</strong>
      <div v-for="source in sources" :key="source">
        <label class="checkbox">
          <input type="checkbox">
          {{source}}
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import { getFeedSources } from '@/util/api';

export default {
  name: 'Sources',
  data() {
    return {
      smmry: false,
      sources: [],
      active: {},
    };
  },
  mounted() {
    getFeedSources().then((results) => {
      this.sources = results.data.sources;
    });
  },
};
</script>

<style>

</style>
