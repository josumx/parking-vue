<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/strommda.jpg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Pago</h1>
        <h2 class="headline font-weight-bold mb-3">Escanee su boleto</h2>
        <v-text-field
          label="No. de boleto"
          placeholder="Escanee su boleto"
          on:keyup.enter="onEnter"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "parkingPago",
  data: () => ({}),
  methods: {
    onEnter: function (e) {
      console.log(e);
    },
  },
};
</script>
