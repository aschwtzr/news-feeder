<template>
  <card
    :headers="[
      { content: id, size:'is-one' },
      { content: date, size:'is-one' },
      { content: source, size:'is-one' },
      { content: title, size:'' },
    ]"
    :preview="preview"
    :keywords="keywords"
    :nlp_kw="nlp_kw"
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
      callback: extractKeywords,
    },
    {
      title: 'Extract Summary',
      class: () => '',
      callback: extractSummary,
    },
    {
      title: 'Extract Features',
      class: () => '',
      callback: () => openArticle(url),
    }
    ]"
    >
    <div @click="showParagraphs = !showParagraphs">
      <button class="button">
        {{ showParagraphs ? 'Hide' : 'Show' }} Content
      </button>
      <div v-show="showParagraphs">
        <div v-for="(para, idx) in paragraphs" :key="`${id}-${para.substring(0, 10)}-${idx}`">
          <div>{{para}}</div>
          <br/>
        </div>
      <br/>
      </div>
    </div>
    <div v-for="(event, idx) in pipelineEvents" :key="`pe_event_${idx}_${id}`">
      <pipeline-event
        :operation="event.operation"
        :input="event.input"
        :output="event.output"
      />
    </div>
  </card>
</template>

<script>
import Card from '../Card.vue';
import PipelineEvent from './PipelineEvent.vue';
import { extractContent } from '../../util/api';

export default {
  name: 'PipelinesArticleCard',
  props: [
    'url',
    'id',
    'date',
    'source',
    'title',
    'keywords',
    'nlp_kw',
    'raw_text',
    'sourceId',
    'paragraphs',
    'events',
    'preview',
  ],
  components: {
    Card,
    PipelineEvent,
  },
  data() {
    return {
      pipelineEvents: [],
      showParagraphs: false,
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
        source_id: this.sourceId,
        url: this.url,
        content: true,
      }).then(function (res) {
        this.pipelineEvents = [...this.pipelineEvents, ...res.data];
        // this.pipelineEvents.push(res.data);
      }.bind(this));
    },
    async extractSummary() {
      /* eslint-disable func-names */
      /* eslint-disable prefer-arrow-callback */
      await extractContent({
        paragraphs: this.paragraphs,
        rawText: this.raw_text,
        summary: true,
      }).then(function (res) {
        this.pipelineEvents = [...this.pipelineEvents, ...res.data];
        // this.pipelineEvents.push(res.data);
      }.bind(this));
    },
    async extractKeywords() {
      /* eslint-disable func-names */
      /* eslint-disable prefer-arrow-callback */
      await extractContent({
        paragraphs: this.paragraphs,
        title: this.title,
        keywords: true,
      }).then(function (res) {
        this.pipelineEvents = [...this.pipelineEvents, ...res.data];
        // this.pipelineEvents.push(res.data);
      }.bind(this));
    },
  },
  mounted() {
    this.pipelineEvents = [...this.events];
  },
};
</script>
<style>
</style>
