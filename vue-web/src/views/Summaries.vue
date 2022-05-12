<template>
  <div>
    <div class="box">
      <button class="button" @click="getTopics">Refresh Summaries</button>
    </div>
    <div v-if="topics.length > 0" style="overflow-y: auto; height: 94vh;">
      <div v-for="(topic, idx) in topics" :key="`${topic.keywords[0]}-${idx}`">
        <card
          :headers="[
            { content: `${topic.articles.length} Articles`, size:'is-one' },
            { content: topic.date, size:'is-one' },
            { content: topic.title, size:'' },
          ]"
          :preview="topic.topic_summ"
          :keywords="topic.keywords"
          :id="idx"
          :nlp_kw="map_nlp(topic.nlp_keywords)"
          :content="`${topic.articles.map(art => art.title).join('--\n\n')}`"
          :buttons="[{
            title: 'View',
            class: () => '',
            callback: () => openTopic(topic),
          }]"
        >
        <div style="padding: 0rem .5rem">
          <div
            v-for="article in topic.articles"
            :key="`topic-article-list-${article.id}`"
            style="padding-top: .5rem;"
            >
            <div class="columns is-multiline">
              <div class="column is-full" style="font-weight: bold">
                {{article.source}} - {{article.title}}
              </div>
              <div class="column is-full">
                <div
                  :style="``"
                  class="keywords__horizontal_container columns is-multiline"
                  >
                  <div
                    v-for="(kw, idx) in [...article.keywords, ...article.nlp_kw]"
                    :key="`${kw}-${article.id}-${idx}`"
                    :style="`${computeKWStyle(kw, topic.keywords)} padding: 0rem 0.75rem;`"
                    class="column is-narrow">{{kw}}</div>
                </div>
              </div>
            </div>
            <div/>
          </div>
        </div>
      </card>
        <!-- :topic_kw="topic.keywords + map_nlp(topic.nlp_keywords)" -->
      </div>
    </div>
  </div>
</template>
<script>
import {
  mapState,
  mapGetters,
  mapActions,
  mapMutations,
} from 'vuex';
import Card from '../components/Card.vue';

export default {
  name: 'Summaries',
  data() {
    return {
      currentSort: 'keywords',
    };
  },
  components: {
    Card,
  },
  methods: {
    ...mapActions({
      getTopics: 'feeds/getTopics',
    }),
    ...mapMutations({
      setSelectedKeywords: 'feeds/setSelectedKeywords',
      setCurrentTopic: 'topic/setCurrentTopic',
    }),
    setSort(sort) {
      if (sort === 'sources' || sort === 'keywords') {
        this.currentSort = sort;
        this.setSelectedKeywords([]);
      } else this.setSelectedKeywords([sort]);
    },
    map_nlp(keywords) {
      if (keywords) {
        return keywords.map(arr => arr[0]);
      }
      return [];
    },
    openTopic(topic) {
      this.setCurrentTopic(topic);
      this.$router.push({ name: 'topic' });
    },
    computeKWStyle(kw, kwList) {
      return kwList.includes(kw) ? 'color: darkred;' : '';
    },
  },
  computed: {
    ...mapGetters({
      mappedTopics: 'feeds/mappedTopics',
      topicsBySource: 'feeds/topicsBySource',
    }),
    sidebarKeywords() {
      return Object.entries(this.keywords).sort((a, b) => {
        return b[1].length - a[1].length;
      }).map(entry => entry[0]);
    },
    ...mapState('feeds', {
      topics: state => state.topics,
      keywords: state => state.keywords,
      sortedKeywords: state => state.sortedKeywords,
      selectedKeywords: state => state.selectedKeywords,
    }),
    topicsByKeyword() {
      if (this.groupByKeywords) {
        return this.mappedTopics;
      }
      return this.topicsBySource;
    },
    groupByKeywords() {
      return (this.currentSort === 'keywords' || this.selectedKeywords.length > 0);
    },
  },
  mounted() {
    if (this.topics.length < 1) {
      this.getTopics();
    }
  },
};
</script>
<style>
  .keywords__horizontal_container {
    /* display: flex; */
    /* flex-direction: row; */
  }
</style>
