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
          /* eslint-disable no-param-reassign */
          const availableSources = results.data.sources.reduce((acc, curr) => {
            acc[curr.id] = curr;
            return acc;
          }, {});
          /* eslint-enable no-param-reassign */
          commit('setAvailableSources', availableSources);
          resolve(availableSources);
        }).catch(error => reject(error));
      });
    },
    getTopics({ commit, rootState }, defaultSources = false) {
      const options = [];
      if (rootState.settings.sources && !defaultSources) {
        const sourceString = `source=${rootState.settings.sources.join(',')}`;
        options.push(sourceString);
      }
      if (rootState.settings.userSource && !defaultSources) {
        const userSourceString = `user_source=${rootState.settings.userSources.join(',')}`;
        options.push(userSourceString);
      }
      getTopics(options).then((res) => {
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
      /* eslint-disable no-param-reassign */
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
      /* eslint-enable no-param-reassign */
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
