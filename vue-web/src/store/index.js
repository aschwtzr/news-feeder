import Vue from 'vue';
import Vuex from 'vuex';
import { getGoogleFeed, getBriefings } from '@/util/api';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    newsFeedView: 'briefings',
    summarizerFeed: {},
    googleFeed: [],
    rssFeeds: [],
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
    addGoogleFeed(state, feed) {
      state.googleFeed = feed;
    },
    addRSSFeed(state, feed) {
      state.rssFeeds = feed;
    },
  },
  actions: {
    getGoogleFeed({ commit }) {
      return new Promise((resolve, reject) => {
        getGoogleFeed().then((results) => {
          const google = results.data.news.map((headline) => {
            let mapped = [];
            if (headline.articles && headline.articles.length > 1) {
              mapped = headline.articles.map((article) => {
                const output = Object.assign({}, article);
                output.content = article.source || article.url;
                return output;
              });
            } else {
              mapped = [{
                title: headline.title,
                url: headline.url,
                content: headline.source,
                date: headline.date || '',
              }];
            }
            const nwbObj = Object.assign({}, headline, { source: headline.source || 'missing source', articles: mapped });
            return nwbObj;
          });
          commit('addGoogleFeed', google);
          resolve();
        }).catch((err) => {
          console.log(err);
          reject(err);
        });
      });
    },
    getBriefings({ commit }) {
      return new Promise((resolve, reject) => {
        getBriefings().then((results) => {
          const { briefings } = results.data;
          commit('addRSSFeed', briefings);
          resolve();
        }).catch((err) => {
          console.log(err);
          reject(err);
        });
      });
    },
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
