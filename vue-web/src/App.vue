<template>
  <div id="app" style="background-color: #F7F7FF;">
    <section>
        <news-feed-tabs v-if="user" />
        <router-view/>
    </section>
  </div>
</template>

<script>
import firebase from 'firebase';
import { mapState, mapMutations } from 'vuex';
import NewsFeedTabs from '@/components/NewsFeedTabs.vue';
import { getUserProfile, getUserPreferences } from './util/firebase';

export default {
  name: 'App',
  components: {
    NewsFeedTabs,
  },
  computed: {
    ...mapState('auth', {
      user: state => state.user,
    }),
  },
  methods: {
    ...mapMutations({
      saveUserProfile: 'auth/saveUserProfile',
    }),
  },
  mounted() {
    const user = firebase.auth().currentUser;
    if (user) {
      this.saveUserProfile(user);
      getUserProfile(user);
      getUserPreferences(user.uid).then((preferences) => {
        console.log(preferences);
      }).catch((error) => {
        console.log(error);
      });
    }
  },
};
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #63B4D1
    }
  }
}
@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
