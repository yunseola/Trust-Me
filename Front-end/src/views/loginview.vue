<template>
  <!-- 기존 템플릿 내용 동일 -->
  <div class="login-container">
    <div class="login-form-wrapper">
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- 기존 폼 내용 동일 -->
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

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="login-btn" 
          :disabled="isLoading"
        >
          {{ isLoading ? '로그인 중...' : '로그인' }}
        </button>

        <div class="find-links">
          <router-link to="/find-id" class="find-link">아이디 찾기</router-link>
          <router-link to="/find-password" class="find-link">비밀번호 찾기</router-link>
        </div>

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
import { login } from '@/stores/auth' // 전역 상태 관리 함수 import

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
    togglePassword() {
      this.showPassword = !this.showPassword
    },

    async handleLogin() {
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
        const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
          username: this.loginForm.userId,
          password: this.loginForm.password,
          remember_me: this.loginForm.keepLogin
        }, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken()
          },
          withCredentials: true
        })

        console.log('API 응답:', response)

        if (response.status === 200) {
          if (response.data && response.data.key) {
            // 전역 상태 업데이트 - 이 부분이 핵심!
            login(response.data.key, response.data.user || { username: this.loginForm.userId })
            
            console.log('로그인 성공 - 전역 상태 업데이트 완료')
            
            // 성공 메시지
            if (this.$toast) {
              this.$toast.success('로그인에 성공했습니다!')
            } else {
              alert('환영합니다!')
            }
            
            // 메인 페이지로 리다이렉트
            this.$router.push('/')
          } else {
            console.warn('API 응답에서 토큰(key) 정보를 찾을 수 없습니다.')
            this.errorMessage = '로그인 처리 중 오류가 발생했습니다.'
          }
        }

      } catch (error) {
        console.error('로그인 오류:', error)
        
        if (error.response) {
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
          this.errorMessage = '네트워크 연결을 확인해주세요.'
        } else {
          this.errorMessage = '로그인 중 오류가 발생했습니다.'
        }
      } finally {
        this.isLoading = false
      }
    },

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

    async socialLogin(provider) {
      try {
        window.location.href = `http://127.0.0.1:8000/accounts/social/${provider}/`
      } catch (error) {
        console.error('소셜 로그인 오류:', error)
        this.errorMessage = '소셜 로그인 중 오류가 발생했습니다.'
      }
    }
  },

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
/* 기존 스타일 동일 */
.login-container {
  font-family: 'Noto Sans KR', sans-serif;
  min-height: calc(50vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center; 
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
