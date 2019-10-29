<template>
  <div>
    <news-feed-tabs style="position: sticky; top: -1px;"/>
    <div style="">
      <div
        v-for="(briefing, index) in briefingsByView"
        :key="`${briefing.source}-${index}`"
        class="news-briefing-wrapper">
        <strong> {{headline(briefing)}} </strong>
        <div v-for="article in briefing.articles" :key="article.title" >
          <article-card
            :title="article.title"
            :url="article.url"
            :content="article.content"
            :date="article.date"
            />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex';
import NewsFeedTabs from '@/components/NewsFeedTabs.vue';
import ArticleCard from '@/components/ArticleCard.vue';

export default {
  name: 'NewsFeed',
  components: {
    ArticleCard,
    NewsFeedTabs,
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
    headline(briefing) {
      let curr = '';
      if (this.currentNewsFeedView === 'briefings') {
        curr = briefing.source;
      } else if (this.currentNewsFeedView === 'world') {
        curr = `${briefing.title} - ${briefing.source}`;
      } else if (this.currentNewsFeedView === 'summaries') {
        const articleCount = this.briefingsByView.length > 0
          ? this.briefingsByView[0].articles.length : 0;
        console.log(`${!!this.briefingsByView} ${articleCount}`);
        curr = `${articleCount} Stories for Summarizer`;
      }
      return curr;
    },
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
  .news-briefing-wrapper {
    padding-bottom: 3rem;
    overflow-y: auto;
  }
</style>
