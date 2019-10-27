<template>
<!-- Duplicate of ArticleCard using Buefy components for comparison -->
  <b-collapse class="card  article-card__container" aria-id="contentIdForA11y3">
      <div
          slot="trigger"
          class="card-header"
          role="button"
          aria-controls="contentIdForA11y3">
          <p class="card-header-title">
              {{title}}
          </p>
          <p v-if="!expanded"
            class="overflowing-text">
            {{content}}
          </p>
          <a class="card-header-icon">
              <b-icon
                  :icon="!expanded ? 'menu-down' : 'menu-right'">
              </b-icon>
          </a>
      </div>
      <div class="card-content" v-show="expanded">
          <div class="content">
            {{content}} <br>
            source:<a :href="url">{{url}}</a>
            <time :datetime="formattedDate">{{formattedDate}}</time>
          </div>
      </div>
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
          @click="summarize = !summarize">
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
  </b-collapse>
</template>

<script>
export default {
  props: ['title', 'url', 'content', 'date'],
  data() {
    return {
      expanded: false,
      saved: false,
      summarize: false,
    };
  },
  computed: {
    formattedDate() {
      let formatted = '';
      if (this.date) {
        formatted = new Date(this.date).toString();
      } else {
        formatted = '';
      }
      return formatted;
    },
    footerSummarizeClass() {
      const outputClass = {
        'card-footer-item': true,
      };
      if (!this.url) {
        outputClass.unavailable = true;
      } else if (this.summarize) {
        outputClass.confirmed = true;
      }
      console.log(outputClass);
      return outputClass;
    },
  },
  methods: {
  },
};
</script>

<style scoped>
  .overflowing-text {
    /* width: 10em; */
    padding-top: .75rem;
    margin: 0rem;
    height: 2.4rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding: .75rem;
    min-width: 40vh;
  }

  .card-footer-item {
    cursor: pointer;
  }

  .article-card__container {
    margin-bottom: 1.5rem;
  }

  .content {
    text-align: initial;
  }

  .confirmed {
    background-color:rgba(70, 226, 117, 0.5);
  }

  .unavailable {
    opacity: 40%;
    cursor: default;
  }

  .unavailable:hover {
    opacity: 40%;
    cursor: default;
    background-color:rgb(255, 255, 255)!important;
  }

  .card-footer-item:hover {
    background-color:rgba(112, 70, 226, 0.5);
  }
</style>
