<template>
  <v-app>
    <TheNavbar/>
    <v-main>
      <TheHeading/>
      <RecipeList/>
    </v-main>
  </v-app>
</template>

<script>
import TheNavbar from './components/TheNavbar.vue';
import TheHeading from './components/TheHeading.vue';
import RecipeList from './components/RecipeList.vue';

export default {
  name: 'App',
  components: {
    TheNavbar,
    TheHeading,
    RecipeList,
  },
  data: () => ({
    //
  }),
};
</script>
