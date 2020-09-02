<template>
  <div class="text-center">
    <v-alert type="error" v-if="erorred">
      There was an issue retrieving recipes.
    </v-alert>
    <v-alert type="warning" v-if="!loading && recipes == null">
      No recipes were found in the database.
    </v-alert>
    <v-row>
      <v-col
        v-for="(recipe, n) in recipes"
        :key="n"
        class="d-flex child-flex"
        cols="12" xl="3" lg="4" md="4" sm="6" xs="12"
      >
          <RecipeListCard :recipe="recipe"/>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import RecipeListCard from './RecipeListCard.vue';
const axios = require('axios');
const api_url = process.env.VUE_APP_API_URL;

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
      .get(`${api_url}/sources/1/recipes`)
      .then(response => (this.recipes = response.data))
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
  }
}
</script>
