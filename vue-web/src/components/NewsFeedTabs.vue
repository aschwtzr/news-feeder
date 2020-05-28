<template>
  <nav class="tabs is-centered is-boxed">
    <ul v-for="option in tabOptions" :key="option.view" class="container">
      <li :class="current === option.routeName ? 'is-active' : ''">
        <a @click="goTo(option.routeName)">
          <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
          <span>{{option.description}}</span>
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NewsFeedTabs',
  data() {
    return {
      current: '',
      tabOptions: [{
        description: 'Feed',
        routeName: 'feed',
      },
      {
        description: 'Summaries',
        routeName: 'summaries',
      },
      {
        description: 'Settings',
        routeName: 'settings',
      },
      {
        description: 'Admin',
        routeName: 'admin',
      }],
    };
  },
  methods: {
    goTo(name) {
      this.current = name;
      this.$router.push({ name });
    },
  },
  computed: {},
};
</script>

<style>
  .tabs {
    position: sticky;
    top: 0rem;
    z-index: 1000;
    background-color: white;
    padding-top: 1rem;
    margin-bottom: 0rem!important;
  }
  .tabs.is-boxed li.is-active a {
    background-color: #F7F7FF;
  }
</style>
