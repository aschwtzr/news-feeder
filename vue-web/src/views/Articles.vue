<template>
  <div class="columns">
    <div class="column">
      <div class="" style="height: 94vh; overflow-y: scroll;">
        <div v-for="article in articles" :key="article.id" style="width: 97.5vw;">
          <article-card
            :showSourceInHeader="true"
            :source="article.source"
            :title="article.title"
            :url="article.url"
            :content="article.raw_text"
            :date="article.date"
            :id="article.id"
            :keywords="article.keywords"
            :nlp_kw="article.nlp_kw"
            :summary="article.summary"
            />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  mapActions,
  mapState,
} from 'vuex';
import ArticleCard from '@/components/article/ArticleCard.vue';

export default {
  data() {
    return {};
  },
  components: {
    ArticleCard,
  },
  methods: {
    ...mapActions({
      getArticles: 'feeds/getArticles',
    }),
    articleSubstring(string) {
      const articleLength = string.length;
      return `${string.substring(0, articleLength > 300 ? 300 : articleLength)}${articleLength > 300 ? '...' : ''}`;
    },
  },
  computed: {
    ...mapState('feeds', {
      articles: state => state.articles,
    }),
  },
  mounted() {
    if (this.articles.length < 1) {
      this.getArticles();
    }
  },
};
</script>

<style>
  .tableFixHead          { overflow: auto; height: calc(100vh - 60px); display: block; }
  .tableFixHead thead th { position: sticky; top: 0; z-index: 1; }

  /* Just common table stuff. Really. */
  table  { border-collapse: collapse; width: 100%; }
  th, td { padding: 8px 16px; }
  th     { background:#eee; }
</style>
