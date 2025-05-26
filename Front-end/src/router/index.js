import loginView from '../views/loginView.vue'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView.vue'
import MetalPriceView from '../views/MetalPriceView.vue'
import ExchangeView from '../views/ExchangeView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import MyPageView from '@/views/MyPageView.vue'
import UserDetailView from '@/views/UserDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: '밑고름: 홈' }
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
      meta: { title: '밑고름: 마이페이지' }
    },
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
    {
      path: '/metal-price',
      name: 'metal-price',
      component: MetalPriceView
    },
    {
    path: '/exchange',   
    name: 'exchange',
    component: ExchangeView   
  },
      {
      path: '/userdetail',
      name: 'UserDetail',
      component: UserDetailView,
      meta: { title: '밑고름: 회원정보수정' }
    },
  ],
})
router.afterEach((to, from) => {
  document.title = to.meta.title || '기본 타이틀';
});



export default router
