<template>
  <v-dialog v-model="show" max-width="500px" persistent>
    <v-card>
      <v-toolbar color="primary" dark>Validacion</v-toolbar>
      <v-card-text>
        <div class="text-h2 pa-12">{{ mensaje }}</div>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn
          color="error"
          @click.stop="
            $parent.clear();
            show = false;
          "
          >Cancelar</v-btn
        >
        <v-btn
          v-if="(state = 'nopagado')"
          color="success"
          @click.stop="
            $parent.payoptions();
            show = false;
          "
          >Pagar</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["visible", "mensaje", "persistent", "pago", "estatus"],
  data: () => ({
    state: "",
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
  watch: {
    estatus: function (val) {
      console.log(val);
      this.state = val;
    },
  },
};
</script>
