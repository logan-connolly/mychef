import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify)

const vuetify = new Vuetify ({
  theme: {
    themes: {
      light: {
        primary: "#42b983",
        secondary: "#2c3e50",
        accent: "#A5DFC5",
        offwhite: "#F0EFEB",
      },
    },
  },
})

export default vuetify
