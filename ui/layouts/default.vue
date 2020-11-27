<template>
  <v-app>
    <TheNavbar/>
    <TheHeading/>
    <nuxt/>
  </v-app>
</template>

<script>
import TheNavbar from '@/components/TheNavbar.vue'
import TheHeading from '@/components/TheHeading.vue'

export default {
  components: {
    TheNavbar,
    TheHeading
  }
}
</script>

<style>
.v-application {
  margin: 0 auto;
}
</style>
