<template>
  <div class="">
    <div class="container">
      <div class="tile is-ancestor is-12 is-vertical">
        <div class="tile is-parent">
          <div class="tile is-child box">
            <div class="tile is-ancestor">
              <div class="tile is-8 is-vertical"> <!-- column is-3 -->
                <div style="font-weight: bold;">
                  Available Feeds
                </div>
                <br/>
                <div
                  v-for="source in sources"
                  :key="`${source.key}-${source.id}`"
                  class="field"
                  >
                  <!-- <div > -->
                    <div class="control">
                      <label class="checkbox">
                        <input
                          type="checkbox"
                          :value="source.id"
                          @click="toggleSource(source.id)"
                          >
                      </label>
                      {{source.description}}
                    </div>
                  <!-- </div> -->
                </div>
              </div>
              <div class="tile "> <!-- column is-4 is-offset-5 -->
                <div class="tile is-ancestor">
                  <div class="tile is-parent is-vertical">
                    <div class="field tile is-child">
                      <label class="label">Limit</label>
                      <div class="control">
                        <input class="input " type="number" v-model="limit">
                      </div>
                    </div>
                    <div class="field tile is-child">
                      <div class="control">
                        <button class="button is-link " @click="fetchSelectedFeeds">
                          Fetch Feed Data
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="Object.keys(rawData).length > 0" class="tile is-parent">
          <div class="is-tile is-parent is-vertical"
            style="width: fill-available"
            >
            <div
              v-for="feed in rawData"
              class="tile is-child"
              :key="`raw_data-${feed.id}`"
              >
              <div class="tile is-ancestor is-vertical">
                  <div class="tile is-parent">
                    <div class="tile is-child box">
                      <div class="tile is-parent is-vertical">
                        <h5 class="title is-5 is-child">{{feed.description}}</h5>
                        <div
                          v-for="(topic, topicIdx) in feed.topics"
                          :key="`rd_topic_${feed.id}_${topicIdx}`"
                          class="tile is-child"
                          >
                          {{topic.articles[0].length > 1 ? `Keywords: ${topic.keywords}` : ''}}
                          <div
                            v-for="article in topic.articles"
                            :key="`${article.url.substring(article.url.length - 1, 30)}_${feed.id}`"
                            >
                            <article-card
                              :url="article.url"
                              :date="article.date"
                              :source="article.source"
                              :sourceId="feed.id"
                              :title="article.title"
                              :keywords="article.keywords"
                              :raw_text="article.raw_text"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
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
import ArticleCard from '../components/pipelines/ArticleCard.vue';

export default {
  name: 'Pipelines',
  components: {
    ArticleCard,
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
