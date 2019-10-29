<template>
  <footer class="card-footer">
    <div
      class="card-footer-item"
      :class="saved ? 'confirmed' : ''"
      @click="saved = !saved">
      Save
      </div>
    <div
      class="card-footer-item"
      v-bind:class="footerSummarizeClass"
      @click="summarizeClicked">
      Summarize
    </div>
    <a
      :href="url"
      target="_blank"
      class="card-footer-item"
      :class="{ unavailable: !url}">
      View
      </a>
  </footer>
</template>

<script>
export default {
  name: 'ArticleCardFooter',
};
</script>

<style>

</style>
