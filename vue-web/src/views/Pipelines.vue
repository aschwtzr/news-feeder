<template>
  <div style="height: calc(95vh - 42px); overflow-y: auto">
    <div class="box">
      <div class="columns">
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
        <div class="column is-4 is-offset-5">
          <div class="tile is-ancestor">
            <div class="tile is-parent is-vertical">
              <button class="button tile is-child" @click="fetchSelectedFeeds">
                Fetch Feed Data
              </button>
              <input class="input tile is-child" type="number" v-model="limit">
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="Object.keys(rawData).length > 0" class="columns">
      <div class="column">
        <div class="tile is-12 is-vertical is-ancestor">
          <div v-for="feed in rawData" class="tile is-vertical" :key="`raw_data-${feed.id}`">
            <div class="box" style="margin-left: 1rem; width: 93vw;">
              <h5 class="title is-5 is-parent">{{feed.description}}</h5>
              <div
                v-for="(topic, idx) in feed.topics"
                :key="`rd_topic_${feed.id}_${idx}`"
                class="tile is-vertical is-child"
                >
                NLTK: {{topic.keywords}}
                <div
                  v-for="(article, idx) in topic.articles[0]"
                  :key="`rd_articles_${idx}_${feed.id}`"
                  >
                  <card
                    :headers="[
                      { content: article.id, size:'is-one' },
                      { content: article.date, size:'is-one' },
                      { content: article.source, size:'is-one' },
                      { content: article.title, size:'' },
                    ]"
                    :keywords="article.keywords"
                    :id="article.id"
                    >
                    <div>
                      {{article.raw_text}}
                    </div>
                  </card>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import {
  mapActions,
  mapState,
} from 'vuex';
import Card from '../components/Card.vue';

export default {
  name: 'Pipelines',
  components: {
    Card,
  },
  data() {
    return {
      selectedSourceIds: [],
      limit: 2,
      articleIds: [],
      topic: {},
    };
  },
  computed: {
    ...mapState('pipelines', {
      sources: state => state.sources,
      rawData: state => state.rawData,
    }),
  },
  methods: {
    ...mapActions({
      getSources: 'pipelines/getSources',
      getRSSData: 'pipelines/getRSSData',
    }),
    fetchSelectedFeeds() {
      const limit = parseInt(this.limit, 0);
      this.getRSSData({ sourceIds: this.selectedSourceIds, limit });
    },
    toggleSource(id) {
      const idIndex = this.selectedSourceIds.indexOf(id);
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
