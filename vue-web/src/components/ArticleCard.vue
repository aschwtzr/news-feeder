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
        <span class="icon is-small" @click="expanded = !expanded">
          <i
            :class="`mdi mdi-${expanded ? 'chevron-down' : 'chevron-right'}`"/>
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
      <footer class="card-footer" style="background-color: #F7F7FF;">
        <div
          class="card-footer-item"
          :class="saved ? 'confirmed' : ''"
          @click="summarizeURL(url)">
          SMMRY
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
  </div>
</template>

<script>
import { mapMutations } from 'vuex';
import { getSummaryForURL } from '@/util/api';
// import ArticleCardFooter from '@/components/ArticleCardFooter.vue';

export default {
  props: ['title', 'url', 'content', 'date'],
  components: {
  },
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
      return outputClass;
    },
  },
  methods: {
    summarizeURL(url) {
      const encodedURL = encodeURIComponent(url);
      getSummaryForURL(encodedURL).then((results) => {
        console.log(results);
      });
    },
    ...mapMutations({
      addToSummarizerFeed: 'addToSummarizerFeed',
    }),
    summarizeClicked() {
      this.summarize = !this.summarize;
      const self = {
        title: this.title,
        url: this.url,
        content: this.content,
        date: this.date,
        active: this.summarize,
      };
      this.addToSummarizerFeed(self);
    },
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
    background-color:rgba(99, 180, 209, 0.5);
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
    background-color:rgba(121, 87, 213, 0.5);
  }
</style>
