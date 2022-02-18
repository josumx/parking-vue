<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">Bienvenido</h1>
        <h2 class="headline font-weight-bold mb-3">Hora : {{ hora }}</h2>
        <h2 class="headline font-weight-bold mb-3">
          {{ sensor }}
        </h2>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import EventService from "@/services/ApiService.js";
import { setIntervalAsync } from "set-interval-async/fixed";

export default {
  name: "entrada",
  data: function () {
    return {
      sensor: "Iniciando ... ",
      hora: Date(),
      mano: false,
      vehiculo: false,
    };
  },
  created: function () {
    var self = this;

    setIntervalAsync(() => self.getsensor(), 1000);
  },
  methods: {
    async getsensor() {
      const response = await EventService.getSensors();
      // this.hora = new Date();
      if (response === false) {
        this.sensor = "Error";
        return "";
      } else {
        if (response.data.sensor) {
          if (response.data.boleto) {
            this.sensor = "Tome su boleto";
            if (this.mano == false) {
              EventService.getBoleto();
              EventService.open();
            }
            this.mano = true;
          } else {
            if (this.mano == false) {
              this.sensor = "Acerque su mano";
            }
          }
        } else {
          this.mano = false;
          this.sensor = "Vehiculo no presente";
        }
      }
    },
  },
};
// function timr() {
//   setTimeout(function () {
//     checkSensor();
//   }, 500);
//   // checkSensor();
// }
// checkSensor();
// entrada.checkstatus();
</script>
