import {
  setBriefingIsActive,
  setUserSources,
  setBriefingFrequency,
  setArticleLimit,
  setShowKeywords,
  createCustomFeed,
  setAlternateEmail,
} from '@/util/firebase';

const settings = {
  namespaced: true,
  state: {
    user: undefined,
    sources: undefined,
    articleLimit: undefined,
    showKeywords: undefined,
    briefingFrequency: undefined,
    briefingIsActive: undefined,
    alternateEmail: undefined,
  },
  mutations: {
    saveUserProfile(state, user) {
      state.user = {
        name: user.displayName,
        email: user.email,
        photo: user.photoURL,
        userId: user.uid,
      };
    },
    setUserPreferences(state, preferences) {
      Object.assign(state, preferences);
    },
  },
  getters: {
    hasSetPreferences(state) {
      const preferences = ['frequency', 'keywords', 'articleLimit', 'sources'];
      const filtered = preferences.filter(key => state[key]);
      return !!(filtered.length);
    },
  },
  actions: {
    setShowKeywords({ commit }, params) {
      setShowKeywords(params.sources, params.userId).then(() => commit('setUserPreferences', { showKeywords: params.showKeywords }));
    },
    setArticleLimit({ commit }, params) {
      setArticleLimit(params.articleLimit, params.userId).then(() => commit('setUserPreferences', { articleLimit: params.articleLimit }));
    },
    setUserSources({ commit }, params) {
      setUserSources(params.sources, params.userId).then(() => commit('setUserPreferences', { sources: params.sources }));
    },
    setBriefingIsActive({ commit }, params) {
      setBriefingIsActive(params.briefingIsActive, params.userId).then(() => commit('setUserPreferences', { briefingIsActive: params.briefingIsActive }));
    },
    setBriefingFrequency({ commit }, params) {
      setBriefingFrequency(params.briefingFrequency, params.userId).then(() => commit('setUserPreferences', { briefingFrequency: params.briefingFrequency }));
    },
    createCustomFeed({ commit }, params) {
      createCustomFeed(params.feedDescription, params.feedKeywords, params.userId).then(feedId => commit('setUserPreferences', { customFeeds: feedId }));
    },
    setAlternateEmail({ commit }, params) {
      setAlternateEmail(params.alternateEmail, params.userId).then(() => commit('setUserPreferences', { alternateEmail: params.alternateEmail }));
    },
  },
};

export default settings;
