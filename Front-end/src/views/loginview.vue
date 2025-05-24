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

        <!-- 로그인 버튼 -->
        <button type="submit" class="login-btn">로그인</button>

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
              <i class="fab fa-facebook-f"></i>
            </button>
            <button type="button" @click="socialLogin('apple')" class="social-btn apple">
              <i class="fab fa-apple"></i>
            </button>
            <button type="button" @click="socialLogin('google')" class="social-btn google">
              <i class="fab fa-google"></i>
            </button>
            <button type="button" @click="socialLogin('naver')" class="social-btn naver">
              <span class="naver-icon">N</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const showPassword = ref(false)
    
    const loginForm = reactive({
      userId: '',
      password: '',
      keepLogin: false
    })

    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    const handleLogin = async () => {
      try {
        // 로그인 API 호출 로직
        console.log('로그인 시도:', loginForm)
        
        // 성공 시 메인 페이지로 이동
        // router.push('/')
        
        // 실제 구현 시에는 API 호출 후 응답에 따라 처리
        alert('로그인 기능을 구현해주세요')
      } catch (error) {
        console.error('로그인 에러:', error)
        alert('로그인에 실패했습니다.')
      }
    }

    const socialLogin = (provider) => {
      console.log(`${provider} 소셜 로그인`)
      // 각 소셜 로그인 구현
      alert(`${provider} 로그인 기능을 구현해주세요`)
    }

    return {
      loginForm,
      showPassword,
      togglePassword,
      handleLogin,
      socialLogin
    }
  }
}
</script>

<style scoped>
.login-container {
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
  max-width: 400px;
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

.login-btn {
  width: 100%;
  padding: 0.875rem;
  background-color: #999;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 1.5rem;
}

.login-btn:hover {
  background-color: #777;
}

.login-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.find-links {
  display: flex;
  justify-content: center;
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
  background-color: #db4437;
  color: white;
}

.social-btn.naver {
  background-color: #03c75a;
  color: white;
}

.naver-icon {
  font-weight: bold;
  font-size: 1.1rem;
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
