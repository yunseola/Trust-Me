<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- 아이디 입력 -->
        <div class="form-group">
          <label for="userId" class="form-label">아이디</label>
          <input
            type="text"
            id="userId"
            v-model="loginForm.userId"
            class="form-control"
            placeholder="아이디를 입력하세요"
            required
          />
        </div>

        <!-- 비밀번호 입력 -->
        <div class="form-group">
          <label for="password" class="form-label">비밀번호</label>
          <div class="password-input-wrapper">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="loginForm.password"
              class="form-control"
              placeholder="비밀번호를 입력하세요"
              required
            />
            <button
              type="button"
              @click="togglePassword"
              class="password-toggle-btn"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              표시
            </button>
          </div>
        </div>

        <!-- 로그인 상태 유지 체크박스 -->
        <div class="form-check">
          <input
            type="checkbox"
            id="keepLogin"
            v-model="loginForm.keepLogin"
            class="form-check-input"
          />
          <label for="keepLogin" class="form-check-label">
            로그인 상태 유지
          </label>
        </div>

        <!-- 에러 메시지 표시 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- 로그인 버튼 -->
        <button 
          type="submit" 
          class="login-btn" 
          :disabled="isLoading"
        >
          {{ isLoading ? '로그인 중...' : '로그인' }}
        </button>

        <!-- 아이디/비밀번호 찾기 링크 -->
        <div class="find-links">
          <router-link to="/find-id" class="find-link">아이디 찾기</router-link>
          <router-link to="/find-password" class="find-link">비밀번호 찾기</router-link>
        </div>

        <!-- 소셜 로그인 -->
        <div class="social-login">
          <p class="social-login-text">또는</p>
          <div class="social-buttons">
            <button type="button" @click="socialLogin('facebook')" class="social-btn facebook">
              <i class="fab fa-facebook-f"><img src="@/assets/facebook_logo.png" width="30px" height="28px" alt="페이스북로고"></i>
            </button>
            <button type="button" @click="socialLogin('apple')" class="social-btn apple">
              <i class="fab fa-apple"><img src="@/assets/apple_logo.png" width="25px" height="28px" alt="애플로고"></i>
            </button>
            <button type="button" @click="socialLogin('google')" class="social-btn google">
              <i class="fab fa-google"><img src="@/assets/google_logo.webp" width="40px" height="40px" alt="구글로고"></i>
            </button>
            <button type="button" @click="socialLogin('naver')" class="social-btn naver">
              <span class="naver-icon"><img src="@/assets/naver_logo.png"  width="29px" height="29px" alt="네이버로고"></span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginForm',
  data() {
    return {
      loginForm: {
        userId: '',
        password: '',
        keepLogin: false
      },
      showPassword: false,
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    // 비밀번호 표시/숨김 토글
    togglePassword() {
      this.showPassword = !this.showPassword
    },

    // 로그인 처리
    async handleLogin() {
      // 입력값 검증
      if (!this.loginForm.userId.trim()) {
        this.errorMessage = '아이디를 입력해주세요.'
        return
      }
      
      if (!this.loginForm.password.trim()) {
        this.errorMessage = '비밀번호를 입력해주세요.'
        return
      }

      this.isLoading = true
      this.errorMessage = ''

      try {
        // Django 백엔드로 로그인 요청
        const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
          username: this.loginForm.userId,  // Django는 보통 username 필드 사용
          password: this.loginForm.password,
          remember_me: this.loginForm.keepLogin
        }, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken() // CSRF 토큰 추가
          },
          withCredentials: true // 쿠키 포함
        })
        console.log('API 응답:', response);
        // 로그인 성공 처리
        // 로그인 성공 처리
