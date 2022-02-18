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
        <h1 class="display-2 font-weight-bold mb-3">
          Bienvenido
        </h1>
        <h2 class="headline font-weight-bold mb-3">
          Acerca su mano al sensor para obtener boleto
        </h2>


      </v-col>


    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'HelloWorld',

    data: () => ({



    }),
  }
</script>
