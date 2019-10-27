import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    newsFeedView: 'briefings',
  },
  mutations: {
    setNewsFeedView(state, view) {
      state.newsFeedView = view;
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
