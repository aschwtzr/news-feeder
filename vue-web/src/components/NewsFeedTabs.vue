<template>
  <div style="position: fixed; width: 100%;">
    <div class="tabs is-centered is-boxed">
      <ul>
        <li
          v-for="option in tabOptions"
          :class="current === option.routeName ? 'is-active' : ''"
          :key="option.view"
          >
          <a @click="goTo(option.routeName)">
            <span class="icon is-small">
              <i :class="`fas fa-${option.icon}`" aria-hidden="true"/>
            </span>
            <span>{{option.description}}</span>
          </a>
        </li>
      </ul>
    </div>
  </div>
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
        icon: 'rss',
      },
      // will need to add these back in once the mvp is up
      {
        description: 'Summaries',
        routeName: 'summaries',
        icon: 'newspaper',
      },
      {
        description: 'Settings',
        routeName: 'settings',
        icon: 'cog',
      },
      {
        description: 'Articles',
        routeName: 'articles',
        icon: 'newspaper',
      },
      // {
      //   description: 'Admin',
      //   routeName: 'admin',
      //   icon: 'user-shield',
      // }
      ],
    };
  },
  methods: {
    goTo(name) {
      this.current = name;
      this.$router.push({ name });
    },
  },
  isActive(name) {
    return this.current === name;
  },
};
</script>

<style>
  /* .tabs {
    position: sticky;
    top: 0rem;
    z-index: 1000;
    background-color: white;
    padding-top: 1rem;
    margin-bottom: 0rem!important;
  } */
  .tabs.is-boxed li.is-active a {
    background-color: #F7F7FF;
  }
</style>
