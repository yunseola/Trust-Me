<template>
  <div id="app-container">
    <header class="app-header">
      <div class="header-content">
        <!-- 로고 영역 -->
        <div class="icon-placeholder">
          <RouterLink to="/"><img src="@/assets/logo_icon.png" width="100px" height="50px" alt="로고아이콘"></RouterLink>
        </div>
        
        <!-- 네비게이션 메뉴 -->
        <nav class="navigation-menu">
          <ul>
            <li><RouterLink to="/introduce">금융상품 소개</RouterLink></li>
            <li><RouterLink to="/recommendation">맞춤형 상품 추천</RouterLink></li>
            <li><RouterLink to="/introducecompare">금융상품 비교</RouterLink></li>
            <li><RouterLink to="/exchange">환율</RouterLink></li>
            <li><RouterLink to="/metal-price">금은시세</RouterLink></li>
          </ul>
        </nav>
        
        <!-- 우측 영역: 상단 링크와 하단 아이콘 -->
        <div class="right-section">
          <!-- 상단 링크들 -->
          <div class="top-bar">
            <div class="auth-links">
              <RouterLink to="/trustme">믿고름소개</RouterLink>
                <span class="separator">|</span>
              <!-- 로그인 상태일 때 -->
              <template v-if="authStore.isLoggedIn">
                <RouterLink to="/mypage">마이페이지</RouterLink>
                <span class="separator">|</span>
                <a href="#" @click.prevent="handleLogout">로그아웃</a>
              </template>
              <!-- 로그아웃 상태일 때 -->
              <template v-else>
                <RouterLink to="/signup">회원가입</RouterLink>
                <span class="separator">|</span>
                <RouterLink to="/login">로그인</RouterLink>
              </template>
            </div>
          </div>
          
          <!-- 하단 아이콘들 -->
          <div class="user-menu">
            <div class="icon-placeholder">
              <img src="@/assets/search_icon.png" width="24px" height="24px" alt="검색아이콘">
            </div>
            <div class="icon-placeholder">
              <img src="@/assets/chatbot_icon.png" width="24px" height="24px" alt="챗봇아이콘">
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <RouterView />
    </main>

    <footer class="app-footer">
      <!-- 푸터 내용은 기존과 동일하게 유지 -->
      <div class="footer-content">
        <div class="footer-icons">
          <div class="footer-icon-placeholder">
            <a href="https://mail.naver.com" target="_blank" rel="noopener noreferrer">
              <img src="@/assets/email_icon.png" width="28px" height="30px" alt="이메일아이콘">
            </a>
          </div>
          <div class="footer-icon-placeholder">
            <a href="https://www.instagram.com/fsskorea/" target="_blank" rel="noopener noreferrer">
              <img src="@/assets/instagram_icon.png" width="29px" height="29px" alt="인스타아이콘">
            </a>
          </div>
          <div class="footer-icon-placeholder">
            <a href="https://www.tiktok.com/tag/%EA%B8%88%EC%9C%B5%EA%B0%90%EB%8F%85%EC%9B%90" target="_blank" rel="noopener noreferrer">
              <img src="@/assets/tiktok_icon.png" width="28px" height="28px" alt="틱톡아이콘">
            </a>
          </div>
          <div class="footer-icon-placeholder">
            <a href="https://www.youtube.com/fsskorea" target="_blank" rel="noopener noreferrer">
              <img src="@/assets/youtube_icon.png" width="29px" height="31px" alt="유튜브아이콘">
            </a>
          </div>
        </div>
        <div class="footer-info">
          <p>(주) 믿고름 사업자 번호: 992-13-01731&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;대표전화: 1599-8244&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;주소: 부산광역시 연제구 신호동 101-2</p>
          <p>
            <RouterLink to="/trustme">회사소개</RouterLink> | 
            <a href="https://www.jobkorea.co.kr/">인재채용</a> |
            <a href="https://www.navercorp.com/nhn/company/proposalGuide.nhn">제휴제안</a> |
            <a href="https://policy.naver.com/policy/service.html">이용약관</a> |
            <a href="https://policy.naver.com/policy/privacy.html">개인정보처리방침</a> |
            <a href="https://policy.naver.com/policy/youthpolicy.html">청소년보호정책</a> |
            <a href="https://policy.naver.com/policy/search_policy.html">믿고름 정책</a> |
            <a href="https://help.naver.com/index.help?lang=ko">고객센터</a> | ⓒ Trust Me™ Corp.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { authStore, logout, checkAuthStatus } from '@/stores/auth'

