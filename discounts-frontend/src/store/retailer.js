import { getData } from './connect';

export default {
  namespaced: true,
  state: {
    loading: false,
    hasErrors: false,
    retailers: [],
  },
  getters: {
    retailers: (state) => state.retailers,
  },
  mutations: {
    loading(state) {
      state.hasErrors = false;
      state.loading = false;
      state.retailers = [];
    },
    setError(state) {
      state.hasErrors = true;
      state.loading = false;
      state.retailers = [];
    },
    setRetailers(state, payload) {
      state.retailers = payload;
      state.loading = false;
      state.hasErrors = false;
    },
  },
  actions: {
    async getRetailers({ commit }) {
      commit('loading');
      const response = await getData(commit, 'partners', '/retailer/', undefined, {});
      if (response.status !== 200) {
        commit('setError');
      } else {
        commit('setRetailers', response.data);
      }
      return response;
    },
  },
};
