import { getData } from './connect';

export default {
  namespaced: true,
  state: {
    loading: false,
    hasErrors: false,
    brands: [],
  },
  getters: {
    brands: (state) => state.brands,
  },
  mutations: {
    loading(state) {
      state.hasErrors = false;
      state.loading = false;
      state.brands = [];
    },
    setError(state) {
      state.hasErrors = true;
      state.loading = false;
      state.brands = [];
    },
    setBrands(state, payload) {
      state.brands = payload;
      state.loading = false;
      state.hasErrors = false;
    },
  },
  actions: {
    async getBrands({ commit }) {
      commit('loading');
      const response = await getData(commit, 'items', '/brand/', undefined, {});
      if (response.status !== 200) {
        commit('setError');
      } else {
        commit('setBrands', response.data);
      }
      return response;
    },
  },
};
