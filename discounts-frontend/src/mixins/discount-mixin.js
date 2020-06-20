export default {
  async created() {
    await this.$store.dispatch('discount/getDiscounts');
    await this.$store.dispatch('category/getCategories');
    await this.$store.dispatch('subcategory/getSubcategories');
    await this.$store.dispatch('retailer/getRetailers');
  },
  computed: {
    discounts() {
      return this.$store.getters['discount/discounts'];
    },
    categories() {
      return this.$store.getters['category/categories'];
    },
    subcategories() {
      return this.$store.getters['subcategory/subcategories'];
    },
    retailers() {
      return this.$store.getters['retailer/retailers'];
    },
  },
};
