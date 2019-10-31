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
        {{ summary || content}}
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
      <footer
        class="card-footer"
        style="background-color: #F7F7FF;">
        <div
          v-for="button in buttons"
          :key="button.title"
          class="card-footer-item"
          :class="button.class()"
          @click="button.callback">
          <span
            v-if="(loading || summary) && button.title === 'Summarize'"
            class="icon is-small"
            @click="expanded = !expanded">
            <i
              :class="`mdi mdi-${loading ? 'loading loading-spinner' : 'check'}`"/>
          </span>
          <div v-else>
            {{button.title}}
          </div>
        </div>
      </footer>
  </div>
</template>

<script>
import { mapMutations, mapActions, mapGetters } from 'vuex';

export default {
  props: ['title', 'url', 'content', 'date', 'summary'],
  components: {
  },
  data() {
    return {
      expanded: false,
      saved: false,
      summarize: false,
      loading: false,
      buttons: [{
        title: 'Save',
        class: this.savedButtonClass,
        callback: this.toggleSaved,
      },
      {
        title: 'Summarize',
        class: this.footerSummarizeClass,
        callback: this.addToSummarizeFeed,
      },
      {
        title: 'View',
        class: this.viewButtonClass,
        callback: this.openArticle,
      }],
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
    ...mapGetters({
      articleInSummarizerFeed: 'articleInSummarizerFeed',
    }),
  },
  methods: {
    ...mapActions({
      summarizeArticle: 'summarizeArticle',
      toggleSummarizerFeed: 'toggleSummarizerFeed',
    }),
    summarizeURL(url) {
      const encodedURL = encodeURIComponent(url);
      this.loading = true;
      this.summarizeArticle(encodedURL);
    },
    ...mapMutations({
      addToSummarizerFeed: 'addToSummarizerFeed',
    }),
    openArticle() {
      window.open(this.url, '_blank');
    },
    toggleSaved() {
      this.saved = !this.saved;
      // TODO: saved vs summarize button workflow
      const article = {
        title: this.title,
        url: this.url,
        content: this.content,
        date: this.date,
      };
      this.addToSummarizerFeed(article);
    },
    addToSummarizeFeed() {
      this.summarize = !this.summarize;
      this.loading = true;
      console.log(this.loading);
      const article = {
        title: this.title,
        url: this.url,
        content: this.content,
        date: this.date,
      };
      this.toggleSummarizerFeed(article).then(() => {
        this.loading = false;
        console.log(this.loading);
      });
    },
    savedButtonClass() {
      return this.articleInSummarizerFeed(this.url) ? 'confirmed' : '';
    },
    viewButtonClass() {
      return { unavailable: !this.url };
    },
    footerSummarizeClass() {
      const outputClass = {
        'card-footer-item': true,
      };
      if (!this.url) {
        outputClass.unavailable = true;
      } else if (this.summary) {
        outputClass.confirmed = true;
      }
      return outputClass;
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

  .loading-spinner {
    animation:  1.5s linear infinite rotate;
  }

  @keyframes rotate {
    from {
      transform: rotate(0deg)
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
