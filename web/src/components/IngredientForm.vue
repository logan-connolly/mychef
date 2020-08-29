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
const axios = require('axios')

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
      .get('http://localhost:8002/api/v1/ingredients')
      .then(response => (this.ingredients = response.data))
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
  }
}
</script>
