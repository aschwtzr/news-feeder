<template>
  <card
    :headers="[
      { content: id, size:'is-one' },
      { content: date, size:'is-one' },
      { content: source, size:'is-one' },
      { content: title, size:'' },
    ]"
    :keywords="keywords"
    :id="id"
    :buttons="[{
      title: 'Source',
      class: () => '',
      callback: () => openArticle(url),
    },
    {
      title: 'Open',
      class: () => '',
      callback: () => openArticle(url),
    },
    {
      title: 'Extract Content',
      class: () => '',
      callback: extractContent,
    },
    {
      title: 'Extract Keywords',
      class: () => '',
      callback: () => openArticle(url),
    },
    {
      title: 'Extract Summary',
      class: () => '',
      callback: () => openArticle(url),
    },
    {
      title: 'Extract Features',
      class: () => '',
      callback: () => openArticle(url),
    }
    ]"
    >
    <div>
      {{raw_text}}
    </div>
    <br/>
    <div v-for="(event, idx) in pipelineEvents" :key="`pe_event_${idx}_${id}`">
      <div>{{event.operation}}</div>
      <div>{{event.input}}</div>
      <div>{{event.output}}</div>
      <br/>
    </div>
  </card>
</template>

<script>
import Card from '../Card.vue';
import { extractContent } from '../../util/api';

export default {
  name: 'PipelinesArticleCard',
  props: ['url', 'id', 'date', 'source', 'title', 'keywords', 'raw_text'],
  components: {
    Card,
  },
  data() {
    return {
      pipelineEvents: [],
    };
  },
  methods: {
    openArticle(url) {
      window.open(url, '_blank');
    },
    async extractContent() {
      /* eslint-disable func-names */
      /* eslint-disable prefer-arrow-callback */
      await extractContent({
        url: this.url,
        content: true,
      }).then(function (res) {
        this.pipelineEvents.push(res.data);
      }.bind(this));
    },
  },
};
</script>
<style>
</style>
