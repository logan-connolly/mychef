<template>
  <v-main>
    <IngredientInput />
    <RecipeList :items="items" />
  </v-main>
</template>

<script>
import IngredientInput from '@/components/IngredientInput.vue';
import RecipeList from '@/components/RecipeList.vue';
import { mapState } from 'vuex';

export default {
  layout: 'default',
  components: { IngredientInput, RecipeList },
  computed: {
    ...mapState('recipes', ['items']),
  },
  head() {
    return {
      title: 'Mychef - Recipes',
    };
  },
  created() {
    this.$store.dispatch('recipes/loadRecipes');
  },
};
</script>
