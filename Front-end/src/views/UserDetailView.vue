<template>
  <div class="edit-profile-container">
    <div class="edit-profile-card">
      <h2>회원정보 수정</h2>
      
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>사용자 정보를 불러오는 중...</p>
      </div>
      
      <div v-else-if="error" class="error">
        <div class="error-icon">⚠️</div>
        <h3>오류 발생</h3>
        <p>{{ error }}</p>
        <button @click="fetchUserInfo" class="retry-btn">다시 시도</button>
      </div>
      
      <form v-else-if="userInfo" @submit.prevent="updateUserInfo" class="edit-form">
        <div class="form-group">
          <label for="username">아이디 (아이디는 변경이 불가능합니다)</label>
          <input 
            type="text" 
            id="username" 
            :value="userInfo.username" 
            disabled 
            class="form-input disabled"
          >
        </div>

        <div class="form-group">
          <label for="nickname">닉네임 *</label>
          <input 
            type="text" 
            id="nickname" 
            v-model="editForm.nickname" 
            required 
            class="form-input"
            placeholder="닉네임을 입력하세요"
          >
        </div>

        <div class="form-group">
          <label for="name">이름 *</label>
          <input 
            type="text" 
            id="name" 
            v-model="editForm.name" 
            required 
            class="form-input"
            placeholder="이름을 입력하세요"
          >
        </div>

        <div class="form-group">
          <label for="phonenumber">전화번호 *</label>
          <input 
            type="tel" 
            id="phonenumber" 
            v-model="editForm.phonenumber" 
            required 
            class="form-input"
            placeholder="01012345678"
            pattern="[0-9]{11}"
            maxlength="11"
          >
        </div>

        <div class="form-group">
          <label for="age">나이 *</label>
          <input 
            type="number" 
            id="age" 
            v-model.number="editForm.age" 
            required 
            class="form-input"
            min="1" 
            max="120"
            placeholder="나이를 입력하세요"
          >
        </div>

        <div class="form-group">
          <label for="email">이메일 *</label>
          <input 
            type="email" 
            id="email" 
            v-model="editForm.email" 
            required 
            class="form-input"
            placeholder="example@email.com"
          >
        </div>

        <div class="form-group">
          <label for="gender">성별 *</label>
          <select 
            id="gender" 
            v-model.number="editForm.gender" 
            required 
            class="form-input"
          >
            <option value="">성별을 선택하세요</option>
            <option value="0">여성</option>
            <option value="1">남성</option>
          </select>
        </div>

        <div class="form-group">
          <label for="salary">연봉 (만원) *</label>
          <input 
            type="number" 
            id="salary" 
            v-model.number="editForm.salary" 
            required 
            class="form-input"
            min="0"
            placeholder="연봉을 입력하세요 (만원 단위)"
          >
        </div>

        <div class="form-group">
          <label for="wealth">자산 (만원) *</label>
          <input 
            type="number" 
            id="wealth" 
            v-model.number="editForm.wealth" 
            required 
            class="form-input"
            min="0"
            placeholder="자산을 입력하세요 (만원 단위)"
          >
        </div>

        <div class="form-actions">
          <button type="button" @click="goBack" class="btn btn-secondary">취소</button>
          <button type="submit" :disabled="updateLoading" class="btn btn-primary">
            {{ updateLoading ? '수정 중...' : '수정 완료' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditProfile',
  data() {
    return {
      userInfo: null,
      editForm: {
        nickname: '',
        name: '',
        phonenumber: '',
        age: null,
        email: '',
        gender: null,
        salary: null,
        wealth: null
      },
      loading: false,
      updateLoading: false,
      error: null
    };
  },
  
  methods: {
    async fetchUserInfo() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('authToken');
        
        if (!token) {
          throw new Error('토큰이 없습니다. 로그인이 필요합니다.');
        }
        
        const response = await axios.get('http://127.0.0.1:8000/accounts/user/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        this.userInfo = response.data;
        
        // 폼에 기존 데이터 채우기
        this.editForm = {
          nickname: this.userInfo.nickname || '',
          name: this.userInfo.name || '',
          phonenumber: this.userInfo.phonenumber || '',
          age: this.userInfo.age || null,
          email: this.userInfo.email || '',
          gender: this.userInfo.gender !== null ? this.userInfo.gender : null,
          salary: this.userInfo.salary || null,
          wealth: this.userInfo.wealth || null
        };
        
      } catch (error) {
        console.error('사용자 정보 조회 실패:', error);
        
        if (error.response) {
          if (error.response.status === 401) {
            this.error = '인증이 만료되었습니다. 다시 로그인해주세요.';
          } else if (error.response.status === 403) {
            this.error = '접근 권한이 없습니다.';
          } else {
            this.error = `서버 오류: ${error.response.status}`;
          }
        } else if (error.request) {
          this.error = '서버에 연결할 수 없습니다.';
        } else {
          this.error = error.message;
        }
      } finally {
        this.loading = false;
      }
    },

    async updateUserInfo() {
      this.updateLoading = true;
      
      try {
        const token = localStorage.getItem('authToken');
        
        if (!token) {
          throw new Error('토큰이 없습니다. 로그인이 필요합니다.');
        }

        // 전화번호 유효성 검사
        if (!/^[0-9]{11}$/.test(this.editForm.phonenumber)) {
          throw new Error('전화번호는 11자리 숫자로 입력해주세요.');
        }

        // 이메일 유효성 검사
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(this.editForm.email)) {
          throw new Error('올바른 이메일 형식을 입력해주세요.');
        }
        
        const response = await axios.put('http://127.0.0.1:8000/accounts/user/', this.editForm, {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        alert('회원정보가 성공적으로 수정되었습니다.');
        
        // 마이페이지로 이동
        this.$router.push('/mypage');
        
      } catch (error) {
        console.error('회원정보 수정 실패:', error);
        
        let errorMessage = '회원정보 수정 중 오류가 발생했습니다.';
        
        if (error.response) {
          if (error.response.status === 401) {
            errorMessage = '인증이 만료되었습니다. 다시 로그인해주세요.';
          } else if (error.response.status === 403) {
            errorMessage = '수정 권한이 없습니다.';
          } else if (error.response.status === 400) {
            // 서버에서 보내는 구체적인 에러 메시지가 있다면 사용
            if (error.response.data && error.response.data.detail) {
              errorMessage = error.response.data.detail;
            } else {
              errorMessage = '입력한 정보를 다시 확인해주세요.';
            }
          } else {
            errorMessage = `서버 오류: ${error.response.status}`;
          }
        } else if (error.request) {
          errorMessage = '서버에 연결할 수 없습니다.';
        } else {
          errorMessage = error.message;
        }
        
        alert(errorMessage);
        
      } finally {
        this.updateLoading = false;
      }
    },

    goBack() {
      this.$router.go(-1);
    }
  },
  
  mounted() {
    this.fetchUserInfo();
  }
};
</script>

<style scoped>
.edit-profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
}

.edit-profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.edit-profile-card h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 700;
}

/* 로딩 및 에러 스타일 */
.loading {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 40px;
  color: #dc3545;
}

.retry-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 16px;
}

/* 폼 스타일 */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  font-size: 14px;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-input.disabled {
  background: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.form-input::placeholder {
  color: #adb5bd;
}

/* 버튼 스타일 */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.btn {
  flex: 1;
  padding: 14px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .edit-profile-container {
    padding: 10px;
  }
  
  .edit-profile-card {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    flex: none;
  }
}

/* 유효성 검사 스타일 */
.form-input:invalid {
  border-color: #dc3545;
}

.form-input:valid {
  border-color: #28a745;
}

/* 선택 박스 스타일 */
select.form-input {
  cursor: pointer;
}

select.form-input option {
  padding: 10px;
}
</style>
