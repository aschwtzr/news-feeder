<template>
  <div class="tile is-ancestor is-12">
    <div class="tile is-parent is-vertical">
      <span class="tile is-child">
        <div class="tile is-parent">
          <div class="tile is-child">{{operation}}</div>
          <button class="button tile is-child" @click="showInput = !showInput">Input</button>
          <div class="button tile is-child" @click="showOutput = !showOutput">Output</div>
        </div>
      </span>
      <div
        class="tile is-child"
        v-show="showInput"
        >
        {{input}}
      </div>
      <div
        class="tile is-child"
        v-show="showOutput"
        >
        {{output}}
      </div>
    </div>
    <br/>
  </div>
</template>
<script>
export default {
  name: 'PipelineEvent',
  props: ['operation', 'input', 'output'],
  data() {
    return {
      show: false,
      showInput: false,
      showOutput: false,
    };
  },
};
</script>
<style>
</style>
