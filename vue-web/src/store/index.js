import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    newsFeedView: 'briefings',
    summarizeFeed: [],
    summaries: [],
  },
  mutations: {
    setNewsFeedView(state, view) {
      state.newsFeedView = view;
    },
    addToSummarizeFeed(state, source) {
      state.summarizeFeed.push(source);
    },
  },
  actions: {
  },
  getters: {
    currentNewsFeedView(state) {
      return state.newsFeedView;
    },
  },
  modules: {
  },
});
