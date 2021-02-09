import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import App from './App.vue';
import router from './router';

import 'bootstrap/dist/css/bootstrap.min.css';

import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primevue/resources/themes/vela-orange/theme.css';
import 'primeflex/primeflex.css';

createApp(App)
  .use(router)
  .use(PrimeVue)
  .mount('#app');
