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
    articleCount: 0,
    topicsCount: 0,
    mappedKeywords: {},
    sortedKeywords: [],
    selectedKeywords: [],
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
    setCounts(state, counts) {
      state.articleCount = counts.articles;
      state.topicsCount = counts.topics;
    },
    setKeywords(state, keywords) {
      state.keywords = keywords;
    },
    setSortedKeywords(state, sortedKeywords) {
      state.sortedKeywords = sortedKeywords;
    },
    setMappedKeywords(state, mappedKeywords) {
      state.mappedKeywords = mappedKeywords;
    },
    setSelectedKeywords(state, selectedKeywords) {
      state.selectedKeywords = selectedKeywords;
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
    getTopics({ commit, rootState }, defaults = false) {
      const options = [];
      if (rootState.settings.sources && !defaults) {
        const sourceString = `source=${rootState.settings.sources.join(',')}`;
        options.push(sourceString);
      }
      if (rootState.settings.customFeeds && !defaults) {
        let userSourceString = `user_source=${rootState.settings.customFeeds.join(',')}`;
        if (options.length > 0) userSourceString = `&${userSourceString}`;
        options.push(userSourceString);
      }
      if (rootState.settings.articleLimit && !defaults) {
        let userSourceString = `limit=${rootState.settings.articleLimit}`;
        if (options.length > 0) userSourceString = `&${userSourceString}`;
        options.push(userSourceString);
      }
      getTopics(options).then((res) => {
        commit('setTopics', res.data.results);
        commit('setKeywords', { ...res.data.keywords });
        commit('setCounts', { ...res.data.counts, keywords: res.data.keywords.length });
        commit('setMappedKeywords', { ...res.data.keywords });
      });
    },
  },
  getters: {
    articleInSummarizerFeed: state => (url) => {
      return state.summarizerFeed[url];
    },
    topicsBySource: (state) => {
      const articles = state.topics[0].topics.reduce((acc, topic) => {
        return [...acc, ...topic.articles];
      }, []);
      const bySourceDict = articles.reduce((acc, curr) => {
        if (acc[curr.source]) {
          acc[curr.source].push(curr);
        } else acc[curr.source] = [curr];
        return acc;
      }, {});
      return Object.entries(bySourceDict).sort((a, b) => {
        return b[1].length - a[1].length;
      }).map((source) => {
        return {
          description: source[0],
          topics: source[1].map((article) => {
            return {
              topic_summ: article.preview,
              keywords: article.keywords,
              title: article.title,
              articles: [article],
            };
          }),
        };
      });
    },
    mappedTopics: (state) => {
      /* eslint-disable no-param-reassign */
      const stateTopics = [...state.topics];
      const topicsMap = stateTopics.reduce((acc, source) => {
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
      const keywords = state.selectedKeywords.length
        ? [...state.selectedKeywords] : state.sortedKeywords;
      const topics = keywords.map((keyword) => {
        if (topicsMap[keyword]) {
          return {
            keywords: [keyword, ...topicsMap[keyword].adjacent],
            articles: topicsMap[keyword].articles,
          };
        }
        return false;
      }).filter(res => typeof res === 'object');
      return [{
        topics,
        description: 'sorted',
      }];
    },
  },
};

export default feeds;
