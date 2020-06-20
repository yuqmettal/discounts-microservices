import { getData } from './connect';

export default {
  namespaced: true,
  state: {
    loading: false,
    hasErrors: false,
    categories: [],
  },
  getters: {
    categories: (state) => state.categories,
  },
  mutations: {
    loading(state) {
      state.hasErrors = false;
      state.loading = false;
      state.categories = [];
    },
    setError(state) {
      state.hasErrors = true;
      state.loading = false;
      state.categories = [];
    },
    setCategories(state, payload) {
      state.categories = payload;
      state.loading = false;
      state.hasErrors = false;
    },
  },
  actions: {
    async getCategories({ commit }) {
      commit('loading');
      const response = await getData(commit, 'partners', '/category/', undefined, {});
      if (response.status !== 200) {
        commit('setError');
      } else {
        commit('setCategories', response.data);
      }
      return response;
    },
  },
};
