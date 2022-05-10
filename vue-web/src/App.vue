<template>
  <div>
    <news-feed-tabs v-if="user" style="background-color: #F7F7FF; z-index: 10;"/>
    <section class="section">
      <router-view style="" class="column"/>
    </section>
  </div>
</template>

<script>
// import firebase from 'firebase';
import { mapState, mapActions } from 'vuex';
import NewsFeedTabs from '@/components/NewsFeedTabs.vue';

export default {
  name: 'App',
  components: {
    NewsFeedTabs,
  },
  computed: {
    ...mapState('settings', {
      user: state => state.user,
    }),
  },
  methods: {
    ...mapActions({
      getAvailableSources: 'feeds/getAvailableSources',
    }),
  },
  mounted() {
    // this.getAvailableSources();
  },
};
</script>

<style lang="scss">
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    // text-align: center;
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
</style>
<!--  // @import "~buefy/src/scss/buefy";-->
