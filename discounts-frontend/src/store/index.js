import Vue from 'vue';
import Vuex from 'vuex';

import discountModule from './discount';
import categoryModule from './category';
import subcategoryModule from './subcategory';
import retailerModule from './retailer';
import brandModule from './brand';

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
    category: categoryModule,
    subcategory: subcategoryModule,
    retailer: retailerModule,
    brand: brandModule,
  },
});
