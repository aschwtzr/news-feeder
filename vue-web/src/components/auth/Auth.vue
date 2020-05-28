<template lang='html'>
  <div>
    <div id='firebaseui-auth-container'></div>
  </div>
</template>

<script>
import firebase from 'firebase';
import * as firebaseui from 'firebaseui';

export default {
  name: 'auth',
  mounted() {
    const uiConfig = {
      signInSuccessUrl: '/feed',
      signInOptions: [
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID,
      ],
    };
    const auth = firebase.auth();
    const ui = new firebaseui.auth.AuthUI(auth);
    ui.start('#firebaseui-auth-container', uiConfig);
  },
};
</script>
