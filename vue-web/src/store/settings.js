import { updateUserSources } from '@/util/firebase';

const settings = {
  namespaced: true,
  state: {
    user: undefined,
    sources: undefined,
    articleLimit: undefined,
    keywords: undefined,
    frequency: undefined,
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
    updateUserSources({ commit }, params) {
      updateUserSources(params.sources, params.userId).then(() => commit('setUserPreferences', { sources: params.sources }));
    },
  },
};

export default settings;
