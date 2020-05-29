const auth = {
  namespaced: true,
  state: {
    user: undefined,
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
  },
};

export default auth;
