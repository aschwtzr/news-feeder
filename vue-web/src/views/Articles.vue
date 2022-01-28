<template>
  <!-- <div class=""> -->
    <div class="columns">
      <div class="column">
        <div class="table-container">
          <table class="table tableFixHead
            is-bordered is-striped is-narrow
            is-hoverable is-fullwidth"
            >
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Title</th>
                <th>Source</th>
                <th>KW</th>
                <th>NLP KW</th>
                <th>Summary</th>
                <th>Raw Text</th>
              </tr>
            </thead>
              <tbody>
                <tr v-for="article in articles" :key="article.id">
                  <td>{{article.id}}</td>
                  <td>{{article.date}}</td>
                  <td>{{article.title}}</td>
                  <td>{{article.source}}</td>
                  <td>{{article.keywords}}</td>
                  <td>{{article.nlp_kw}}</td>
                  <td>{{article.summary}}</td>
                  <td>{{article.raw_text}}</td>
                </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  <!-- </div> -->
</template>

<script>
import {
  mapActions,
  mapState,
} from 'vuex';

export default {
  data() {
    return {};
  },
  methods: {
    ...mapActions({
      getArticles: 'feeds/getArticles',
    }),
  },
  computed: {
    ...mapState('feeds', {
      articles: state => state.articles,
    }),
  },
  mounted() {
    if (this.articles.length < 1) {
      this.getArticles();
    }
  },
};
</script>

<style>
  .tableFixHead          { overflow: auto; height: calc(100vh - 60px); display: block; }
  .tableFixHead thead th { position: sticky; top: 0; z-index: 1; }

  /* Just common table stuff. Really. */
  table  { border-collapse: collapse; width: 100%; }
  th, td { padding: 8px 16px; }
  th     { background:#eee; }
</style>
