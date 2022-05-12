<template>
  <div>
    <div class="box columns">
      <div class="column is-3">
        <div style="font-weight: bold;">
          Available Feeds
        </div>
        <br/>
        <div v-for="source in sources" :key="`${source.key}-${source.id}`">
          <label>
              <input type="checkbox" :value="source.id" @click="toggleSource(source.id)">
              {{source.description}}
          </label>
        </div>
      </div>
      <div class="column is-4 is-offset-7">
        <button class="button" @click="getRSSData(selectedSourceIds)">
          Fetch Feed Data
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import {
  mapActions,
  mapState,
} from 'vuex';

export default {
  name: 'Pipelines',
  data() {
    return {
      selectedSourceIds: [],
      articleIds: [],
      topic: {},
    };
  },
  computed: {
    ...mapState('pipelines', {
      sources: state => state.sources,
    }),
  },
  methods: {
    ...mapActions({
      getSources: 'pipelines/getSources',
      getRSSData: 'pipelines/getRSSData',
    }),
    fetchSelectedFeeds() {
      debugger;
      this.getRSSData(this.selectedSourceIds);
    },
    toggleSource(id) {
      const idIndex = this.selectedSourceIds.indexOf(id);
      console.log(idIndex);
      if (idIndex >= 0) {
        this.selectedSourceIds = this.selectedSourceIds.filter(sourceId => sourceId !== id);
      } else this.selectedSourceIds = [...this.selectedSourceIds, id];
    },
  },
  mounted() {
    if (this.sources.length < 1) {
      this.getSources();
    }
  },
};
</script>
<style>
</style>
