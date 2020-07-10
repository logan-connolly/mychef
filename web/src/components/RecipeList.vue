<template>
  <v-row>
    <v-col cols="12">
      <v-container fluid>
        <v-row>
          <v-col 
            v-for="(recipe, n) in recipes"
            :key="n"
            class="d-flex child-flex"
            cols="4">
              <RecipeListCard :recipe="recipe"/>
          </v-col>
        </v-row>
      </v-container>
    </v-col>
  </v-row>
</template>

<script>
import RecipeListCard from './RecipeListCard.vue'
//import mychef from '../api/mychef';
const axios = require('axios')

export default {
  name: 'RecipeList', 
  components: {
    RecipeListCard
  },
  data: () => ({
    recipes: null,
    loading: true,
    erorred: false
  }),
  mounted () {
    axios
      .get('http://localhost:8002/api/v1/sources/1/recipes/')
      .then(response => (this.recipes = response.data))
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
  }
}
</script>
