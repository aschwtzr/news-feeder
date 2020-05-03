<template>
  <section>
    <div class="columns">
      <div class="column is-full">
        <div class="media">
          <div class="media-left">
            <figure class="image is-128x128">
              <img :src="user.photo" class="is-rounded" alt="Placeholder image">
            </figure>
          </div>
          <div class="media-content">
            <p class="title is-4">{{user.name}}</p>
            <p class="subtitle is-6">{{user.email}}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="columns is-vcentered">
      <div class="column">Email Settings</div>
      <div class="column">
        <input class="input" name="email" type="text" :placeholder="user.email">
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
  </section>
</template>

<script>
import { mapState } from 'vuex';
import { getFeedSources } from '@/util/api';
import { getSources } from '../util/firebase';

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
    ...mapState({
      user: state => state.user,
    }),
  },
  mounted() {
    getFeedSources().then((results) => {
      this.sources = results.data.sources;
    });
    getSources();
  },
};
</script>

<style>

</style>
