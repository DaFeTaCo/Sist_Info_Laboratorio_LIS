import { createRouter, createWebHistory } from 'vue-router'
import Inicio from '../views/Inicio.vue'
import Pacientes from '../views/Pacientes.vue'
import Resultados from '../views/Resultados.vue'
import Laboratoristas from '@/views/Laboratoristas.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/inicio' },
    { path: '/inicio', name: 'Inicio', component: Inicio },
    { path: '/resultados', component: Resultados },
    { path: '/pacientes', name: 'Pacientes', component: Pacientes },
    { path: '/laboratoristas', name: 'Laboratoristas', component: Laboratoristas }
  ]
})

export default router
