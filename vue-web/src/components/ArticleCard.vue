<template>
  <div class="card article-card__container">
    <header class="card-header">
      <p
        class="card-header-title"
        style="min-width: fit-content; width: 60vh;">
        {{title}}
      </p>
      <p v-if="!expanded"
        class="overflowing-text">
        {{content}}
      </p>
      <div class="card-header-icon" aria-label="more options">
        <span class="icon" @click="expanded = !expanded">
          <b-icon
            :icon="expanded ? 'chevron-down' : 'chevron-right'"
            size="is-small"
            >
          </b-icon>
        </span>
      </div>
    </header>
    <div class="card-content is-loading" v-show="expanded">
      <div class="content">
        {{content}} <br>
        source:<a :href="url">{{url}}</a>
        <br>
        <br>
        <time datetime="2016-1-1">{{formattedDate}}</time>
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
  </div>
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
