<template>
  <v-container class="pa-0">
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
  </v-container>
</template>

<script>
export default {
  name: 'TheNavbarAbout',
  data: () => ({
    dialog: false
  })
}
</script>
