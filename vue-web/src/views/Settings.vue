<template>
  <div>
    <div class="columns settings__override">
      <div clsas="column">Frequency
        <div class="field">
          <div class="control">
            <label
              v-for="option in ['AM', 'PM']"
              class="checkbox"
              style="margin-right: .5rem;"
              :key="option"
              >
              <input type="checkbox">
               {{option}}
            </label>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label class="label">Alternate Delivery Address</label>
          <div class="control">
            <input class="input" type="text" :placeholder="user.email">
          </div>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <label>
            <input type="checkbox" v-model="smmry">
            Include SMMRY warning: paid service
        </label>
        <label>
            <input type="number" v-model="articleLimit">
            Article Limit
        </label>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <strong>Available Sources</strong>
          <div v-for="source in availableSources" :key="source">
          <label class="checkbox">
            <input type="checkbox"/>
            {{source}}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Settings',
  data() {
    return {
      smmry: false,
    };
  },
  computed: {
    ...mapState('auth', {
      user: state => state.user,
      sources: state => state.sources,
      articleLimit: state => state.articleLimit,
      keywords: state => state.keywords,
      frequency: state => state.frequency,
    }),
    ...mapState({
      availableSources: state => state.availableSources,
    }),
  },
  mounted() {
  },
};
</script>

<style>
  .settings__override {
    margin-left: 1rem!important;
    margin-right: 0px!important;
  }

</style>
