<template>
  <div>
    <div
      v-for="(source, index) in briefings"
      :key="`${source.description}-${index}`"
      class="feed-topic-source-wrapper">
      <strong v-if="groupedBySource"> {{source.description}} </strong>
      <div v-for="topic in source.topics" :key="topic.title">
        <Topic :topic="topic" :groupedBySource="groupedBySource"/>
        <br>
      </div>
    </div>
  </div>
</template>

<script>
import Topic from '@/components/feed/Topic.vue';

export default {
  name: 'NewsFeedArticleList',
  components: {
    Topic,
  },
  props: {
    groupedBySource: {
      type: Boolean,
      default: () => false,
      require: true,
    },
    briefings: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  methods: {},
  computed: {},
};
</script>

<style>
  .feed-topic-source-wrapper {
    margin-bottom: 3rem;
  }
</style>
