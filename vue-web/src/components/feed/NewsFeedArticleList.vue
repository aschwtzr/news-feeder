<template>
  <div>
    <div
      v-for="(source, index) in briefings"
      :key="`${source.description}-${index}`"
      class="topic-source-wrapper">
      <strong v-if="groupedBySource"> {{source.description}} </strong>
      <div v-for="topic in source.topics" :key="topic.keywords.join('')" >
        <div :style="groupedBySource ? '': 'font-weight: strong'">
          keywords: {{topic.keywords.join(', ')}}
        </div>
        <div v-for="(article, index) in topic.articles" :key="`${source}-${index}`">
          <strong v-if="!groupedBySource"> {{article.source}} </strong>
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
import ArticleCard from '@/components/article/ArticleCard.vue';

export default {
  name: 'NewsFeedArticleList',
  components: {
    ArticleCard,
  },
  props: {
    groupedBySource: {
      type: Boolean,
      default: () => false,
      require: true,
    },
    briefings: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  methods: {},
  computed: {},
};
</script>

<style>
  .topic-source-wrapper {
    margin-bottom: 3rem;
  }
</style>
