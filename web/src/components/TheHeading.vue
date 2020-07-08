<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mt-5">
        <h1 class="secondary--text font-weight-bold mb-3">
          Welcome to 
          <span class="primary--text font-weight-bold mb-3">
            MyChef
          </span>
        </h1>
        <p class="secondary--text subheading mt-5">
          We help you decide what to cook based on what you have in the kitchen 
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'TheHeading',
  data: () => ({
    //
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-family: Pacifico, sans-serif;
  font-size: 300%;
}
p {
  font-size: 120%;
}
</style>
