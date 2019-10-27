import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    newsFeedView: 'briefings',
    summarizerFeed: {},
    summaries: [],
  },
  mutations: {
    setNewsFeedView(state, view) {
      state.newsFeedView = view;
    },
    addToSummarizerFeed(state, source) {
      const updatedFeed = Object.assign({}, state.summarizerFeed);
      if (updatedFeed[source.url]) {
        updatedFeed[source.url].active = source.active;
      } else {
        updatedFeed[source.url] = source;
      }
      state.summarizerFeed = updatedFeed;
    },
  },
  actions: {
  },
  getters: {
    currentNewsFeedView(state) {
      return state.newsFeedView;
    },
    articlesForSummarizer(state) {
      const feed = Object.entries(state.summarizerFeed);
      const mapped = feed.map(objArr => objArr[1]);
      const filtered = mapped.filter(article => article.active);
      return filtered;
    },
  },
  modules: {
  },
});
