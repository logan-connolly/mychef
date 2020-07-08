<template>
  <v-row>
    <v-col cols="12" sm="6" offset-sm="3">
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
import RecipeListCard from './RecipeListCard.vue';
import mychef from '../api/mychef';

export default {
  name: 'RecipeList', 
  components: {
    RecipeListCard
  },
  data: () => ({
    recipes: mychef.getRecipes(),
  }),
}
</script>
