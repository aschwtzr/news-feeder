<template lang='html'>
  <div>
    <div id='firebaseui-auth-container'></div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';
import firebase from 'firebase';
import * as firebaseui from 'firebaseui';
import { getUserProfile, getUserPreferences } from '../../util/firebase';

export default {
  name: 'auth',
  methods: {
    ...mapMutations('auth', {
      saveUserProfile: 'saveUserProfile',
    }),
  },
  mounted() {
    const uiConfig = {
      signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID,
      ],
      callbacks: {
        signInSuccessWithAuthResult: function (authResult) {
          const { user } = authResult;
          this.saveUserProfile(user);
          getUserProfile(user);
          getUserPreferences(user.uid);
          this.$router.push('/feed');
          return false;
        }.bind(this),
      },
    };
    const auth = firebase.auth();
    const ui = new firebaseui.auth.AuthUI(auth);

    if (auth.currentUser) {
      const user = auth.currentUser;
      this.saveUserProfile(user);
      getUserProfile(user);
      getUserPreferences(user.uid).then((preferences) => {
        console.log(preferences);
        this.$router.push({ path: '/' });
      }).catch((error) => {
        console.log(error);
      });
    } else ui.start('#firebaseui-auth-container', uiConfig);
  },
};
</script>
