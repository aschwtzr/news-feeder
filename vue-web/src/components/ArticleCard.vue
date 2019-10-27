<template>
  <div class="card">
    <header class="card-header">
      <p
        class="card-header-title"
        style="min-width: fit-content; width: 60vh;">
        {{title}}
      </p>
      <p v-if="!expanded"
        class="overflowing-text">
        {{content}}
      </p>
      <div class="card-header-icon" aria-label="more options">
        <span class="icon" @click="expanded = !expanded">
          <b-icon
            :icon="expanded ? 'chevron-down' : 'chevron-right'"
            size="is-small"
            >
          </b-icon>
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
    <footer class="card-footer">
      <a href="#" class="card-footer-item">Save</a>
      <a href="#" v-show="url" class="card-footer-item">Summarize</a>
      <a :href="url" target="_blank" v-show="url" class="card-footer-item">View</a>
    </footer>
  </div>
</template>

<script>
export default {
  props: ['title', 'url', 'content', 'date'],
  data() {
    return {
      expanded: false,
    };
  },
  computed: {
    formattedDate() {
      let formatted;
      if (this.date) {
        formatted = new Date(this.date).toString();
      } else {
        formatted = '';
      }
      return formatted;
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

  .content {
    text-align: initial;
  }

  .card-footer-item:hover {
    background-color:rgba(112, 70, 226, 0.5);
  }
</style>
