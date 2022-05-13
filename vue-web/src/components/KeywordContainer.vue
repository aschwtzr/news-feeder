<template>
  <div>
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
  </div>
</template>

<script>
export default {

}
</script>

<style>

</style>