<template>
  <aside class="menu">
    <p class="menu-label">
      Grouped By
    </p>
    <ul class="menu-list">
      <li>
        <a @click="toggleGrouping">{{views[viewIndex]}}</a>
      </li>
    </ul>
    <p class="menu-label">
      Keywords
    </p>
    <ul class="menu-list">
      <li v-for="keyword in keywords" :key="keyword">
        <button class="button is-white" @click="toggleSort(keyword)">{{keyword}}</button>
      </li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  props: ['keywords'],
  data() {
    return {
      viewIndex: 0,
      views: ['keywords', 'sources'],
    };
  },
  methods: {
    toggleGrouping() {
      this.viewIndex = this.nextViewIndex;
      this.toggleSort(this.views[this.viewIndex]);
    },
    toggleSort(sortKey) {
      this.$emit('sortChanged', sortKey);
    },
  },
  computed: {
    nextViewIndex() {
      if (this.viewIndex + 1 < this.views.length) {
        return this.viewIndex + 1;
      }
      return 0;
    },
  },
};
</script>

<style>

</style>
