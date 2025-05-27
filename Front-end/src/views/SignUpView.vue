<template>
  <div class="signup-container">
    <div class="signup-form">
      <form @submit.prevent="handleSubmit">
        <!-- Username -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <input 
            v-model="form.username"
            type="text" 
            placeholder="아이디"
            required
          />
        </div>

        <!-- Password1 -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M18,8h-1V6c0-2.76-2.24-5-5-5S7,3.24,7,6v2H6c-1.1,0-2,0.9-2,2v10c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V10C20,8.9,19.1,8,18,8z"/>
            </svg>
          </div>
          <input 
            v-model="form.password1"
            type="password" 
            placeholder="비밀번호"
            required
          />
        </div>

        <!-- Password2 -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M18,8h-1V6c0-2.76-2.24-5-5-5S7,3.24,7,6v2H6c-1.1,0-2,0.9-2,2v10c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2V10C20,8.9,19.1,8,18,8z"/>
            </svg>
          </div>
          <input 
            v-model="form.password2"
            type="password" 
            placeholder="비밀번호 확인"
            :class="{ 'error': passwordMismatch }"
            required
          />
        </div>
        <!-- Name -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <input 
            v-model="form.name"
            type="text" 
            placeholder="이름"
            required
          />
        </div>
        <!-- Nickname -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <input 
            v-model="form.nickname"
            type="text" 
            placeholder="닉네임"
            required
          />
        </div>
                <!-- Age -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
            </svg>
          </div>
          <input 
            v-model.number="form.age"
            type="number" 
            placeholder="나이"
            required
          />
        </div>
        <!-- Gender -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M11.5 1a.5.5 0 0 1 0-1h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V1.707l-3.45 3.45A4 4 0 0 1 8.5 10.97V13H10a.5.5 0 0 1 0 1H8.5v1.5a.5.5 0 0 1-1 0V14H6a.5.5 0 0 1 0-1h1.5v-2.03a4 4 0 1 1 3.471-6.648L14.293 1zm-.997 4.346a3 3 0 1 0-5.006 3.309 3 3 0 0 0 5.006-3.31z"/>
            </svg>
          </div>
          <select v-model="form.gender" required>
            <option value="" disabled>성별</option>
            <option value="0">남자</option>
            <option value="1">여자</option>
          </select>
        </div>
        <!-- Email -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
            </svg>
          </div>
          <input 
            v-model="form.email"
            type="email" 
            placeholder="이메일"
            required
          />
        </div>
        <!-- Phone Number -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
            </svg>
          </div>
          <input 
            v-model="form.phonenumber"
            type="tel" 
            placeholder="전화번호"
            required
          />
        </div>

        <!-- Salary -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
            </svg>
          </div>
          <input 
            v-model.number="form.salary"
            type="number" 
            placeholder="월소득(만원)"
          />
        </div>

        <!-- Wealth -->
        <div class="input-group">
          <div class="icon">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
            </svg>
          </div>
          <input 
            v-model.number="form.wealth"
            type="number" 
            placeholder="자산(만원)"
          />
        </div>

        <!-- 가입하기 버튼 -->
        <button type="submit" class="signup-btn" :disabled="isLoading">
          {{ isLoading ? '처리중...' : '가입하기' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignupForm',
  data() {
    return {
      isLoading: false,
      form: {
        username: '',
        email: '',
        password1: '',
        password2: '',
        nickname: '',
        name: '',
        phonenumber: '',
        age: null,
        gender: '',
        salary: null,
        wealth: null
      }
    }
  },
  computed: {
    passwordMismatch() {
      return this.form.password1 && this.form.password2 && 
             this.form.password1 !== this.form.password2;
    }
  },
  methods: {
    async handleSubmit() {
      // 비밀번호 확인
      if (this.passwordMismatch) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
      }

      // 필수 필드 검증
      if (!this.form.username || !this.form.email || !this.form.password1 || !this.form.password2) {
        alert('필수 필드를 모두 입력해주세요.');
        return;
      }

      this.isLoading = true;
      
      try {
        // JSON 형태로 데이터 전송 (DRF 표준)
        const response = await fetch('http://127.0.0.1:8000/accounts/signup/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: JSON.stringify({
            username: this.form.username,
            email: this.form.email,
            password1: this.form.password1,
            password2: this.form.password2,
            nickname: this.form.nickname,
            name: this.form.name,
            phonenumber: this.form.phonenumber,
            age: this.form.age,
            gender: parseInt(this.form.gender),
            salary: this.form.salary,
            wealth: this.form.wealth
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert('회원가입이 완료되었습니다!, 로그인해주세요.');
          
          // 토큰이 반환되는 경우 저장
          if (data.token || data.key) {
            localStorage.setItem('authToken', data.token || data.key);
          }
          
          // 로그인 페이지로 이동
          this.$router.push('/login');
        } else {
          // 에러 메시지 처리
          let errorMessage = '회원가입에 실패했습니다.';
          if (data.username) {
            errorMessage = `아이디: ${data.username[0]}`;
          } else if (data.email) {
            errorMessage = `이메일: ${data.email[0]}`;
          } else if (data.password1) {
            errorMessage = `비밀번호: ${data.password1[0]}`;
          } else if (data.non_field_errors) {
            errorMessage = data.non_field_errors[0];
          }
          alert(errorMessage);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('네트워크 오류가 발생했습니다. 다시 시도해주세요.');
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>


<style scoped>
/* 전체 컨테이너 - 로그인 폼과 일관성 유지 */
.signup-container {
  font-family: 'Noto Sans KR', sans-serif;
  min-height: calc(50vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;

  padding: 40px 20px;
  overflow-x: hidden;
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
}

.signup-form {
  background: white;
  border-radius: 8px; /* 로그인 폼과 동일 */
  padding: 3rem 2.5rem; /* 로그인 폼과 동일 */
  width: 100%;
  max-width: 550px; /* 로그인 폼과 동일한 너비 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  margin: 0 auto;
}

.form-title {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
  font-size: 1.8rem;
  font-weight: 700;
}

.input-group {
  position: relative;
  margin-bottom: 1.5rem; /* 로그인 폼과 동일 */
}

.icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon svg {
  fill: currentColor;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 50px; /* 로그인 폼과 동일 */
  border: 1px solid #ddd; /* 로그인 폼과 동일 */
  border-radius: 4px; /* 로그인 폼과 동일 */
  font-size: 1rem; /* 로그인 폼과 동일 */
  background-color: #fafafa;
  transition: all 0.3s ease;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}

.input-group input:focus,
.input-group select:focus {
  outline: none;
  border-color: #4a90e2; /* 로그인 폼과 동일 */
  background-color: white;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2); /* 로그인 폼과 동일 */
}

.input-group input.error {
  border-color: #dc3545;
}

.input-group input::placeholder {
  color: #999;
}

/* select 요소 특별 스타일링 */
.input-group select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6,9 12,15 18,9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  cursor: pointer;
}

.signup-btn {
  width: 100%;
  padding: 0.875rem; /* 로그인 폼과 동일 */
  background-color: #4a90e2; /* 로그인 폼과 동일 */
  color: white;
  border: none;
  border-radius: 25px; /* 로그인 폼과 동일 */
  font-size: 1rem; /* 로그인 폼과 동일 */
  font-weight: 500; /* 로그인 폼과 동일 */
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 1.5rem; /* 로그인 폼과 동일 */
}

.signup-btn:hover:not(:disabled) {
  background-color: #357abd; /* 로그인 폼과 동일 */
}

.signup-btn:disabled {
  background-color: #ccc; /* 로그인 폼과 동일 */
  cursor: not-allowed;
}

/* 전역 스크롤바 문제 해결 - 핵심 부분 */
:global(html) {
  overflow-y: scroll !important; /* 항상 세로 스크롤바 표시 */
  scrollbar-gutter: stable; /* 스크롤바 공간 예약 */
}

:global(body) {
  overflow-x: hidden !important; /* 가로 스크롤 방지 */
  width: 100% !important;
  max-width: 100vw !important;
  box-sizing: border-box !important;
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .signup-container {
    padding: 20px 10px;
  }
  
  .signup-form {
    padding: 2rem 1.5rem; /* 로그인 폼과 동일 */
    margin: 0 10px;
    max-width: calc(100vw - 20px);
  }
  
  .form-title {
    font-size: 1.5rem;
  }
  
  .input-group input,
  .input-group select {
    font-size: 16px; /* iOS 줌 방지 */
    padding: 12px 12px 12px 45px;
  }
}
</style>