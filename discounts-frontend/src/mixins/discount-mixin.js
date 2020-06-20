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
  },
  methods: {
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.discounts[this.editedIndex], this.editedItem);
      } else {
        this.discounts.push(this.editedItem);
      }
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
