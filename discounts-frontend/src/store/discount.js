import { getData } from './connect';

export default {
  namespaced: true,
  state: {
    loading: false,
    hasErrors: false,
    discounts: [],
  },
  getters: {
    discounts: (state) => state.discounts,
  },
  mutations: {
    loading(state) {
      state.hasErrors = false;
      state.loading = false;
      state.discounts = [];
    },
    setError(state) {
      state.hasErrors = true;
      state.loading = false;
      state.discounts = [];
    },
    setDiscounts(state, payload) {
      state.discounts = payload;
      state.loading = false;
      state.hasErrors = false;
    },
  },
  actions: {
    async getDiscounts({ commit }) {
      commit('loading');
      const response = await getData(commit, 'items', '/discount/', undefined, {});
      if (response.status !== 200) {
        commit('setError');
      } else {
        commit('setDiscounts', response.data);
      }
      return response;
    },
  },
};
