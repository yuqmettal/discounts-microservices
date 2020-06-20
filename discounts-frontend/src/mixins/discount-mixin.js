export default {
  async created() {
    await this.$store.dispatch('discount/getDiscounts');
    await this.$store.dispatch('category/getCategories');
    await this.$store.dispatch('subcategory/getSubcategories');
    await this.$store.dispatch('retailer/getRetailers');
    await this.$store.dispatch('brand/getBrands');
  },
  computed: {
    discounts() {
      return this.$store.getters['discount/discounts'];
    },
    categories() {
      return this.$store.getters['category/categories'];
    },
    categoriesForSelect() {
      return this.categories.map((category) => ({ value: category.id, text: category.name }));
    },
    subcategories() {
      return this.$store.getters['subcategory/subcategories'];
    },
    subcategoriesForSelect() {
      return this.subcategories
        .map((subcategory) => ({ value: subcategory.id, text: subcategory.name }));
    },
    retailers() {
      return this.$store.getters['retailer/retailers'];
    },
    retailersForSelect() {
      return this.retailers
        .map((retailer) => ({ value: retailer.id, text: retailer.name }));
    },
    brands() {
      return this.$store.getters['brand/brands'];
    },
    brandsForSelect() {
      return this.brands
        .map((brand) => ({ value: brand.id, text: brand.name }));
    },
  },
  methods: {
    async save() {
      await this.$store.dispatch('discount/createDiscount', this.editedItem);
      this.close();
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = { ...this.defaultItem };
        this.editedIndex = -1;
      });
    },
    editItem(item) {
      this.editedIndex = this.discounts.indexOf(item);
      this.editedItem = { ...item };
      this.dialog = true;
    },
    deleteItem(item) {
      return item;
    },
  },
};
