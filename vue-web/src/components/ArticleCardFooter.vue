<template>
  <div>
    <div
      class="card-footer-item"
      :class="saved ? 'confirmed' : ''"
      @click="saved = !saved">
      Share
      </div>
    <div
      class="card-footer-item"
      v-bind:class="footerSummarizeClass"
      @click="summarize">
      Summarize
      </div>
    <a
      :href="url"
      target="_blank"
      class="card-footer-item"
      :class="{ unavailable: !url}">
      View
      </a>
  </div>
</template>

<script>
export default {
  name: 'ArticleCardFooter',
  data() {
    return {
      saved: false,
      summarize: false,
    };
  },
  methods: {
    share() {
      this.$emit('share')
    },
    summarize() {
      this.summarize = !this.summarize;
      // summarize acts as a flag for the state of the article: i.e. whether it's being added or removed
      this.$emit('summarize', this.summarize)
    },
  },
};
</script>

<style>

</style>
