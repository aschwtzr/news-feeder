<template>
  <div class="news-briefing-container">
    <button @click="toggleKeywords = !toggleKeywords">toggle</button>
    <div
      v-for="(source, index) in sources"
      :key="`${source.description}-${index}`"
      class="topic-source-wrapper">
      <strong> {{source.description}} </strong>
      <div v-for="topic in source.topics" :key="topic.keywords.join('')" >
        <div>keywords: {{topic.keywords.join()}}</div>
        <div v-for="(article, index) in topic.articles" :key="`${source}-${index}`">
          <article-card
            :title="article.title"
            :url="article.url"
            :content="article.preview"
            :date="article.date"
            :summary="article.summary || false"
            />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import ArticleCard from '@/components/ArticleCard.vue';
import { getTopics } from '@/util/api';

export default {
  name: 'NewsFeedArticleList',
  data() {
    return {
      sources: [],
      keywords: {},
      sortedKeywords: [],
      toggleKeywords: false,
    };
  },
  components: {
    ArticleCard,
  },
  methods: {},
  computed: {
    mappedTopics() {
      /* eslint-disable prefer-arrow-callback */
      /* eslint-disable func-names */
      return this.sources.reduce(function (acc, source) {
        source.topics.forEach(function (topic) {
          const sorted = topic.keywords.sort(function (a, b) {
            return this.keywords[b] - this.keywords[a];
          }.bind(this));
          if (acc[sorted[0]]) {
            acc[sorted[0]].articles = [...acc[sorted[0]].articles, topic.articles];
            acc[sorted[0]].adjacent = [...acc[sorted[0]].adjacent, topic.articles];
          } else {
            acc[sorted[0]] = { articles: topic.articles, adjacent: sorted.splice(0, 1) };
          }
        }.bind(this));
        return acc;
      }.bind(this), {});
    },
    ...mapGetters({
      currentNewsFeedView: 'currentNewsFeedView',
    }),
  },
  mounted() {
    /* eslint-disable prefer-arrow-callback */
    /* eslint-disable func-names */
    getTopics().then(function (res) {
      this.sources = res.data.results;
      this.keywords = res.data.keywords;
      this.sortedKeywords = Object.entries(res.data.keywords)
        .sort((a, b) => b[1] - a[1])
        .map(pair => pair[0]);
    }.bind(this));
  },
};
</script>

<style>
  .topic-source-wrapper {
    margin-bottom: 3rem;
    overflow-y: auto;
    width: 90vw;
  }

  .news-briefing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
</style>
