export const state = () => ({
  page: 1,
  items: [],
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
  },
};

export const actions = {
  async loadRecipes({ commit, rootState }) {
    commit("SET_PAGE", 1);
    await this.$axios
      .get(`/api/recipes/?page=${rootState.recipes.page}&size=8`)
      .then((res) => {
        commit("SET_ITEMS", res.data);
      })
      .catch((error) => console.log(error));
  },

  async updateRecipes({ commit, rootState, dispatch }) {
    const selected = rootState.ingredients.selected;
    if (selected.length === 0) {
      return dispatch("loadRecipes");
    }

    const query = '"' + selected.join('" "') + '"';
    await this.$axios
      .get("/search", { params: { q: query } })
      .then((res) => {
        commit("UPDATE_ITEMS", res.data);
      })
      .catch((error) => console.log(error));
  },

  async addRecipes({ commit, rootState }) {
    commit("SET_PAGE", rootState.recipes.page + 1);
    await this.$axios
      .get(`/api/recipes/?page=${rootState.recipes.page}&size=8`)
      .then((res) => {
        if (res.data.items.length === 0) {
          commit("SET_PAGE", rootState.recipes.page - 1);
        } else {
          commit("ADD_ITEMS", res.data);
        }
      })
      .catch((error) => console.log(error));
  },
};
