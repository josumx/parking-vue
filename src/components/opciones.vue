<template>
  <v-dialog v-model="show" max-width="500px">
    <v-alert type="info">Seleccione una forma de pago</v-alert>
    <v-card>
      <v-btn size="x-large"> Tarjeta de Credito/Debito </v-btn>
      <v-btn disabled size="x-large"> CODI </v-btn>
      <v-btn disabled size="x-large"> Mercadopago </v-btn>
      <v-card-actions>
        <v-btn
          color="error"
          @click.stop="
            $parent.clear();
            show = false;
          "
          >Cancelar</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["visible", "mensaje"],
  data: () => ({
    estatus: "demo",
  }),

  computed: {
    show: {
      get() {
        return this.visible;
      },
      set(value) {
        if (!value) {
          this.$emit("close");
        }
      },
    },
  },
};
</script>
