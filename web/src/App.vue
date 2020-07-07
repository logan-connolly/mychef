<template>
  <div id="app">
    <TheHeading/>
    <RecipeList/>
  </div>
</template>

<script>
import TheHeading from './components/TheHeading.vue'
import RecipeList from './components/RecipeList.vue'

export default {
  name: 'App',
  components: {
    TheHeading,
    RecipeList
  }
}
</script>

<style>
#app {
  font-family: Montserrat, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
