import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap';
import router from './router';

import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';

Vue.use(Vuetify);
const vuetify = new Vuetify();

const app = createApp(App);

app.use(vuetify);
app.use(router);

app.mount('#app');
