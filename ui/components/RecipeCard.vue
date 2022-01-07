<template>
  <v-container>
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card id="recipe__card" class="mx-auto">
          <a :href="recipe.url">
            <v-img :src="recipe.image" :alt="recipe.name"></v-img>
          </a>
          <v-fade-transition>
            <v-overlay v-if="hover" absolute color="offwhite" opacity="0.8">
              <v-row align="center">
                <v-col class="text-center">
                  <div class="my-2">
                    <h3 class="secondary--text text-center ma-7">
                      {{ recipe.name }}
                    </h3>
                  </div>
                  <div class="my-2">
                    <v-btn :href="recipe.url" target="_blank" color="primary">
                      See More
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-overlay>
          </v-fade-transition>
        </v-card>
      </template>
    </v-hover>
  </v-container>
</template>

<script>
export default {
  name: 'RecipeCard',
  props: ['recipe'],
};
</script>

<style scoped>
#recipe__card {
  border: 3px solid;
  border-color: rgba(193, 200, 215, 0.3);
  box-shadow: 3px 3px 8px 0px rgba(0, 0, 0, 0.3);
}
</style>
