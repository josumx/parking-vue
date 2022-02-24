<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center"></div>

      <v-spacer></v-spacer>

      <v-btn href="#" target="_blank" text>
        <span class="mr-2">Strom MDA Parking System</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <pago />
    </v-main>
  </v-app>
</template>

<script>
import pago from "./components/pago";

export default {
  name: "App",

  components: {
    pago,
  },

  data: () => ({
    //
  }),
};
</script>
