<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="secondary--text font-weight-bold mb-3">
          {{ msg }}
          <span class="primary--text font-weight-bold mb-3">
            {{ name }}
          </span>
        </h1>
        <p class="secondary--text subheading">
          {{ subheading }} 
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'TheHeading',
  data: () => ({
    msg: 'Welcome to ',
    name: 'MyChef',
    subheading: 'We help you decide what to cook based on what you have in the kitchen',
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-family: Pacifico, sans-serif;
  font-size: 300%;
}
</style>
