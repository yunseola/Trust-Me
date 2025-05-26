import loginView from '../views/loginView.vue'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView.vue'
import MetalPriceView from '../views/MetalPriceView.vue'
import ExchangeView from '../views/ExchangeView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import MyPageView from '@/views/MyPageView.vue'
import UserDetailView from '@/views/UserDetailView.vue'
import introduceView from '@/views/introduceView.vue'
import IntroduceDetailView from '@/views/IntroduceDetailView.vue'
import IntroduceCompareView from '@/views/IntroduceCompareView.vue'
import RecommendationView from '@/views/RecommendationView.vue'

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
      path: '/introducecompare',
      name: 'introducecompare',
      component: IntroduceCompareView,
      meta: { title: '밑고름: 금융상품비교' }
    },
    {
      path: '/metal-price',
      name: 'metal-price',
      component: MetalPriceView,
      meta: { title: '밑고름: 금은시세' }
    },
     {
      path: '/introduce',
      name: 'introduce',
      component: introduceView,
      meta: { title: '밑고름: 금융상품소개' }
    },
    { path: '/introduce/:type/:fin_prdt_cd',
      name: 'IntroduceDetail',
      component: IntroduceDetailView,
      props: true,
    meta: { title: '밑고름: 금융상품상세' } },
    {
    path: '/exchange',   
    name: 'exchange',
    component: ExchangeView,   
    meta: { title: '밑고름: 환율정보' }
  },
      {
      path: '/userdetail',
      name: 'UserDetail',
      component: UserDetailView,
      meta: { title: '밑고름: 회원정보수정' }
    },
    {
    path: '/recommendation',   
    name: 'recommendation',
    component: RecommendationView,
    meta: { title: '밑고름: 상품추천' }   
  },
  ],
})
router.afterEach((to, from) => {
  document.title = to.meta.title || '기본 타이틀';
});



export default router
