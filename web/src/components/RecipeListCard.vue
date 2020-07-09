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
              color="secondary"
              opacity="0.5">
              <v-row align="center">
                <v-col class="text-center">
                  <div class="my-2">
                    <h3 class="offwhite--text text-center ma-7">
                      {{ recipe.name }}
                    </h3>
                  </div>
                  <div class="my-2">
                    <v-btn
                      :href="recipe.url"
                      target="_blank"
                      color="primary">
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
  name: 'RecipeListCard', 
  props: ['recipe'],
  data: () => ({
    //
  }),
}
</script>