if (response.status === 200) {
  // API 응답에서 'key' 값을 토큰으로 사용
  if (response.data && response.data.key) { // response.data가 존재하고, 그 안에 key가 있는지 확인
    localStorage.setItem('authToken', response.data.key); // 'authToken'이라는 키로 response.data.key 값을 저장
    console.log('authToken 저장 완료:', localStorage.getItem('authToken'));
  } else {
    console.warn('API 응답에서 토큰(key) 정보를 찾을 수 없습니다.');
    // 필요하다면 여기서 사용자에게 토큰 정보가 없음을 알리는 로직 추가
  }
  
  // 현재 API 응답에는 사용자 정보(user)가 없어 보입니다.
  // 만약 API가 사용자 정보도 반환한다면, 해당 키로 접근하여 저장해야 합니다.
  // 예를 들어, response.data.userData 와 같은 형태라면 아래와 같이 수정합니다.
  // if (response.data.userData) {
  //   localStorage.setItem('user', JSON.stringify(response.data.userData));
  // }

  // 성공 메시지 표시 (선택사항)
  this.$toast?.success('로그인에 성공했습니다!');
  
  // 메인 페이지로 리다이렉트
  this.$router.push('/');
}

      } catch (error) {
        console.error('로그인 오류:', error)
        
        // 에러 처리
        if (error.response) {
          // 서버에서 응답한 에러
          switch (error.response.status) {
            case 400:
              this.errorMessage = '아이디 또는 비밀번호가 올바르지 않습니다.'
              break
            case 401:
              this.errorMessage = '인증에 실패했습니다. 다시 시도해주세요.'
              break
            case 429:
              this.errorMessage = '너무 많은 로그인 시도입니다. 잠시 후 다시 시도해주세요.'
              break
            case 500:
              this.errorMessage = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
              break
            default:
              this.errorMessage = error.response.data?.message || '로그인 중 오류가 발생했습니다.'
          }
        } else if (error.request) {
          // 네트워크 오류
          this.errorMessage = '네트워크 연결을 확인해주세요.'
        } else {
          // 기타 오류
          this.errorMessage = '로그인 중 오류가 발생했습니다.'
        }
      } finally {
        this.isLoading = false
      }
    },

    // CSRF 토큰 가져오기
    getCSRFToken() {
      const cookies = document.cookie.split(';')
      for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=')
        if (name === 'csrftoken') {
          return value
        }
      }
      return ''
    },

    // 소셜 로그인 처리
    async socialLogin(provider) {
      try {
        // 소셜 로그인 URL로 리다이렉트
        window.location.href = `http://127.0.0.1:8000/accounts/social/${provider}/`
      } catch (error) {
        console.error('소셜 로그인 오류:', error)
        this.errorMessage = '소셜 로그인 중 오류가 발생했습니다.'
      }
    }
  },

  // 컴포넌트 마운트 시 실행
  mounted() {
    // 이미 로그인된 사용자라면 메인 페이지로 리다이렉트
    const token = localStorage.getItem('authToken')
    if (token) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.login-container {
  font-family: 'Noto Sans KR', sans-serif;
  min-height: calc(50vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.login-form-wrapper {
  background: white;
  border-radius: 8px;
  padding: 3rem 2.5rem;
  width: 100%;
  max-width: 550px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.password-input-wrapper {
  position: relative;
}

.password-toggle-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.password-toggle-btn:hover {
  color: #666;
}

.form-check {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.form-check-input {
  width: 16px;
  height: 16px;
}

.form-check-label {
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  text-align: center;
  border: 1px solid #fcc;
}

.login-btn {
  width: 100%;
  padding: 0.875rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 1.5rem;
}

.login-btn:hover:not(:disabled) {
  background-color: #357abd;
}

.login-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.find-links {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.find-link {
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
}

.find-link:hover {
  color: #4a90e2;
  text-decoration: underline;
}

.social-login {
  text-align: center;
}

.social-login-text {
  color: #999;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.social-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.social-btn {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: transform 0.2s ease;
}

.social-btn:hover {
  transform: translateY(-2px);
}

.social-btn.facebook {
  background-color: #1877f2;
  color: white;
}

.social-btn.apple {
  background-color: #000;
  color: white;
}

.social-btn.google {
  background-color: #FFFFFF;
  color: white;
}

.social-btn.naver {
  background-color: #03CD66;
}

@media (max-width: 480px) {
  .login-form-wrapper {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }
  
  .social-buttons {
    gap: 0.75rem;
  }
  
  .social-btn {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>
