export const state = () => ({
  items: []
});

export const mutations = {
  SET_ITEMS(state, data) {
    state.items = data;
  },
  UPDATE_ITEMS(state, data) {
    state.items = data.hits;
  }
};

export const actions = {
  async loadRecipes({ commit, rootState }) {
    const selected = rootState.ingredients.selected;
    if (selected.length == 0) {
      await this.$axios
        .get("/sources/1/recipes/?limit=18")
        .then(res => {
          commit("SET_ITEMS", res.data);
        })
        .catch(error => console.log(error));
    } else {
      await this.$axios
        .get("http://localhost:7700/indexes/recipes/search", {
          params: {
            q: selected.join(" ")
          }
        })
        .then(res => {
          commit("UPDATE_ITEMS", res.data);
        })
        .catch(error => console.log(error));
    }
  }
};
