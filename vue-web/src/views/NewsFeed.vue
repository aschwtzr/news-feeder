<template>
  <div>
    <news-feed-tabs />
    <div v-if="currentNewsFeedView === 'summaries'">
      Summary goes here
    </div>
    <news-feed-article-list :briefings="briefingsByView" />
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';
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
    }),

  },
  computed: {
    ...mapGetters({
      currentNewsFeedView: 'currentNewsFeedView',
      articlesForSummarizer: 'articlesForSummarizer',
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
  },
};
</script>

<style>

</style>
