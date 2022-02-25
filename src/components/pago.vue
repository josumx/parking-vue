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
          on:keyup.enter="keypad"
          v-model="boleto"
          prepend-icon="mdi-qrcode"
          large
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-card-text class="pa-0">
        <v-container grid-list-xs pa-1>
          <v-layout row wrap pa0>
            <v-flex xs3 v-for="(boton, index) in botones" :key="index">
              <v-btn
                block
                depressed
                large
                v-if="boton.color"
                v-on:click="keypad(boton.value)"
                :color="boton.color"
              >
                <v-icon v-if="boton.icon" dark>{{ boton.icon }}</v-icon>
                <template v-else>{{ boton.label }}</template>
              </v-btn>
            </v-flex>
            <v-flex xs4>
              <v-btn
                v-on:click="remove()"
                block
                depressed
                large
                color="warning"
              >
                <v-icon>mdi-backspace</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs4>
              <v-btn v-on:click="clear()" block depressed large color="error">
                <v-icon>mdi-close-octagon-outline</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs4>
              <v-btn
                block
                depressed
                large
                color="success"
                v-on:click="validatarifa()"
              >
                <v-icon>mdi-checkbox-marked-circle</v-icon>
              </v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-row>
    <tarifa
      :visible="showtarifa"
      @close="showtarifa = false"
      :mensaje="estatus"
    />
    <opciones
      :visible="showopciones"
      @close="showopciones = false"
      :mensaje="estatus"
    />
  </v-container>
</template>


<script>
import EventService from "@/services/ApiService.js";
import tarifa from "./tarifa.vue";
import opciones from "./opciones.vue";
import { SerialPort } from "serialport";
// const serialPort = require("serialport");

export default {
  name: "pago",
  data: () => ({
    boleto: "",
    estatus: "",
    showtarifa: false,
    showopciones: false,
    port: new SerialPort({
      path: "COM14",
      baudRate: 9600,
      autoOpen: false,
    }),
    botones: [
      { label: "1", value: "1", color: "normal" },
      { label: "2", value: "2", color: "normal" },
      { label: "3", value: "3", color: "normal" },
      { label: "F", value: "F", color: "primary" },
      { label: "4", value: "4", color: "normal" },
      { label: "5", value: "5", color: "normal" },
      { label: "6", value: "6", color: "normal" },
      { label: "E", value: "E", color: "primary" },
      { label: "7", value: "7", color: "normal" },
      { label: "8", value: "8", color: "normal" },
      { label: "9", value: "9", color: "normal" },
      { label: "D", value: "D", color: "primary" },
      { label: "A", value: "A", color: "primary" },
      { label: "0", value: "0", color: "normal" },
      { label: "B", value: "B", color: "primary" },
      { label: "C", value: "C", color: "primary" },
    ],
  }),
  created: function () {
    this.boleto = "A142F199E";
    this.showtarifa = false;
    this.showopciones = false;

    this.port.on("data", (data) => {
      console.log(data);
      this.validatarifaescaner(data.toString("ascii"));
    });

    const connect = () => {
      console.log("connecting");
      this.port.open((error) => {
        if (error) {
          console.log("connecting error");
          connect();
        } else {
          console.log("connecting ok");
        }
      });
    };
    this.port.on("close", () => {
      connect();
    });
    connect();
  },
  methods: {
    readSerial: function () {},
    clear: function () {
      this.boleto = "";
    },
    remove: function () {
      this.boleto = this.boleto.substr(0, this.boleto.length - 1);
    },
    keypad: function (value) {
      this.boleto = this.boleto + value;
      console.log(value);
    },
    validatarifa: async function () {
      const response = await EventService.getTarifa(this.boleto);
      this.estatus = response.data.estatus;
      console.log(tarifa);
      this.showtarifa = true;
    },
    validatarifaescaner: async function (string) {
      const response = await EventService.getTarifa(string);
      this.estatus = response.data.estatus;
      console.log(tarifa);
      this.showtarifa = true;
    },
    payoptions: async function () {
      this.activarPago();
      this.showopciones = true;
    },
    activarPago: async function () {
      this.port.write(Buffer.from([0x14, 0x01]));
      this.port.write(Buffer.from([0x14, 0x01]));
      this.port.write(Buffer.from([0x14, 0x01]));
      try {
        await new Promise((resolve, reject) => {
          let done = false;
          const cb = (data) => {
            if (data.toString("ascii") == "0") {
              resolve();
            } else {
              reject();
            }
            this.port.off("data", cb);
            done = true;
          };
          this.port.on("data", cb);
          setTimeout(() => {
            console.log("timeout");
            if (!done) {
              reject();
              this.port.off("data", cb);
            }
          }, 1000);
        });
        console.log("Ok");
      } catch (error) {
        console.log("Error", error);
      }
    },
  },
  components: {
    tarifa,
    opciones,
  },
};
/*

=> 110001000000  --  setup
=> 1101FFFF0000  --  setup max min


=> 1401 enable  ACK  00
Esperar evento <=  1003fde9
=> 1301F40001  -- SETEO COBRO ACK 100503
=> 13020001 producto despachadoDESPACHADO  ack => 00 
=> 1304  Mensaje de finalizacion de transaccion ACK  00 10 07 
=> 1400 DISABLE
*/
</script>

