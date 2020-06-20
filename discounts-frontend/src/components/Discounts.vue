<template>
  <v-container>
    <v-card class="mx-auto" outlined>
      <v-data-table :headers="headers" :items="discounts" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat color="black">
            <v-toolbar-title>Descuentos</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">Nuevo</v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">Descuento</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12" sm="12" md="12">
                        <v-text-field v-model="editedItem.discount.name" label="Nombre" required />
                      </v-col>
                      <v-col cols="12" sm="12" md="12">
                        <v-text-field
                          v-model="editedItem.discount.description"
                          label="Descripcion"
                        />
                      </v-col>
                      <v-col cols="12" sm="12" md="12">
                        <v-select
                          v-model="editedItem.categories"
                          :items="categoriesForSelect"
                          label="Categorias"
                          multiple
                          chips
                          hint="Selecciona las categorias que aplicaran descuento"
                          persistent-hint
                          deletable-chips
                        />
                      </v-col>
                      <v-col cols="12" sm="12" md="12">
                        <v-select
                          v-model="editedItem.subcategories"
                          :items="subcategoriesForSelect"
                          label="Subcategorias"
                          multiple
                          chips
                          hint="Selecciona las subcategorias que aplicaran descuento"
                          persistent-hint
                          deletable-chips
                        />
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                  <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize">Reset</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import discountMixin from '../mixins/discount-mixin';

export default {
  name: 'Discounts',
  mixins: [discountMixin],
  data: () => ({
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fecha Inicio', value: 'start_date' },
      { text: 'Fecha Fin', value: 'end_date' },
      { text: 'Por clientes', value: 'by_clients' },
      { text: '', value: 'actions', sortable: false },
    ],
    editedIndex: -1,
    editedItem: {
      discount: {
        name: '',
        description: '',
        start_date: '2020-06-20',
        end_date: '2020-06-20',
        calendarized: false,
        priority: 0,
        discount: 0,
        retailer_id: 0,
        by_categories: false,
        by_subcategories: false,
        by_brands: false,
        by_products: false,
        by_clients: false,
        to_prime_clients: false,
        free_shipping: false,
        free_shipping_amount: 0,
        according_deliver_day: false,
        according_order_day: false,
        order_and_deliver_same_day: false,
      },
      categories: [],
      subcategories: [],
      brands: [],
      products: [],
    },
    defaultItem: {
      discount: {
        name: '',
        description: '',
        start_date: '2020-06-20',
        end_date: '2020-06-20',
        calendarized: false,
        priority: 0,
        discount: 0,
        retailer_id: 0,
        by_categories: false,
        by_subcategories: false,
        by_brands: false,
        by_products: false,
        by_clients: false,
        to_prime_clients: false,
        free_shipping: false,
        free_shipping_amount: 0,
        according_deliver_day: false,
        according_order_day: false,
        order_and_deliver_same_day: false,
      },
      categories: [],
      subcategories: [],
      brands: [],
      products: [],
    },
  }),
};
</script>
