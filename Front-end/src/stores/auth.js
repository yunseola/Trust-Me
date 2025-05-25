// src/stores/auth.js
import { reactive, watchEffect } from 'vue'

// localStorage에서 초기 상태 읽어오기
const getInitialState = () => {
  const token = localStorage.getItem('authToken')
  const user = localStorage.getItem('user')
  
  return {
    isLoggedIn: !!token,
    user: user ? JSON.parse(user) : null,
    token: token || null
  }
}

// 반응형 상태 생성
export const authStore = reactive(getInitialState())

// 상태 변경 시 localStorage에 자동 저장
watchEffect(() => {
  if (authStore.token) {
    localStorage.setItem('authToken', authStore.token)
  } else {
    localStorage.removeItem('authToken')
  }
  
  if (authStore.user) {
    localStorage.setItem('user', JSON.stringify(authStore.user))
  } else {
    localStorage.removeItem('user')
  }
})

// 로그인 액션
export const login = (token, userData = null) => {
  authStore.token = token
  authStore.user = userData
  authStore.isLoggedIn = true
}

// 로그아웃 액션
export const logout = () => {
  authStore.token = null
  authStore.user = null
  authStore.isLoggedIn = false
}

// 로그인 상태 확인
export const checkAuthStatus = () => {
  const token = localStorage.getItem('authToken')
  if (token) {
    authStore.token = token
    authStore.isLoggedIn = true
    // 필요시 사용자 정보도 복원
    const user = localStorage.getItem('user')
    if (user) {
      authStore.user = JSON.parse(user)
    }
  }
}
