import Vue from 'vue';
import Vuex from 'vuex';

import discountModule from './discount';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    discount: discountModule,
  },
});
