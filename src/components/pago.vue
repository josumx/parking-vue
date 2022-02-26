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
                <br />
                <v-icon v-if="boton.icon" dark>{{ boton.icon }}</v-icon>
                <template v-else>{{ boton.label }}</template>
                <br />
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
    <br />
    <v-alert v-show="!estatusport" dense type="error">
      Nayax disconnected</v-alert
    >
    <v-alert v-show="estatusport" dense type="success">
      Nayax connected</v-alert
    >
    <v-alert dense type="info"> {{ estatus }}</v-alert>
    <v-alert dense type="info"> {{ mensaje }}</v-alert>

    <tarifa
      :visible="showtarifa"
      @close="showtarifa = false"
      :mensaje="mensaje"
      :estatus="estatus"
    />
    <opciones
      :visible="showopciones"
      @close="showopciones = false"
      :mensaje="estatus"
    />
  </v-container>
</template>

<style>
.v-btn {
  width: 36px;
  min-width: 36px;
}
</style>
<script>
import EventService from "@/services/ApiService.js";
import escanerservice from "@/services/escaner.js";
import tarifa from "./tarifa.vue";
import opciones from "./proceso.vue";
import { SerialPort } from "serialport";
const { ReadlineParser } = require("@serialport/parser-readline");

// const serialPort = require("serialport");

