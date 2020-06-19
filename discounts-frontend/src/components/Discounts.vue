<template>
  <v-container>
    <h1>Discounts</h1>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>
  </v-container>
</template>

<script>
export default {
  name: 'Discounts',
  data() {

  },
};
</script>
