import Vue from 'vue';
import Buefy from 'buefy';
import firebase from 'firebase';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';
import firebaseConfig from './util/firebaseConfig';
import { getUserProfile } from './util/api';

Vue.use(Buefy);

Vue.config.productionTip = false;
new Vue({
  store,
  router,
  created() {
    firebase.initializeApp(firebaseConfig);
    if (!store.state.settings.user) {
      this.$router.push({ path: '/auth' });
    }
    firebase.auth().onAuthStateChanged((user) => {
      store.commit('settings/saveUserProfile', user);
      getUserProfile(user.uid).then((profile) => {
        store.commit('settings/setUserPreferences', profile);
        console.log(profile);
      }).catch((error) => {
        console.log(error);
      });
      router.push('/');
    });
  },
  render: h => h(App),
}).$mount('#app');
