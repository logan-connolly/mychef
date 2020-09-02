<template>
  <v-autocomplete
    v-model="selected"
    :items="ingredients"
    item-text="ingredient"
    item-value="id"
    label="Ingredients"
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
const axios = require('axios');
const api_url = process.env.VUE_APP_API_URL;

export default {
  name: 'IngredientForm', 
  data: () => ({
    selected: null,
    ingredients: null,
    loading: true,
    erorred: false
  }),
  mounted () {
    axios
      .get(`${api_url}/ingredients`)
      .then(response => (this.ingredients = response.data))
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
  }
}
</script>

<style scoped>
.v-input {
  margin: auto;
  max-width: 70%;
}
.v-text-field {
  padding-top: 0px;
  padding-bottom: 24px;
}
</style>
