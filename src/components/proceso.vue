<template>
  <v-dialog v-model="show" max-width="500px">
    <v-alert type="info">Pago</v-alert>
    <v-card>
      Pago en proceso siga las instrucciones de la terminal Nayax
      <v-card-actions>
        <v-btn
          color="error"
          @click.stop="
            $parent.desactivarPago();
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
