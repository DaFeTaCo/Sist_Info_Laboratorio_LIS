import { createRouter, createWebHistory } from 'vue-router'
import Inicio from '../views/Inicio.vue'
import Pacientes from '../views/Pacientes.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/inicio' },
    { path: '/inicio', name: 'Inicio', component: Inicio },
    { path: '/pacientes', name: 'Pacientes', component: Pacientes }
  ]
})

export default router