export default {
  name: "pago",
  data: () => ({
    boleto: "",
    estatus: "",
    estatus_pago: "inactivo",
    mensaje: "",
    showtarifa: false,
    showopciones: false,
    estatusport: false,
    port: new SerialPort({
      path: "COM1",
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
    escanerservice.connect();

    // this.port.on("data", (data) => {
    //   console.log(data.toString("ascii"));
    // });
    const parser = this.port.pipe(new ReadlineParser({ delimiter: "\r\n" }));
    parser.on("data", (data) => {
      this.process(data.trim());
    });

    const connect = () => {
      console.log("connecting");
      this.port.open(async (error) => {
        if (error) {
          console.log("connecting error");
          console.log(error);
          setTimeout(() => connect(), "3000");
        } else {
          console.log("connecting ok");

          this.estatusport = true;
        }
      });
    };
    this.port.on("close", () => {
      this.estatusport = false;
      connect();
    });
    connect();
  },
  methods: {
    enviar: async function (comando) {
      console.log("Enviamos", comando);
      await this.sleep(500);
      this.port.write(
        Buffer.from(comando.split(" ").map((hex) => parseInt(hex, 16)))
      );
    },
    process: async function (data) {
      // validar estado.
      console.log("Recibimos", data);
      switch (this.estatus_pago) {
        case "inactivo":
          break;
        case "activando":
          if (data == "00") {
            this.estatus_pago = "esperando_tarjeta";
            console.log(this.estatus_pago);
          }

          break;
        case "esperando_tarjeta":
          // en espera de que pasen tarjeta
          if (data == "10 03 FD E9") {
            // calcular tarifa
            let importe = 1.21;
            let centavos = importe * 100;
            const b3 = (centavos & 0x0000ff).toString(16);
            const b2 = ((centavos >> 8) & 0x0000ff).toString(16);
            const b1 = ((centavos >> 16) & 0x0000ff).toString(16);
            await this.enviar(`13 ${b1} ${b2} ${b3} 00 01`);
            this.estatus_pago = "esperando_cobro";
            console.log(this.estatus_pago);
          }
          break;
        case "esperando_cobro":
          // if (data == "10 05 00 14") {
          if (data.startsWith("10 05")) {
            await this.sleep(3000);
            // maquina muestra retir tarjeta
            await this.enviar("13 02 00 01");
            this.estatus_pago = "confirmando_despacho";
            console.log(this.estatus_pago);
          }
          break;
        case "confirmando_despacho":
          if (data == "00") {
            await this.sleep(3000);
            // maquina dice gracias
            await this.enviar("13 04");
            // this.port.write(Buffer.from([0x13, 0x04]));
            this.estatus_pago = "terminando";
            console.log(this.estatus_pago);
            return "";
          } else if (data == "FF") {
            await this.enviar("13 02 00 01");
            // await this.enviar("13 04");
            // await this.enviar("14 00");
            // this.estatus_pago = "desactivando";
            // console.log(this.estatus_pago);
          }
          break;
        case "terminando":
          if (data == "10 07") {
            await this.enviar("14 00");
            // this.port.write(Buffer.from([0x14, 0x00]));
            this.estatus_pago = "desactivando";
            console.log(this.estatus_pago);
          }
          break;
        case "desactivando":
          if (data == "00") {
            this.estatus_pago = "inactivo";
            console.log(this.estatus_pago);
          }
      }
      if (data == "10 04") {
        await this.enviar("14 00");

        this.estatus_pago = "desactivando";
        console.log(this.estatus_pago);
      }
    },
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
      const response = await EventService.getTarifaQR(string);
      this.estatus = response.data.estatus;
      let msg;
      switch (this.estatus) {
        case "nopagado":
          msg = "Boleto :" + response.cadena;
          msg = msg + "Tarifa :" + response.tarifa;
          break;
        case "pagado":
          msg = "Boleto ya pagado";
          break;
        case "invalido":
          msg = "Boleto inexistente";
          break;
      }
      this.mensaje = msg;
      console.log(tarifa);
      this.showtarifa = true;
    },
    payoptions: async function () {
      this.activarPago();
      this.showopciones = true;
    },
    desactivarPago: async function () {
      await this.enviar("14 00");
    },
    sleep: function (ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    activarPago: async function () {
      // 1) solicitar tarjeta
      await this.enviar("11 00 01 00 00 00");
      // this.port.write(Buffer.from([0x11, 0x00, 0x01, 0x00, 0x00, 0x00]));
      await this.enviar("11 01 ff ff 00 00");
      // this.port.write(Buffer.from([0x11, 0x01, 0xff, 0xff, 0x00, 0x00]));
      await this.enviar("14 01");
      // this.port.write(Buffer.from([0x14, 0x01]));
      this.estatus_pago = "activando";
      console.log(this.estatus_pago);
      // 2) esperar confirmacion
      // 3) mandar preset de cobro
      // 4) esperar confirmacion de banco.
      // 5) mando aviso producto despachado .

      // try {
      //   await new Promise((resolve, reject) => {
      //     let done = false;
      //     const cb = (data) => {
      //       if (data == "0") {
      //         resolve();
      //       } else {
      //         reject();
      //       }
      //       this.port.off("data", cb);
      //       done = true;
      //     };
      //     this.port.on("data", cb);
      //     setTimeout(() => {
      //       console.log("timeout");
      //       if (!done) {
      //         reject();
      //         this.port.off("data", cb);
      //       }
      //     }, 1000);
      //   });
      //   console.log("Ok");
      // } catch (error) {
      //   console.log("Error", error);
      // }
    },
  },
  components: {
    tarifa,
    opciones,
  },
};
/*

=> 0x11 0x00 0x01 0x00 0x00 0x00   --  setup
=> 0x11 0x01 0xFF 0xFF 0x00 0x00   --  setup max min

=> 1401 enable  ACK  00
Esperar evento <=  1003fde9
=> 0x13 0x00 0x00 0x14 0x00 0x01  -- SETEO COBRO ACK 10050014
=> 13020001 producto despachadoDESPACHADO  ack => 00 
=> 1304  Mensaje de finalizacion de transaccion ACK   10 07 
=> 1400 DISABLE

0x13 0x00 0x00 0x14 0x00 0x01

==== RESPUESTAS  === 
10 04 == CANCELACION DE OPERACION DESPUES DE ELEGIR PRODUCTO
10 03 FD E9 == ELIGA UN PRODUCTO  HAY QUE RESPONDER CON EL TOTAL 


inicio ** solo escaner 
en espera de solicitud de pago.
en espera de tarjeta.
en espera de pago.
en espera de finalizacion.


13 00 00 14 00 01
13 00 00 14 00 01
*/
</script>

