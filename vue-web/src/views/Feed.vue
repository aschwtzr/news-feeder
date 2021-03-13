<template>
  <div style="height: 100%;">
    <div class="columns is-marginless content-view">
      <div class="column is-narrow feed__sidebar-container">
        <sidebar :keywords="sidebarKeywords" @sortChanged="(sort) => setSort(sort)"/>
      </div>
      <div class="column feed__article-list">
        <news-feed-article-list
          :briefings="groupByKeywords ? topics : topicsBySource"
          :groupedBySource="!groupByKeywords"
        />
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
import NewsFeedArticleList from '@/components/feed/NewsFeedArticleList.vue';
import Sidebar from '@/components/feed/Sidebar.vue';

export default {
  name: 'Feed',
  data() {
    return {
      currentSort: 'keywords',
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
  .content-view {
    top: 3.5rem;
    height:calc(100vh -  2.75rem);
    width: 100vw;
  }

  .feed__component-container {
    display: flex;
    flex-direction: row;
  }

  .feed__sidebar-container {
    border-right: 1px solid rgba(0, 0, 0, .25);
    overflow-y: scroll;
  }

  .feed__article-list {
      overflow-y: scroll;
  }
  @media screen and (max-width: 600px) {
    .feed__sidebar-container {
      display: none;
      overflow-y: visible;
    }
}

</style>
