<template>
  <div>
    <!-- <div style="position: fixed;">
      <div class="media">
        <div class="media-left">
          <figure class="image is-32x32">
            <img :src="user.photo" class="is-rounded" alt="Placeholder image">
          </figure>
        </div>
        <div class="media-content">
          <p class="title is-4">{{user.name}}</p>
          <p class="subtitle is-6">{{user.email}}</p>
        </div>
      </div>
    </div> -->
    <div class="columns settings__override">
      <div clsas="column">Frequency
        <div class="field">
          <div class="control">
            <label class="checkbox" style="margin-right: .5rem;">
              <input type="checkbox">
              AM
            </label>
            /
            <label class="checkbox">
              <input type="checkbox">
              PM
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
          <div v-for="source in sources" :key="source">
          <label class="checkbox">
            <input type="checkbox" />
            {{source}}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { getFeedSources } from '@/util/api';

export default {
  name: 'Settings',
  data() {
    return {
      smmry: false,
      sources: [],
      active: {},
      articleLimit: 8,
    };
  },
  computed: {
    ...mapState('auth', {
      user: state => state.user,
    }),
  },
  mounted() {
    getFeedSources().then((results) => {
      this.sources = results.data.sources.map(source => source.description);
    });
  },
};
</script>

<style>
  .settings__override {
    margin-left: 1rem!important;
    margin-right: 0px!important;
  }

</style>
