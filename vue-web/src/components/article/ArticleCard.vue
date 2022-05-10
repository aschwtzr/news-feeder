<template>
  <div class="card article-card__container">
    <header class="card-header" @click="expanded = !expanded" style="cursor: pointer;">
      <div class="card-header-title" style="display: block!important;">
        <div class="columns">
          <div class="column is-1">{{id}}</div>
          <div class="column is-2">{{formattedDate}}</div>
          <div class="column is-2">{{source}}</div>
          <div class="column">{{title}}</div>
        </div>
      </div>
      <div class="card-header-icon" aria-label="more options" >
        <span class="icon is-small">
          <i :class="`fas fa-angle-${expanded ? 'down' : 'right'}`"/>
        </span>
      </div>
    </header>
    <div class="card-content is-loading">
        <!-- v-if="!expanded" -->
      <div
        class="overflowing-text"
        style="cursor: pointer;"
        @click="expanded = !expanded">
        {{ summary }}
      </div>
      <div class="article-card__summary" v-show="expanded">
        <div class="article__keyword-container">
          NLTK:
          <div
            v-for="(keyword, index) in keywords"
            :key="`${keyword}-${index}-${id}`"
            >
            <button class="button is-white">{{`${keyword} `}}</button>
          </div>
        </div>
        <div class="article__keyword-container">
          NLP:
          <div
            v-for="(keyword, index) in nlp_kw"
            :key="`${keyword}-${index}-${id}`"
            >
            <button class="button is-white">{{`${keyword} `}}</button>
          </div>
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
            v-if="loading && button.title === 'Summarize'"
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
  props: ['title', 'url', 'content', 'date', 'summary', 'keywords', 'nlp_kw', 'id', 'showSourceInHeader', 'source'],
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
        callback: this.summarizeArticle,
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
        formatted = moment(this.date).format('MMMM Do YYYY, HH:mm');
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
    summarizeArticle() {
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
    margin: 0rem;
    /* height: 2.4rem; */
    /* overflow: hidden; */
    overflow: wrap;
    /* text-overflow: ellipsis; */
    text-align: start;
    /* white-space: nowrap; */
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

  .article__keyword-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
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
