<template>
  <section style="background-color: #F7F7FF;">
    <news-feed-tabs />
    <div style=" padding-top: 1.5rem;" class="container">
      <settings v-if="currentNewsFeedView === 'settings'" />
      <admin v-if="currentNewsFeedView === 'admin'" />
      <topic v-if="currentNewsFeedView === 'topics'" />
      <div v-else>
        <div v-if="currentNewsFeedView === 'summaries'">
          {{ summarizerSummary }}
        </div>
        <news-feed-article-list :briefings="briefingsByView" />
      </div>
    </div>
  </section>
</template>

<script>
import {
  mapGetters,
  mapActions,
  mapState,
  mapMutations,
} from 'vuex';
import _ from 'lodash';
import NewsFeedArticleList from '@/components/NewsFeedArticleList.vue';
import Settings from '@/views/Settings.vue';
import Admin from '@/views/Admin.vue';
import Topic from '@/components/Topic.vue';

export default {
  name: 'NewsFeed',
  components: {
    NewsFeedTabs,
    NewsFeedArticleList,
    Settings,
    Admin,
    Topic,
  },
  data() {
    return {
      briefings: [],
      googleNews: [],
    };
  },
  methods: {
    ...mapActions({
      getBriefings: 'getBriefings',
      getGoogleFeed: 'getGoogleFeed',
      getContentSummary: 'getContentSummary',
    }),
    ...mapMutations({
      setSummarizerSummary: 'setSummarizerSummary',
    }),
  },
  computed: {
    ...mapGetters({
      currentNewsFeedView: 'currentNewsFeedView',
      articlesForSummarizer: 'articlesForSummarizer',
      summarizerSummary: 'summarizerSummary',
    }),
    ...mapState({
      googleFeed: state => state.googleFeed,
      rssFeeds: state => state.rssFeeds,
    }),
    briefingsByView() {
      let curr = [];
      if (this.currentNewsFeedView === 'briefings') {
        curr = this.rssFeeds;
      } else if (this.currentNewsFeedView === 'world') {
        curr = this.googleFeed;
      } else if (this.currentNewsFeedView === 'summaries') {
        curr = [{
          source: 'summarizer',
          articles: this.articlesForSummarizer,
        }];
      }
      return curr;
    },
  },
  mounted() {
    this.getBriefings();
    this.getGoogleFeed();
    this.debouncedGetContentSummary = _.debounce(this.getContentSummary, 500);
  },
  watch: {
    articlesForSummarizer(newList) {
      console.log(newList);
      this.setSummarizerSummary('Summarizing...');
      this.debouncedGetContentSummary(newList);
    },
  },
};
</script>

<style scoped>
  .container {
    height: calc(100vh - 1.5rem)
  }
</style>
