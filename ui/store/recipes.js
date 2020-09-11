export const state = () => ({
  items: []
});

export const mutations = {
  SET_ITEMS(state, data) {
    state.items = data;
  }
};

export const actions = {
  async loadRecipes({ commit }) {
    await this.$axios
      .get("/sources/1/recipes/")
      .then(res => {
        commit("SET_ITEMS", res.data);
      })
      .catch(error => console.log(error));
  }
};
