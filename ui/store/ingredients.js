export const state = () => ({
  items: [],
  selected: []
});

export const mutations = {
  SET_ITEMS(state, data) {
    state.items = data;
  },
  UPDATE_SELECTED(state, ingredients) {
    state.selected = ingredients;
  }
};

export const actions = {
  async loadIngredients({ commit }) {
    await this.$axios
      .get("/ingredients")
      .then(res => {
        commit("SET_ITEMS", res.data);
      })
      .catch(error => console.log(error));
  },
  updateSelected({ commit }, ingredients) {
    commit("UPDATE_SELECTED", ingredients);
  }
};
