import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import App from './App.vue';
import router from './router';

import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';
import 'primevue/resources/themes/vela-orange/theme.css';

createApp(App)
  .use(router)
  .use(PrimeVue)
  .mount('#app');
