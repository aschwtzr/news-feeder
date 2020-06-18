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
      state.sources = preferences.sources;
      state.articleLimit = preferences.articleLimit;
      state.keywords = preferences.keywords;
      state.frequency = preferences.frequency;
    },
  },
  getters: {
    hasSetPreferences(state) {
      const preferences = ['frequency', 'keywords', 'articleLimit', 'sources'];
      const filtered = preferences.filter(key => state[key]);
      return !!(filtered.length);
    },
  },
};

export default settings;
