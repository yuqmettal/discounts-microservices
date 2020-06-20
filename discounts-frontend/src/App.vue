<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
      </div>

      <v-spacer></v-spacer>

      <v-btn href="https://github.com/yuqmettal/discounts-microservices" target="_blank" text>
        <span class="mr-2">GitHub</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <Discounts />
    </v-main>
  </v-app>
</template>

<script>
import Discounts from './components/Discounts.vue';

export default {
  name: 'App',

  created() {
    this.$vuetify.theme.dark = true;
  },

  components: {
    Discounts,
  },

  data: () => ({
    //
  }),
};
</script>
