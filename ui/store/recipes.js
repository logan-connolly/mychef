export const state = () => ({
  source: 1,
  page: 1,
  items: []
});

export const mutations = {
  SET_ITEMS(state, data) {
    state.items = data.items;
  },
  ADD_ITEMS(state, data) {
    state.items = [...state.items, ...data.items];
  },
  UPDATE_ITEMS(state, data) {
    state.items = data.hits;
  },
  SET_PAGE(state, pageNumber) {
    state.page = pageNumber;
  }
};

export const actions = {
  async loadRecipes({ commit, rootState }) {
    commit("SET_PAGE", 1);
    await this.$axios
      .get(
        `/sources/${rootState.recipes.source}/recipes/?page=${rootState.recipes.page}&size=8`
      )
      .then(res => {
        commit("SET_ITEMS", res.data);
      })
      .catch(error => console.log(error));
  },
  async updateRecipes({ commit, rootState, dispatch }) {
    const selected = rootState.ingredients.selected;
    if (selected.length === 0) {
      return dispatch("loadRecipes");
    }
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
  },
  async addRecipes({ commit, rootState }) {
    commit("SET_PAGE", rootState.recipes.page + 1);
    await this.$axios
      .get(
        `/sources/${rootState.recipes.source}/recipes/?page=${rootState.recipes.page}&size=8`
      )
      .then(res => {
        commit("ADD_ITEMS", res.data);
      })
      .catch(error => console.log(error));
  }
};
