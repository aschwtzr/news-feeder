<template>
  <div class="columns is-marginless is-centered">
    <div clsas="column">
      <p class="help is-success" v-if="!hasSetPreferences">
        Looks like you haven't set any preferences.
      </p>
      <div class="field">
          <label class="label">
            Daily Email Summary
          </label>
          <div class="control">
          <label>
            <input type="checkbox" v-model="email">
            sign me up
            <!-- 🌍 🌎 🌏 -->
          </label>
        </div>
      </div>
      <div class="field">
        <div class="label">
          Feed Sources
        </div>
        <div
          v-for="source in mergedSources"
          style="display: flex; flex-direction: column;"
          :key="source.key"
          >
          <div class="control" @click="toggleSource(source.key, source.id)">
            <label>
              <input type="checkbox" :checked="source.active"/>
              {{source.description}}
            </label>
          </div>
        </div>
        <div style="display: flex; flex-direction: column;">
          <label class="label">Create News Feed</label>
          <div class="field has-addons" >
            <div class="control">
              <input class="input" type="text" placeholder="search query">
            </div>
            <div class="control">
              <a class="button is-primary">
                Create
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="field">
        <div class="label">
          Frequency
        </div>
        <div class="control" style="display: flex; flex-direction: row; justify-content: center;">
          <label
            v-for="option in ['AM', 'PM']"
            style="margin-right: .5rem;"
            :key="option"
            >
            <input type="checkbox">
              {{option}}
          </label>
        </div>
      </div>
      <div class="field" >
        <label class="label">
            Article Limit
            <div
            class="control"
            style="display: flex; flex-direction: row; justify-content: center;"
            >
            <input type="number" v-model="articleLimit">
            </div>
        </label>
      </div>
      <div style="display: flex; flex-direction: column;">
        <label class="label">Alternate Delivery Address</label>
        <div class="field has-addons" >
          <div class="control">
            <input class="input" type="text" placeholder="alias@tafka.io">
          </div>
            <div class="control">
              <a class="button is-primary">
                Update
              </a>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import { updateUserSources } from '@/util/firebase';

export default {
  name: 'Settings',
  data() {
    return {
      email: false,
      smmry: false,
    };
  },
  computed: {
    ...mapState('settings', {
      user: state => state.user,
      sources: state => state.sources,
      articleLimit: state => state.articleLimit,
      keywords: state => state.keywords,
      frequency: state => state.frequency,
    }),
    ...mapState('feeds', {
      availableSources: state => state.availableSources,
    }),
    ...mapGetters({
      hasSetPreferences: 'settings/hasSetPreferences',
      mergedSources: 'mergedSources',
    }),
  },
  methods: {
    toggleSource(key, id) {
      if (this.sources && this.sources.includes(key)) {
        updateUserSources(this.sources.filter(arrKey => arrKey !== key), this.user.userId);
      } else if (this.sources) {
        updateUserSources([...this.sources, id], this.user.userId);
      } else {
        updateUserSources([id], this.user.userId);
      }
    },
  },
};
</script>

<style>
  .settings__override {
    margin-left: 1rem!important;
    margin-right: 0px!important;
  }

</style>
