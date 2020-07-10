<template>
  <v-app-bar
    app
    flat
    dense
    color="white"
  >
    <TheNavbarAbout/>

    <v-btn
      href="https://github.com/logan-connolly/mychef"
      target="_blank"
      color="primary"
      text>
      <span class="secondary--text mr-2">GitHub</span>
      <v-icon>mdi-github</v-icon>
    </v-btn>

  </v-app-bar>
</template>

<script>
import TheNavbarAbout from './TheNavbarAbout.vue';

export default {
  name: 'TheNavbar',
  components: {
    TheNavbarAbout
  },
  data: () => ({
    //
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  font-family: Pacifico, sans-serif;
}
</style>
