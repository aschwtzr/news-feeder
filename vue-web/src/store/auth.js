const auth = {
  namespaced: true,
  state: {
    user: undefined,
    sources: undefined,
    articleLimit: undefined,
    keywords: undefined,
    frequency: [],
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
      state.preferences = preferences;
    },
  },
};

export default auth;
