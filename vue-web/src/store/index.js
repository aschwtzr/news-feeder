import Vue from 'vue';
import Vuex from 'vuex';
import settings from './settings';
import feeds from './feeds';
import topic from './topic';
/* eslint-disable import/prefer-default-export */
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    settings,
    feeds,
    topic,
  },
  state: {
  },
  mutations: {
  },
  actions: {
  },
  getters: {
    mergedSources(state) {
      if (state.settings.sources) {
        const mappedSources = state.settings.sources.map((key) => {
          return { ...state.feeds.availableSources[key], ...{ active: true } };
        });
        const remainingSources = Object.keys(state.feeds.availableSources)
          .filter(key => !state.settings.sources.includes(key))
          .map(key => state.feeds.availableSources[key]);
        return [...mappedSources, ...remainingSources];
      }
      return state.feeds.availableSources;
    },
    articlesForSummarizer(state) {
      const feed = Object.entries(state.summarizerFeed);
      const mapped = feed.map(objArr => objArr[1]);
      // const filtered = mapped.filter(article => article.active);
      return mapped;
    },
  },
});
