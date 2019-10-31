<template>
  <div>
    <footer v-for="button in buttons" class="card-footer" style="background-color: #F7F7FF;" :key="button.title">
      <div
        class="card-footer-item"
        :class="saved ? 'confirmed' : ''"
        @click="saved = !saved">
        {{button.title}}
        </div>
      <div
        class="card-footer-item"
        :class="footerSummarizeClass"
        @click="addToSummarizeFeed">
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
  </div>
</template>

<script>
export default {
  name: 'ArticleCardButtons',
  computed: {
    buttons() {
      return [{
        title: 'save',
        callback: function() {
          
        }
      }]
    }
  }
}
</script>

<style>

</style>