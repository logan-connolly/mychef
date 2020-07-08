<template>
  <v-app-bar
    app
    color="rgba(240,239,235,0.4)">

    <div class="d-flex align-center">
      <h3 class="primary--text font-weight-bold">
        MyChef
      </h3>
    </div>

    <v-spacer></v-spacer>

    <v-btn
      href="https://github.com/logan-connolly/mychef"
      target="_blank"
      color="primary"
      text>
      <span class="secondary--text mr-2">GitHub</span>
      <v-icon>mdi-open-in-new</v-icon>
    </v-btn>

  </v-app-bar>
</template>

<script>
export default {
  name: 'TheNavbar',
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
