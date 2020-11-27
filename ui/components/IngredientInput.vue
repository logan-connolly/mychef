<template>
  <v-autocomplete
    v-model="selected"
    :items="items"
    item-text="ingredient"
    item-value="ingredient"
    label="Select ingredients you have"
    class="pb-6 pa-0"
    clearable
    chips
    deletable-chips
    full-width
    hide-details
    hide-no-data
    hide-selected
    multiple
    single-line
  ></v-autocomplete>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'IngredientInput',
  computed: {
    ...mapState('ingredients', ['items']),
    selected : {
      get() {
        return this.$store.state.ingredients.selected
      },
      set(items) {
        this.$store.dispatch('ingredients/updateSelected', items),
        this.$store.dispatch('recipes/loadRecipes')
      }
    }
  },
  created() {
    this.$store.dispatch('ingredients/loadIngredients')
  }
}
</script>

<style scoped>
.v-autocomplete {
  margin: 0 auto;
  width: 60%;
}
</style>
