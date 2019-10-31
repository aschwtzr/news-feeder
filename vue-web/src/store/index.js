import Vue from 'vue';
import Vuex from 'vuex';
import { getGoogleFeed, getBriefings, getSummaryForURL } from '@/util/api';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    newsFeedView: 'briefings',
    summarizerFeed: {},
    googleFeed: [],
    rssFeeds: [],
    apiLimit: undefined,
  },
  mutations: {
    setNewsFeedView(state, view) {
      state.newsFeedView = view;
    },
    addToSummarizerFeed(state, article) {
      debugger;
      state.summarizerFeed = { ...state.summarizerFeed, [article.url]: article };
    },
    addGoogleFeed(state, feed) {
      state.googleFeed = feed;
    },
    addRSSFeed(state, feed) {
      state.rssFeeds = feed;
    },
    summaryForArticle(state, summary) {
      state.summarizerFeed[summary.key].summary = summary.value;
    },
    setAPILimit(state, limit) {
      state.apiLimit = limit;
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
    summarizeArticle({ commit }, url) {
      return new Promise((resolve, reject) => {
        getSummaryForURL(url).then((results) => {
          const { summary_data: summaryData } = results.data;
          const decodedURL = decodeURIComponent(url);
          commit('summaryForArticle', { key: decodedURL, value: summaryData.summary });
          commit('setAPILimit', summaryData.limit);
          resolve();
        }).catch((error) => {
          reject(error);
        });
      });
    },
    toggleSummarizerFeed({ state, dispatch, commit }, article) {
      debugger;
      commit('addToSummarizerFeed', article);
      if (!state.summarizerFeed[article.url].summary) {
        dispatch('summarizeArticle', article.url);
      }
    },
  },
  getters: {
    currentNewsFeedView(state) {
      return state.newsFeedView;
    },
    articlesForSummarizer(state) {
      const feed = Object.entries(state.summarizerFeed);
      const mapped = feed.map(objArr => objArr[1]);
      // const filtered = mapped.filter(article => article.active);
      return mapped;
    },
  },
  modules: {
  },
});
