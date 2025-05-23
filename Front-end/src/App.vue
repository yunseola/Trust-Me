<template>
  <div id="app-container">
    <header class="app-header">
      <div class="header-content">
        <router-link to="/" class="logo-placeholder"></router-link>

        <nav class="navigation-menu">
          <ul>
            <li><router-link to="/products">금융상품 소개</router-link></li>
            <li><router-link to="/recommend">맞춤형 상품 추천</router-link></li>
            <li><router-link to="/compare">금융상품 비교</router-link></li>
            <li><router-link to="/exchange">환율</router-link></li>
            <li><router-link to="/market">금융 시세</router-link></li>
          </ul>
        </nav>

        <div class="user-menu">
          <div class="icon-placeholder"></div>
          <div class="icon-placeholder"></div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-icons">
          <div class="footer-icon-placeholder"></div>
          <div class="footer-icon-placeholder"></div>
          <div class="footer-icon-placeholder"></div>
          <div class="footer-icon-placeholder"></div>
        </div>
        
        <div class="footer-info">
          <p>(주) 믿고름 사업자 번호: 992-13-01731   대표전화: 1599-8244   주소: 부산광역시 연제구 신호동 101-2</p>
          <p>회사소개 | 인재채용 | 제휴제안 | 이용약관 | 개인정보처리방침 | 청소년보호정책 | 믿고름 정책 | 고객센터  | ⓒ Trust Me™ Corp.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// 스크립트 로직은 비워둡니다.
</script>

<style>
/* ======== 전역 및 레이아웃 스타일 ======== */
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

/* ======== HEADER 스타일 (색상 변경) ======== */
.app-header {
  width: 100%;
  background-color: #22356F; /* 배경색 변경 */
  color: #FFFFFF; /* header 안의 모든 글자 색상 흰색으로 지정 */
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

.logo-placeholder {
  width: 100px;
  height: 35px;
  background-color: #FFFFFF; /* 로고 배경을 흰색으로 하여 잘 보이게 함 */
  opacity: 0.8; /* 약간의 투명도 조절 */
  border-radius: 4px;
}

.navigation-menu a {
  font-size: 16px;
  font-weight: 500;
  color: #FFFFFF; /* 네비게이션 텍스트 색상 변경 */
  opacity: 0.9; /* 기본 텍스트 약간 투명하게 */
}

.navigation-menu a:hover {
  opacity: 1;
}

.navigation-menu a.router-link-exact-active {
  font-weight: 700;
  opacity: 1; /* 활성화된 메뉴는 완전한 흰색 */
}

.navigation-menu ul {
  display: flex;
  gap: 40px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-placeholder {
  width: 24px;
  height: 24px;
  background-color: #FFFFFF; /* 아이콘 배경도 흰색으로 */
  opacity: 0.8;
  border-radius: 50%;
}

/* ======== FOOTER 스타일 (색상 변경) ======== */
.app-footer {
  width: 100%;
  background-color: #22356F; /* 배경색 변경 */
  color: #FFFFFF; /* 내부 모든 텍스트의 기본 색상을 흰색으로 설정 */
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
  width: 28px;
  height: 28px;
  background-color: #FFFFFF;
  opacity: 0.8;
}

.footer-info p {
  font-size: 13px;
  /* color 속성은 상위 .app-footer에서 상속받음 */
  opacity: 0.7; /* 정보 텍스트는 약간 더 투명하게 */
  margin: 0;
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
}
</style>
