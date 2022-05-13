<template>
  <div class="columns is-marginless is-centered">
    <div clsas="column is centered">
      <p class="help is-success" v-if="!hasSetPreferences">
        Looks like you haven't set any preferences.
      </p>
      <div class="field settings__field-container">
          <label class="label">
            Daily Email Briefing
          </label>
          <div class="control">
          <label>
            <input type="checkbox" :checked="briefingIsActive" @click="toogleBriefingIsActive">
            🌍 🌏 🌎
          </label>
        </div>
      </div>
      <div class="field settings__field-container">
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
      </div>
      <div style="display: flex; flex-direction: column;" class="settings__field-container">
        <p class="help is-success">
          Add keywords and a description, then click create.
        </p>
        <label class="label">Create News Feed</label>
        <div class="field has-addons" >
          <div class="control">
            <input
              class="input"
              type="text"
              placeholder="keyword"
              v-model="keywordInput"
              v-on:keyup.enter="addCreateFeedKeyword"
              >
          </div>
          <div class="control" @click="addCreateFeedKeyword">
            <a class="button is-info">
              Add
            </a>
          </div>
        </div>
        <div class="field has-addons" >
          <div class="control">
            <input
              class="input"
              type="text"
              placeholder="Description"
              v-model="createFeedDescription"
              >
          </div>
          <div class="control" @click="createFeedFirestore">
            <a class="button is-primary">
              Create
            </a>
          </div>
        </div>
        <div class="card" v-if="createFeedDescription || createFeedKeywords.length">
          <div class="card-content" style="max-width: 20vw;">
            <strong>
              {{createFeedDescription}}
            </strong>
            <div style="display: flex; flex-direction: row; flex-wrap: wrap;">
              <div
                v-for="keyword in createFeedKeywords"
                :key="keyword"
                style="padding-right: 1rem;"
                >
                {{keyword}}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="field settings__field-container" >
        <label class="label">
            Article Limit
            <div
            class="control"
            style="display: flex; flex-direction: row; justify-content: center;"
            >
            <input class="input" type="number" :value="articleLimit" @change="setLimit">
            </div>
        </label>
      </div>
      <div style="display: flex; flex-direction: column;">
        <label class="label">Alternate Delivery Address</label>
        <div class="field has-addons" >
          <div class="control">
            <input
              class="input"
              type="email"
              v-model="alternateEmailInput"
              v-on:keyup.enter="setEmail"
              placeholder="alias@newssumm.io"
              >
          </div>
            <div class="control" @click="setEmail">
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
import { mapState, mapGetters, mapActions } from 'vuex';

export default {
  name: 'Settings',
  data() {
    return {
      keywordInput: '',
      createFeedKeywords: [],
      createFeedDescription: '',
      alternateEmailInput: '',
    };
  },
  computed: {
    ...mapState('settings', {
      user: state => state.user,
      sources: state => state.sources,
      articleLimit: state => state.articleLimit,
      showKeywords: state => state.keywords,
      briefingFrequency: state => state.briefingFrequency,
      briefingIsActive: state => state.briefingIsActive,
      alternateEmail: state => state.alternateEmail,
    }),
    ...mapState('feeds', {
      availableSources: state => state.availableSources,
    }),
    ...mapGetters({
      hasSetPreferences: 'settings/hasSetPreferences',
      mergedSources: 'mergedSources',
    }),
    baseParams() {
      return {
        userId: this.user.userId,
      };
    },
  },
  methods: {
    ...mapActions({
      setUserSources: 'settings/setUserSources',
      setBriefingIsActive: 'settings/setBriefingIsActive',
      setArticleLimit: 'settings/setArticleLimit',
      createCustomFeed: 'settings/createCustomFeed',
      setAlternateEmail: 'settings/setAlternateEmail',
    }),
    createFeedFirestore() {
      const params = {
        ...this.baseParams,
        feedDescription: this.createFeedDescription,
        feedKeywords: this.createFeedKeywords,
      };
      if (!this.createFeedDescription || this.createFeedKeywords.length < 1) {
        // show alert https://bulma.io/documentation/elements/notification/
      } else {
        this.createCustomFeed(params);
      }
    },
    addCreateFeedKeyword() {
      this.createFeedKeywords.push(this.keywordInput);
      this.keywordInput = '';
    },
    toogleBriefingIsActive() {
      const params = { ...this.baseParams, briefingIsActive: !this.briefingIsActive };
      this.setBriefingIsActive(params);
    },
    setLimit(event) {
      const params = { ...this.baseParams, articleLimit: parseInt(event.target.value, 10) };
      this.setArticleLimit(params);
    },
    setEmail() {
      const params = { ...this.baseParams, alternateEmail: this.alternateEmailInput };
      this.setAlternateEmail(params);
    },
    toggleSource(key, id) {
      const params = this.baseParams;
      if (this.sources && this.sources.includes(id)) {
        params.sources = this.sources.filter(sourceId => sourceId !== id);
        this.setUserSources(params);
      } else if (this.sources) {
        params.sources = [...this.sources, id];
        this.setUserSources(params);
      } else {
        params.sources = [id];
        this.setUserSources(params);
      }
    },
    toggleFrequency(time) {
      const params = this.baseParams;
      if (this.briefingFrequency && this.briefingFrequency.includes(time)) {
        params.briefingFrequency = this.briefingFrequency.filter(key => key !== time);
        this.setBriefingFrequency(params);
      } else if (this.sources) {
        params.briefingFrequency = [...this.briefingFrequency, time];
        this.setBriefingFrequency(params);
      } else {
        params.briefingFrequency = [time];
        this.setBriefingFrequency(params);
      }
    },
  },
  mounted() {
    if (this.alternateEmail) {
      this.alternateEmailInput = this.alternateEmail;
    }
  },
};
</script>

<style>
  .settings__field-container {
    padding-bottom: 1rem;
  }
  .settings__override {
    margin-left: 1rem!important;
    margin-right: 0px!important;
  }

</style>
