<template>
  <div class="card__container">
    <header class="card-header" @click="expanded = !expanded" style="cursor: pointer;">
      <div class="card-header-title" style="display: block!important;">
        <div class="columns">
          <div v-for="(header, index) in headers" :key="`${content}-${index}-${id}`">
            <div :class="`column ${header.size}`">{{header.content}}</div>
          </div>
        </div>
      </div>
      <div class="card-header-icon" aria-label="more options" >
        <span class="icon is-small">
          <i :class="caratAngle"/>
        </span>
      </div>
    </header>
    <div class="card-content is-loading">
        <!-- v-if="!expanded" -->
      <div
        class="overflowing-text"
        style="cursor: pointer;"
        @click="expanded = !expanded">
        {{ preview }}
      </div>
      <div class="article__keyword-container" v-if="keywords.length">
        NLTK: <br>
        <span
          v-for="(keyword, index) in keywords"
          :key="`${keyword}-${index}-${id}`"
          :class="`tag ${keywordClass(keyword)}`"
          >
          {{keyword}}
        </span>
      </div>
      <div class="article__keyword-container" v-if="nlp_kw">
        NLP: <br>
        <span
          v-for="(keyword, index) in nlp_kw"
          :key="`${keyword}-${index}-${id}`"
          :class="`tag ${keywordClass(keyword)}`"
          >
          {{keyword}}
        </span>
      </div>
      <div class="article-card__summary" v-show="expanded">
        <div>
          <slot></slot>
          <!-- {{content}} -->
        </div>
      </div>
    </div>
      <footer class="card-footer" style="background-color: #F7F7FF; border: 1px solid #dbdbdb;">
        <a
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
        </a>
      </footer>
  </div>
</template>

<script>
import moment from 'moment';
import { mapMutations, mapActions, mapGetters } from 'vuex';

export default {
  props: ['headers', 'preview', 'nlp_kw', 'keywords', 'id', 'content', 'buttons', 'date', 'topic_kw'],
  components: {
  },
  data() {
    return {
      expanded: false,
      saved: false,
      summarize: false,
      loading: false,
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
    caratAngle() {
      return `fas fa-angle-${this.expanded ? 'down' : 'right'}`;
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
    keywordClass(keyword) {
      if (this.topic_kw && this.topic_kw.includes(keyword)) {
        return 'is-success';
      }
      return '';
    },
  },
};
</script>

<style scoped>
  .card__container {
    margin-bottom: 1.5rem;
    border: .75px solid rgb(121, 87, 213, .5);
  }
  .overflowing-text {
    margin: 0rem;
    /* height: 2.4rem; */
    /* overflow: hidden; */
    overflow: wrap;
    /* text-overflow: ellipsis; */
    text-align: start;
    /* white-space: nowrap; */
  }

  /* .article-card__footer-item {
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
  } */
</style>
