<template>
  <div style="overflow-y: auto; height: 94vh;">
        <!-- TOPIC OVERVIEW -->
    <div class="columns">
      <div style="font-weight: bold;" class="column">{{title}}</div>
      <div class="column is-2">{{date}}</div>
    </div>
    <div>{{topic_summ}}</div>
    <br>
    <div class="columns is-multiline" style="width: 90vw;">
      <div
        v-for="kw in keywords"
        :key="`${kw}`"
        class="column is-narrow"
        style="padding: 0rem 0.75rem;"
        >
        {{kw}}
      </div>
    </div>
    <!-- <div>{{articles.length}}
        {{articles.map(art => art.source).join(', ')}}</div> -->
    <!-- <br> -->
        <!-- ARTICLES -->
    <div class="articles__horizontal_container columns is-multiline">
      <div v-for="article in articles" :key="article.id" class="column is-full">
        <card
          :headers="[
            { content: article.id, size:'is-one' },
            { content: article.date, size:'is-one' },
            { content: article.source, size:'is-one' },
            { content: article.title, size:'' },
          ]"
          :keywords="article.keywords"
          :id="article.id"
          :nlp_kw="article.nlp_kw"
          :content="article.raw_text"
          :topic_kw="keywords"
        />
        <!-- :preview="article.preview" -->
        <!-- <div class="columns is-multiline">
          <div class="column is-full">{{article.source}} - {{article.title}}</div>
          <div class="column is-full">
            <div
              :style="``"
              class="keywords__horizontal_container columns is-multiline"
              >
              <div
                v-for="kw in [...article.keywords, ...article.nlp_kw]" :key="`${kw}-${article.id}`"
                :style="`${computeKWStyle(kw, keywords)} padding: 0rem 0.75rem;`"
                class="column is-narrow">{{kw}}</div>
            </div>
          </div>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations, mapActions, mapState } from 'vuex';
import Card from '../components/Card.vue';

export default {
  props: [],
  components: {
    Card,
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
    ...mapState('topic', {
      articles: state => state.articles,
      date: state => state.date,
      keywords: state => state.keywords,
      nlp_kw: state => state.nlp_kw,
      title: state => state.title,
      topic_summ: state => state.topic_summ,
    }),
  },
  methods: {
    ...mapActions({
      toggleSummarizerFeed: 'toggleSummarizerFeed',
    }),
    ...mapMutations({
      addToSummarizerFeed: 'addToSummarizerFeed',
    }),
    computeKWStyle(kw, kwList) {
      return kwList.includes(kw) ? 'color: darkred;' : '';
    },
  },
};
</script>
<style>
</style>
