<template>
  <div class="tabs is-centered is-boxed">
    <ul v-for="option in tabOptions" :key="option.view">
      <li :class="isActive(option.view) ? 'is-active' : ''">
        <a @click="toggleView(option.view)">
          <span class="icon is-small"><i class="fas fa-image" aria-hidden="true"></i></span>
          <span>{{option.description}}</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapMutations, mapGetters } from 'vuex';
// TODO: add tabs for custom Google News
export default {
  name: 'NewsFeedTabs',
  data() {
    return {
      tabOptions: [{
        description: 'Briefings',
        view: 'briefings',
      },
      {
        description: 'World News',
        view: 'world',
      },
      {
        description: 'Summaries',
        view: 'summaries',
      },
      {
        description: 'Settings',
        view: 'settings',
      }],
    };
  },
  methods: {
    ...mapMutations({
      setNewsFeedView: 'setNewsFeedView',
    }),
    toggleView(view) {
      this.setNewsFeedView(view);
    },
    isActive(view) {
      return this.currentNewsFeedView === view;
    },
  },
  computed: {
    ...mapGetters({
      currentNewsFeedView: 'currentNewsFeedView',
    }),
  },
};
</script>

<style>
  .tabs {
    position: sticky;
    top: 0rem;
    z-index: 1000;
    background-color: white;
    padding-top: 1rem;
  }
</style>
