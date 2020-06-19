<template>
  <v-container>
    <v-card class="mx-auto" outlined>
      <h1>Discounts</h1>
      <v-data-table
        :headers="headers"
        :items="discounts"
        class="elevation-1"
      ></v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'Discounts',
  async created() {
    await this.$store.dispatch('discount/getDiscounts');
  },
  computed: {
    discounts() {
      return this.$store.getters['discount/discounts'];
    },
  },
  data: () => ({
    headers: [{ text: 'Id', value: 'id' }],
  }),
};
</script>
