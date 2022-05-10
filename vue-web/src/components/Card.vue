<template>
  <div class="card article-card__container">
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
      <div class="article-card__summary" v-show="expanded">
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
        <div>
          <!-- <slot name="content"/> -->
          {{content}}
        </div>
      </div>
    </div>
      <footer class="card-footer" style="background-color: #F7F7FF; border: 1px solid #dbdbdb;">
        <button
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
        </button>
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
</style>
