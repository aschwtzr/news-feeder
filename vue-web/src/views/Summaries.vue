<template>
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
      />
      <!-- :topic_kw="topic.keywords + map_nlp(topic.nlp_keywords)" -->
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
