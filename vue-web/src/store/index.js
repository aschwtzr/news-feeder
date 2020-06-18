import Vue from 'vue';
import Vuex from 'vuex';
import settings from './settings';
import {
  getGoogleFeed,
  getBriefings,
  getSummaryForURL,
  getContentSummary,
  getFeedSources,
} from '@/util/api';
/* eslint-disable import/prefer-default-export */
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    settings,
  },
  state: {
    newsFeedView: 'briefings',
    summarizerFeed: {},
    summarizerSummary: '',
    googleFeed: [],
    rssFeeds: [],
    apiLimit: undefined,
    availableSources: {},
  },
  mutations: {
    setNewsFeedView(state, view) {
      state.newsFeedView = view;
    },
    addToSummarizerFeed(state, article) {
      state.summarizerFeed = { ...state.summarizerFeed, [article.url]: article };
    },
    addGoogleFeed(state, feed) {
      state.googleFeed = feed;
    },
    addRSSFeed(state, feed) {
      state.rssFeeds = feed;
    },
    summaryForArticle(state, article) {
      const newArticle = { ...state.summarizerFeed[article.key], summary: article.value };
      state.summarizerFeed = { ...state.summarizerFeed, [article.key]: newArticle };
    },
    setAPILimit(state, limit) {
      state.apiLimit = limit;
    },
    setSummarizerSummary(state, summary) {
      state.summarizerSummary = summary;
    },
    setAvailableSources(state, sources) {
      state.availableSources = sources;
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
        getBriefings().then((res) => {
          const { results } = res.data;
          commit('addRSSFeed', results);
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
          const summaryData = results.data;
          const decodedURL = decodeURIComponent(url);
          commit('summaryForArticle', { key: decodedURL, value: summaryData.summary });
          commit('setAPILimit', summaryData.api_limitation);
          resolve();
        }).catch((error) => {
          reject(error);
        });
      });
    },
    toggleSummarizerFeed({ state, dispatch, commit }, article) {
      return new Promise((resolve, reject) => {
        commit('addToSummarizerFeed', article);
        if (!state.summarizerFeed[article.url].summary) {
          dispatch('summarizeArticle', article.url).then((res) => { resolve(res); }).catch((res) => { reject(res); });
        }
      });
    },
    getContentSummary({ commit, getters }) {
      const contentForSummarizing = getters.articlesForSummarizer.map((article) => {
        return article.summary || article.content;
      });
      console.log(contentForSummarizing);
      getContentSummary(contentForSummarizing).then((results) => {
        commit('setSummarizerSummary', results.data.summary);
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
      // const filtered = mapped.filter(article => article.active);
      return mapped;
    },
    articleInSummarizerFeed: state => (url) => {
      return state.summarizerFeed[url];
    },
    summarizerSummary(state) {
      return state.summarizerSummary.reduce((prev, curr) => {
        let summary = prev;
        summary += curr;
        return summary;
      }, '');
    },
  },
});
