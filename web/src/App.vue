<template>
  <v-app>
    <TheNavbar/>
    <v-main>
      <TheHeading/>
      <IngredientForm/>
      <RecipeList/>
    </v-main>
  </v-app>
</template>

<script>
import TheNavbar from './components/TheNavbar.vue';
import TheHeading from './components/TheHeading.vue';
import IngredientForm from './components/IngredientForm.vue';
import RecipeList from './components/RecipeList.vue';

export default {
  name: 'App',
  components: {
    TheNavbar,
    TheHeading,
    IngredientForm,
    RecipeList,
  },
  data: () => ({
    //
  }),
};
</script>

<style scoped>
.v-main {
  margin: auto;
  max-width: 60%;
}
</style>
