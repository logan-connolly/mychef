<template>
  <v-main style="padding: 0px;">
    <IngredientInput/>
    <v-row>
      <v-col
        v-for="(recipe, n) in items"
        :key="n"
        class="d-flex child-flex"
        cols="12" xl="2" lg="3" md="4" sm="4" xs="12"
      >
        <RecipeCard :recipe="recipe"/>
      </v-col>
    </v-row>
  </v-main>
</template>

<script>
import IngredientInput from '@/components/IngredientInput.vue'
import RecipeCard from '@/components/RecipeCard.vue'
import { mapState } from 'vuex';

export default {
  layout: 'default',
  head() {
    return {
      title: 'Mychef - Recipes'
    }
  },
  computed: {
    ...mapState('recipes', ['items'])
  },
  created() {
    this.$store.dispatch('recipes/loadRecipes')
  }
}
</script>
