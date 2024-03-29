import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
// import VueGeoLocation from 'vue-browser-geolocation'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'



const vuetify = createVuetify({
  components,
  directives,
})

// createApp(App).use(vuetify).use(router).provide('ws', ws).mount('#app')

createApp(App).use(vuetify).use(router).mount('#app')
