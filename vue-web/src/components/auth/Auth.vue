<template lang='html'>
  <div>
    <div id='firebaseui-auth-container'></div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';
import firebase from 'firebase';
import * as firebaseui from 'firebaseui';
import { getUserProfile } from '../../util/firebase';

export default {
  name: 'auth',
  methods: {
    ...mapMutations('auth', {
      saveUserProfile: 'saveUserProfile',
      setUserPreferences: 'setUserPreferences',
    }),
  },
  mounted() {
    const router = this.$router;
    const uiConfig = {
      signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID,
      ],
      callbacks: {
        signInSuccessWithAuthResult: (authResult) => {
          const { user } = authResult;
          this.saveUserProfile(user);
          getUserProfile(user.uid).then((profile) => {
            console.log(profile);
            this.setUserPreferences(profile);
            this.$router.push({ path: '/' });
          }).catch((error) => {
            console.log(error);
          });
          router.push('/feed');
          return false;
        },
      },
    };
    const auth = firebase.auth();
    const ui = new firebaseui.auth.AuthUI(auth);

    if (auth.currentUser) {
      const user = auth.currentUser;
      this.saveUserProfile(user);
      getUserProfile(user.uid).then((profile) => {
        this.setUserPreferences(profile);
        console.log(profile);
        this.$router.push({ path: '/' });
      }).catch((error) => {
        console.log(error);
      });
    } else ui.start('#firebaseui-auth-container', uiConfig);
  },
};
</script>