const router = useRouter()

// 로그아웃 처리 함수
const handleLogout = () => {
  logout() // 전역 상태 업데이트
  alert('로그아웃 되었습니다.')
  router.push('/')
}

// 컴포넌트 마운트 시 인증 상태 확인
onMounted(() => {
  checkAuthStatus()
})
</script>

<style scoped>
/* 기존 스타일 유지 + 추가 스타일 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

body {
  font-family: 'Noto Sans KR', sans-serif;
  margin: 0;
  background-color: #f4f7fa;
  color: #333;
}

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  box-sizing: border-box;
}

a {
  text-decoration: none;
  color: inherit;
}

/* ======== HEADER 스타일 ======== */
.app-header {
  width: 100%;
  background-color: #22356F;
  color: #FFFFFF;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  height: 100px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

/* ======== 네비게이션 메뉴 스타일 ======== */
.navigation-menu ul {
  display: flex;
  gap: 40px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navigation-menu ul li {
  font-size: 16px;
  font-weight: 500;
  color: #FFFFFF;
  opacity: 0.9;
  transition: opacity 0.2s ease;
  cursor: pointer;
}



.navigation-menu a.router-link-exact-active {
  font-weight: 700;
  opacity: 1;
}

/* ======== 우측 섹션 스타일 ======== */
.right-section {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.top-bar {
  display: flex;
  justify-content: flex-end;
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.auth-links a {
  font-size: 12px;
  font-weight: 400;
  color: #FFFFFF;
  opacity: 0.8;
  padding: 4px 6px;
  border-radius: 3px;
  transition: opacity 0.2s ease, background-color 0.2s ease;
}

.separator {
  color: #FFFFFF;
  opacity: 0.6;
  font-size: 11px;
  margin: 0 2px;
}

/* 사용자 이름 스타일 추가 */
.user-name {
  font-size: 12px;
  color: #FFFFFF;
  opacity: 0.9;
  font-weight: 500;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 15px;
}

.icon-placeholder {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

/* ======== FOOTER 스타일 (기존과 동일) ======== */
.app-footer {
  width: 100%;
  background-color: #22356F;
  color: #FFFFFF;
  padding: 30px 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  padding: 0 20px;
}

.footer-icons {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.footer-icon-placeholder {
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.footer-icon-placeholder img {
  filter: brightness(0) invert(1);
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.footer-icon-placeholder:hover img {
  opacity: 1;
}

.footer-info p {
  font-size: 15px;
  line-height: 1.6;
  opacity: 0.7;
  margin: 5px 0;
}

.footer-info p:nth-of-type(2) {
  font-size: 10px;
}

.footer-info a {
  color: #FFFFFF;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.footer-info a:hover {
  opacity: 1;
  text-decoration: underline;
}

/* ======== 반응형 스타일 ======== */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 20px;
    gap: 15px;
  }
  
  .navigation-menu ul {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .right-section {
    align-items: center;
    gap: 10px;
  }
  
  .auth-links a {
    font-size: 11px;
    padding: 3px 5px;
  }
  
  .user-menu {
    gap: 12px;
  }

  .footer-info p {
    font-size: 12px;
  }
  .footer-info p:nth-of-type(2) {
    font-size: 9px;
  }
}

@media (max-width: 480px) {
  .navigation-menu ul li {
    font-size: 14px;
  }

  .auth-links {
    gap: 6px;
  }
  
  .auth-links a {
    font-size: 10px;
    padding: 2px 4px;
  }
  
  .separator {
    font-size: 10px;
  }
  
  .user-menu {
    gap: 10px;
  }

  .footer-icons {
    gap: 20px;
  }
  .footer-icon-placeholder img {
    width: 24px;
    height: auto;
  }
}
</style>
