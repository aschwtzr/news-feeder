<template>
  <div style="background-color: #F7F7FF;">
    <news-feed-tabs />
    <div style=" padding-top: 1.5rem;">
      <div v-if="currentNewsFeedView === 'summaries'">
        {{ summarizerSummary }}
      </div>
      <news-feed-article-list :briefings="briefingsByView" />
    </div>
  </div>
</template>

<script>
import {
  mapGetters,
  mapActions,
  mapState,
  mapMutations,
} from 'vuex';
import _ from 'lodash';
import NewsFeedTabs from '@/components/NewsFeedTabs.vue';
import NewsFeedArticleList from '@/components/NewsFeedArticleList.vue';

export default {
  name: 'NewsFeed',
  components: {
    NewsFeedTabs,
    NewsFeedArticleList,
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
      debugger;
      console.log(newList);
      this.setSummarizerSummary('Summarizing...');
      this.debouncedGetContentSummary(newList);
    },
  },
};
</script>

<style>

</style>
