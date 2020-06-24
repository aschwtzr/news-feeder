<template>
  <div class="card article-card__container">
    <header class="card-header" @click="expanded = !expanded" style="cursor: pointer;">
      <p class="card-header-title" style="">
        {{title}}
      </p>
      <div class="card-header-icon" aria-label="more options" >
        <span class="icon is-small">
          <i :class="`mdi mdi-${expanded ? 'chevron-down' : 'chevron-right'}`"/>
        </span>
      </div>
    </header>
    <div v-if="summary || content" class="card-content is-loading">
        <div
          v-if="!expanded"
          class="overflowing-text"
          style="cursor: pointer;"
          @click="expanded = !expanded">
          {{ summary || content }}
        </div>
      <div class="article-card__summary" v-show="expanded">
        <div style="padding-bottom: 1rem;">
          <time datetime="2016-1-1">{{formattedDate}}</time>
        </div>
        <div>
          {{content}}
        </div>
      </div>
    </div>
      <footer class="card-footer" style="background-color: #F7F7FF; border: 1px solid #dbdbdb;">
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
import moment from 'moment';
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
        formatted = moment(this.date).format('MMMM Do YYYY, HH:mm:ss');
      } else {
        formatted = '';
      }
      return formatted;
    },
    ...mapGetters({
      articleInSummarizerFeed: 'feeds/articleInSummarizerFeed',
    }),
  },
  methods: {
    ...mapActions({
      toggleSummarizerFeed: 'toggleSummarizerFeed',
    }),
    ...mapMutations({
      addToSummarizerFeed: 'addToSummarizerFeed',
    }),
    openArticle() {
      window.open(this.url, '_blank');
    },
    toggleSaved() {
      this.saved = !this.saved;
    },
    addToSummarizeFeed() {
    },
    savedButtonClass() {
      return this.articleInSummarizerFeed(this.url) ? 'article-card__confirmed' : '';
    },
    viewButtonClass() {
      return { unavailable: !this.url };
    },
    footerSummarizeClass() {
      const outputClass = {
        'article-card__footer-item': true,
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
    padding-top: .75rem;
    margin: 0rem;
    height: 2.4rem;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: .75rem;
    text-align: start;
  }

  .article-card__footer-item {
    cursor: pointer;
  }

  .article-card__container {
    margin-bottom: 1.5rem;
    border: .75px solid rgb(121, 87, 213, .5);
  }

  .article-card__summary {
    text-align: initial;
    display: flex;
    flex-direction: column;
  }

  .article-card__confirmed {
    background-color:rgba(99, 180, 209, 0.5);
  }

  .article-card__unavailable {
    opacity: 40%;
    cursor: default;
  }

  .article-card__unavailable:hover {
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
