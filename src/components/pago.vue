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

// const { par  se } = require("path").default;
// import serialPort from "@/serialport";
const serialPort = require("serialport");

const port = new serialPort("COM12", { baudRate: 9600 });

const parser = new serialPort.parsers.Readline();

port.pipe(parser);

parser.on("data", (line) => {
  console.log("Arduino dice: " + line);
  port.write("Era una vez ");
});

// import SerialPort from "serialport";
// const SerialPort = require("serialport");

// const Readline = SerialPort.parsers.Readline;
// const port = new SerialPort("COM12", {
//   baudRate: 9600,
// });
// console.log(port);
// const parser = new Readline();
// port.pipe(parser);

// //Read Data
// parser.on("data", (line) => {
//   console.log(line);
// });

export default {
  name: "pago",
  data: () => ({
    boleto: "",
    estatus: "",
    showtarifa: false,
    showopciones: false,
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
    payoptions: async function () {
      this.showopciones = true;
    },
  },
  components: {
    tarifa,
    opciones,
  },
};
</script>


