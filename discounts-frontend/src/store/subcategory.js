import { getData } from './connect';

export default {
  namespaced: true,
  state: {
    loading: false,
    hasErrors: false,
    subcategories: [],
  },
  getters: {
    subcategories: (state) => state.subcategories,
  },
  mutations: {
    loading(state) {
      state.hasErrors = false;
      state.loading = false;
      state.subcategories = [];
    },
    setError(state) {
      state.hasErrors = true;
      state.loading = false;
      state.subcategories = [];
    },
    setSubcategories(state, payload) {
      state.subcategories = payload;
      state.loading = false;
      state.hasErrors = false;
    },
  },
  actions: {
    async getSubcategories({ commit }) {
      commit('loading');
      const response = await getData(commit, 'partners', '/subcategory/', undefined, {});
      if (response.status !== 200) {
        commit('setError');
      } else {
        commit('setSubcategories', response.data);
      }
      return response;
    },
  },
};
