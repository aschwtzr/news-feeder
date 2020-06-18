import {
  getFeedSources,
  getTopics,
} from '@/util/api';

const feeds = {
  namespaced: true,
  state: {
    availableSources: {},
    summarizerFeed: {},
    topics: [],
    keywords: {},
    sortedKeywords: [],
  },
  mutations: {
    setAvailableSources(state, sources) {
      state.availableSources = sources;
    },
    addToSummarizerFeed(state, article) {
      state.summarizerFeed = { ...state.summarizerFeed, [article.url]: article };
    },
    setTopics(state, topics) {
      state.topics = topics;
    },
    setKeywords(state, keywords) {
      state.keywords = keywords;
    },
    setSortedKeywords(state, sortedKeywords) {
      state.sortedKeywords = sortedKeywords;
    },
  },
  actions: {
    getAvailableSources({ commit }) {
      return new Promise((resolve, reject) => {
        getFeedSources().then((results) => {
          const availableSources = results.data.sources.reduce((acc, curr) => {
            acc[curr.id] = curr;
            return acc;
          }, {});
          commit('setAvailableSources', availableSources);
          resolve(availableSources);
        }).catch(error => reject(error));
      });
    },
    getTopics({ commit }) {
      getTopics().then((res) => {
        commit('setTopics', res.data.results);
        commit('setKeywords', res.data.keywords);
        const sorted = Object.entries(res.data.keywords)
          .sort((a, b) => b[1] - a[1])
          .map(pair => pair[0]);
        commit('setSortedKeywords', sorted);
      });
    },
  },
  getters: {
    articleInSummarizerFeed: state => (url) => {
      return state.summarizerFeed[url];
    },
    mappedTopics: state => (currentKeywords) => {
      const mapped = state.topics.reduce((acc, source) => {
        source.topics.forEach((topic) => {
          const sorted = topic.keywords.sort((a, b) => {
            return state.keywords[b] - state.keywords[a];
          });

          if (acc[sorted[0]]) {
            acc[sorted[0]].articles = [...acc[sorted[0]].articles, ...topic.articles];
            acc[sorted[0]].adjacent = [...acc[sorted[0]].adjacent, ...sorted.slice(1)];
          } else {
            acc[sorted[0]] = { articles: topic.articles, adjacent: sorted.slice(1) };
          }
        });
        return acc;
      }, {});
      const topics = currentKeywords.map((keyword) => {
        if (mapped[keyword]) {
          return {
            keywords: [keyword, ...mapped[keyword].adjacent],
            articles: mapped[keyword].articles,
          };
        }
        return false;
      })
        .filter(res => typeof res === 'object');
      return [{
        topics,
        description: 'sorted',
      }];
    },
  },
};

export default feeds;
