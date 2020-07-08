<template>
  <v-container>
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card
          class="mx-auto">
          <v-img 
            :src="recipe.image" 
            :alt="recipe.name"
            contain></v-img>
          <v-fade-transition>
            <v-overlay
              v-if="hover"
              absolute
              color="offwhite"
              opacity="0.9">
              <v-layout row justify-center>
                <h3
                  class="secondary--text text-center ma-7">
                  {{ recipe.name }}
                </h3>
                <v-btn 
                  :href="recipe.url"
                  color="primary">
                  See More
                </v-btn>
              </v-layout>
            </v-overlay>
          </v-fade-transition>
        </v-card>
      </template>
    </v-hover>
  </v-container>
</template>

<script>
export default {
  name: 'RecipeListCard', 
  props: ['recipe'],
  data: () => ({
    //
  }),
}
</script>
