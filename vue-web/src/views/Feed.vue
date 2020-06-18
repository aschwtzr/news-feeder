<template>
  <div style="height: 100%;">
    <div class="columns is-marginless content-view">
      <div class="column is-narrow feed__sidebar-container">
        <sidebar :keywords="sidebarKeywords" @sortChanged="(sort) => currentSort = sort"/>
      </div>
      <div class="column" style="overflow-y: auto;">
        <news-feed-article-list
          :briefings="groupedBySource ? topics : mappedTopics"
          :groupedBySource="groupedBySource"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import NewsFeedArticleList from '@/components/feed/NewsFeedArticleList.vue';
import Sidebar from '@/components/feed/Sidebar.vue';

export default {
  name: 'Feed',
  data() {
    return {
      currentSort: 'feed',
    };
  },
  components: {
    NewsFeedArticleList,
    Sidebar,
  },
  methods: {
    ...mapActions({
      getTopics: 'feeds/getTopics',
    }),
  },
  computed: {
    ...mapGetters({
      mappedTopics: 'feeds/mappedTopics',
    }),
    sidebarKeywords() {
      const { topics } = this.mappedTopics(this.currentKeywords)[0];
      if (topics.length) {
        return topics.map(topic => topic.keywords[0]);
      }
      return [];
    },
    ...mapState('feeds', {
      topics: state => state.topics,
      keywords: state => state.keywords,
      sortedKeywords: state => state.sortedKeywords,
    }),

    groupedBySource() {
      return this.currentSort === 'feed';
    },
    currentKeywords() {
      if (this.currentSort === 'feed' || this.currentSort === 'keywords') {
        return this.sortedKeywords;
      }
      return [this.currentSort];
    },
  },
  mounted() {
    this.getTopics();
  },
};
</script>

<style>
  .content-view {
    /* position: fixed; */
    top: 3.5rem;
    height:calc(100vh -  2.75rem);
    /* width: 100%; */
  }

  .topic-source-wrapper {
    margin-bottom: 3rem;
    overflow-y: auto;
  }

  .feed__component-container {
    display: flex;
    flex-direction: row;
  }

  .feed__sidebar-container {
    border-right: 1px solid rgba(0, 0, 0, .25);
    overflow-y: auto;
  }

  .feed__full-width-fixed-container {
    /* position: fixed;
    top: 3.5rem;
    height:calc(100vh -  2.75rem);
    width: 100%; */
  }

</style>
