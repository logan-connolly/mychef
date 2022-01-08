<template>
  <v-container>
    <v-row no-gutters v-if="items.length > 1">
      <v-col v-for="(recipe, n) in items" :key="n" cols="12" sm="4">
        <RecipeCard :recipe="recipe" />
      </v-col>
    </v-row>
    <div v-else-if="items.length === 1">
      <RecipeCard :recipe="items[0]" />
    </div>
    <div v-else class="d-flex justify-center">
      <h3>No recipes found</h3>
    </div>
    <v-btn @click="addMoreRecipes" id="hide" />
  </v-container>
</template>

<script>
import RecipeCard from "@/components/RecipeCard.vue";

export default {
  name: "RecipeList",
  props: ["items"],
  components: { RecipeCard },
  methods: {
    addMoreRecipes() {
      window.onscroll = () => {
        let bottomOfWindow =
          document.documentElement.scrollTop + window.innerHeight ==
          document.documentElement.offsetHeight;
        if (bottomOfWindow) {
          this.$store.dispatch("recipes/addRecipes");
        }
      };
    },
  },
  mounted() {
    this.addMoreRecipes();
  },
};
</script>

<style scoped>
#hide {
  visibility: hidden !important;
}
</style>
