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
  router,
  store,
  created() {
    firebase.initializeApp(firebaseConfig);
    firebase.auth().onAuthStateChanged((user) => {
      if (user && this.$router.path !== '/feed') {
        this.$router.push('/feed');
      } else {
        this.$router.push('/auth');
      }
    });
  },
  render: h => h(App),
}).$mount('#app');
