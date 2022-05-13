<template>
  <section>
    <div class="container">
      <div class="columns">
        <div class="column">
          <input class="input" name="source" type="text" placeholder="source">
        </div>
      </div>
      <button>Go</button>
    </div>
  </section>
</template>

<script>
// import { getSources } from '../util/firebase';

export default {
  data() {
    return {
      uuid: undefined,
    };
  },
  methods: {
  },
  mounted() {
    const array = new Uint32Array(3);
    window.crypto.getRandomValues(array);
    this.uuid = array.reduce((prev, curr, idx) => {
      return `${curr}${idx === 0 ? prev : `-${prev}`}`;
    }, '');
  },
};
</script>

<style>

</style>
