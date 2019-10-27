<template>
  <div>
    <news-feed-tabs />
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
</template>

<script>
import { mapGetters } from 'vuex';
import { getBriefings, getGoogleFeed } from '@/util/api';
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
    headline(briefing) {
      let curr = '';
      if (this.currentNewsFeedView === 'briefings') {
        curr = briefing.source;
      } else if (this.currentNewsFeedView === 'world') {
        curr = `${briefing.title} - ${briefing.source}`;
      }
      return curr;
    },
  },
  computed: {
    ...mapGetters({
      currentNewsFeedView: 'currentNewsFeedView',
    }),
    briefingsByView() {
      let curr = [];
      if (this.currentNewsFeedView === 'briefings') {
        curr = this.briefings;
      } else if (this.currentNewsFeedView === 'world') {
        curr = this.googleNews;
      }
      return curr;
    },
  },
  mounted() {
    getBriefings().then((results) => {
      this.briefings = results.data.briefings;
    });
    getGoogleFeed().then((results) => {
      this.googleNews = results.data.news.map((headline) => {
        let mapped = [];
        if (headline.articles && headline.articles.length > 1) {
          mapped = headline.articles.map((article) => {
            const output = Object.assign({}, article);
            output.content = article.source || article.url;
            return output;
          });
          // console.log(`mapped: ${mapped[0].content}`);
        } else {
          mapped = [{
            title: headline.title,
            url: headline.url,
            content: headline.source,
            date: headline.date || '',
          }];
          // console.log(`dummy: ${mapped[0].content}`);
        }
        const nwbObj = Object.assign({}, headline, { source: headline.source || 'missing source', articles: mapped });
        return nwbObj;
      });
    });
  },
};
</script>

<style>
  .news-briefing-wrapper {
    padding-bottom: 3rem;
  }
</style>
