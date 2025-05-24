import loginView from '../views/loginView.vue'
import HomeView from '../views/HomeView.vue'
import MetalPriceView from '../views/MetalPriceView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
      {
        path: '/login',
        name: 'login',
        component: loginView
      },
    {
      path: '/metal-price',
      name: 'metal-price',
      component: MetalPriceView
    },
  ],
})


export default router
