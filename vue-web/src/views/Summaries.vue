<template>
  <div style="overflow-y: scroll;">
    <div v-for="topic in topics[0].topics" :key="topic.keywords[0]">
      <div>{{topic.title}}</div>
      <div>{{topic.keywords}}</div>
      <div>{{topic.date}}</div>
      <div>{{topic.articles.length}} {{topic.articles.map(art => art.source).join(', ')}}</div>
      <br>
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

export default {
  name: 'JEllo',
  data() {
    return {
      currentSort: 'keywords',
    };
  },
  components: {},
  methods: {
    ...mapActions({
      getTopics: 'feeds/getTopics',
    }),
    ...mapMutations({
      setSelectedKeywords: 'feeds/setSelectedKeywords',
    }),
    setSort(sort) {
      if (sort === 'sources' || sort === 'keywords') {
        this.currentSort = sort;
        this.setSelectedKeywords([]);
      } else this.setSelectedKeywords([sort]);
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
    this.getTopics();
  },
};
</script>
<style>
</style>
