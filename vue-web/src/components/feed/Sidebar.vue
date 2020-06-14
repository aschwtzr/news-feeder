<template>
  <aside class="menu">
    <p class="menu-label">
      Group By
    </p>
    <ul class="menu-list">
      <li>
        <a @click="toggleGrouping">{{views[nextViewIndex]}}</a>
      </li>
      <li v-for="keyword in keywords" :key="keyword">
        <a @click="toggleSort(keyword)">{{keyword}}</a>
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
      views: ['feed', 'keywords'],
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
