<template>
  <div style="">
    <div
      v-for="(briefing, index) in briefings"
      :key="`${briefing.source}-${index}`"
      class="news-briefing-wrapper">
      <strong> {{headline(briefing)}} </strong>
      <div v-for="article in briefing.articles" :key="article.title" >
        <article-card
          :title="article.title"
          :url="article.url"
          :content="article.content"
          :date="article.date"
          :summary="article.summary || false"
          />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import ArticleCard from '@/components/ArticleCard.vue';

export default {
  name: 'NewsFeedArticleList',
  components: {
    ArticleCard,
  },
  props: {
    briefings: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  methods: {
    headline(briefing) {
      let curr = '';
      if (this.currentNewsFeedView === 'briefings') {
        curr = briefing.source;
      } else if (this.currentNewsFeedView === 'world') {
        curr = `${briefing.title} - ${briefing.source}`;
      } else if (this.currentNewsFeedView === 'summaries') {
        console.log('SUMMARIES');
        console.log(this.briefings);
        const articleCount = this.briefings[0] && this.briefings[0].articles
          ? this.briefings[0].articles.length : 0;
        console.log(`${!!this.briefings[0].articles} ${articleCount}`);
        curr = `${articleCount} Stories for Summarizer`;
      }
      return curr;
    },
  },
  computed: {
    ...mapGetters({
      currentNewsFeedView: 'currentNewsFeedView',
    }),
  },
};
</script>

<style>
  .news-briefing-wrapper {
    padding-bottom: 3rem;
    overflow-y: auto;
  }
</style>
