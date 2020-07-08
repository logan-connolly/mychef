<template>
  <v-app>
    <v-main>
      <TheHeading/>
      <v-container ma-auto>
        <RecipeList/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import TheHeading from './components/TheHeading.vue';
import RecipeList from './components/RecipeList.vue';

export default {
  name: 'App',
  components: {
    TheHeading,
    RecipeList,
  },
  data: () => ({
    //
  }),
};
</script>
