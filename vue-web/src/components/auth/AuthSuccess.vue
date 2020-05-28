<template>
  <div>
    <h1>Signup succeeded</h1>
    <button @click='logOut'>Log out</button>
    <hr>
    <img :src="user.photo" style="height: 120px"> <br>
    <p>{{user.name}}</p>
    <p>{{user.email}}</p>
    <p>{{user.userId}}</p>
    <hr>
    <button @click="goToNF"> Go </button>
    <pre>{{user}}</pre>
  </div>
</template>

<script>
import firebase from 'firebase';
import { mapState, mapMutations } from 'vuex';
import { getUserProfile, getUserPreferences } from '../../util/firebase';

export default {
  computed: {
    ...mapState({
      user: state => state.user,
    }),
  },
  methods: {
    ...mapMutations({
      saveUserProfile: 'saveUserProfile',
    }),
    logOut() {
      firebase.auth().signOut();
    },
    goToNF() {
      this.$router.push({ path: '/feed' });
    },
  },
  created() {
    const user = firebase.auth().currentUser;
    if (user) {
      this.saveUserProfile(user);
      getUserProfile(user);
      getUserPreferences(user.uid).then((preferences) => {
        console.log(preferences);
      }).catch((error) => {
        console.log(error);
      });
    }
  },
};
</script>
