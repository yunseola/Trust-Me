import loginView from '../views/loginView.vue'
import HomeView from '../views/HomeView.vue'
<<<<<<< HEAD
import SignUpView from '../views/SignUpView.vue'
=======
import MetalPriceView from '../views/MetalPriceView.vue'
>>>>>>> 1f2a099567a73e9aa1925d293987432bcb05c4d4
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: '밑고름: 홈' }
    },
<<<<<<< HEAD
    {
      path: '/login',
      name: 'login',
      component: loginView,
      meta: { title: '밑고름: 로그인' }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      meta: { title: '밑고름: 회원가입' }
    },

=======
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
>>>>>>> 1f2a099567a73e9aa1925d293987432bcb05c4d4
  ],
})
router.afterEach((to, from) => {
  document.title = to.meta.title || '기본 타이틀';
});



export default router
