import Vue from 'vue';
import Buefy from 'buefy';
import firebase from 'firebase';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';
import 'buefy/dist/buefy.css';
import firebaseConfig from './util/firebaseConfig';

Vue.use(Buefy);

Vue.config.productionTip = false;
new Vue({
  store,
  router,
  created() {
    firebase.initializeApp(firebaseConfig);
    if (!store.state.auth.user) {
      this.$router.push({ path: '/auth' });
    }
    firebase.auth().onAuthStateChanged((user) => {
      store.commit('auth/saveUserProfile', user);
      router.push('/');
    });
  },
  render: h => h(App),
}).$mount('#app');
