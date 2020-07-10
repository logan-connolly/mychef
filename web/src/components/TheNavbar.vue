<template>
  <v-app-bar
    app
    flat
    dense
    color="white"
  >
    <v-spacer></v-spacer>

    <v-btn
      @click.stop="dialog = true"
      color="primary"
      text>
      <span class="secondary--text mr-2">About</span>
      <v-icon>mdi-information-outline</v-icon>
    </v-btn>

    <v-dialog
      v-model="dialog"
      max-width="500"
    >
      <v-card>
        <v-card-title class="headline font-weight-bold">Why MyChef</v-card-title>

        <v-card-text class="headline font-weight-light">
          We put all your favorite plant-based recipes in one place. On top of that, we recommend what to make based on what you have at home. No Ads, no tracking, just helping you decide what to make.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
export default {
  name: 'TheNavbar',
  data: () => ({
    dialog: false
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  font-family: Pacifico, sans-serif;
}
</style>
