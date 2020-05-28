<template>
  <div class="news-briefing-container">
    <button @click="groupedBySource = !groupedBySource">toggle</button>
    <news-feed-article-list
      :briefings="groupedBySource ? sources : mappedTopics"
      :groupedBySource="groupedBySource"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import NewsFeedArticleList from '@/components/NewsFeedArticleList.vue';
import { getTopics } from '@/util/api';

export default {
  name: 'Feed',
  data() {
    return {
      sources: [],
      keywords: {},
      sortedKeywords: [],
      groupedBySource: true,
    };
  },
  components: {
    NewsFeedArticleList,
  },
  methods: {},
  computed: {
    mappedTopics() {
      /* eslint-disable prefer-arrow-callback */
      /* eslint-disable func-names */
      const mapped = this.sources.reduce(function (acc, source) {
        source.topics.forEach(function (topic) {
          const sorted = topic.keywords.sort(function (a, b) {
            return this.keywords[b] - this.keywords[a];
          }.bind(this));

          if (acc[sorted[0]]) {
            acc[sorted[0]].articles = [...acc[sorted[0]].articles, ...topic.articles];
            acc[sorted[0]].adjacent = [...acc[sorted[0]].adjacent, ...sorted.slice(1)];
          } else {
            acc[sorted[0]] = { articles: topic.articles, adjacent: sorted.slice(1) };
          }
        }.bind(this));
        return acc;
      }.bind(this), {});
      const topics = this.sortedKeywords.map((keyword) => {
        if (mapped[keyword]) {
          return {
            keywords: [keyword, ...mapped[keyword].adjacent],
            articles: mapped[keyword].articles,
          };
        }
        return false;
      }).filter(res => typeof res === 'object');
      return [{
        topics,
        description: 'sorted',
      }];
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
