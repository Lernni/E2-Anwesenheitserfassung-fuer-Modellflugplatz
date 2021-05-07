import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Unicon from 'vue-unicons'
import { uniEditAlt, uniMinusCircle } from 'vue-unicons/dist/icons'

Unicon.add([uniEditAlt, uniMinusCircle])

createApp(App).use(Unicon).use(router).mount('#app')