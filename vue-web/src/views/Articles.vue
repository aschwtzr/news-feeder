<template>
  <div class="">
    <!-- <div class="column"> -->
      <!-- <div class=""> -->
        <div v-for="article in articles" :key="article.id">
          <article-card
            :url="article.url"
            :date="article.date"
            :source="article.source"
            :sourceId="article.source"
            :title="article.title"
            :keywords="article.keywords"
            :showSourceInHeader="true"
            :raw_text="article.raw_text"
            :paragraphs="article.paragraphs"
            :id="article.id"
            :nlp_kw="article.nlp_kw"
            :preview="article.summary"
            :events="[]"
            />
        </div>
      <!-- </div> -->
    <!-- </div> -->
  </div>
</template>

<script>
import {
  mapActions,
  mapState,
} from 'vuex';
import ArticleCard from '@/components/pipelines/ArticleCard.vue';

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
