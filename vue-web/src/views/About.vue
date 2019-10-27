<template>
  <div class="about">
    <h1>This is an about page</h1>
            <div class="block">
            <b-icon
                icon="account"
                size="is-small">
            </b-icon>
            <b-icon
                icon="home"
                size="is-small">
            </b-icon>
            <b-icon
                icon="view-dashboard"
                size="is-small">
            </b-icon>
        </div>
        <div>
          <b-button @click="clickMe">Click Me</b-button>
        </div>
  </div>
</template>

<script>
export default {
  methods: {
    clickMe() {
      this.$buefy.notification.open('Clicked!!');
    },
  },
};
</script>
