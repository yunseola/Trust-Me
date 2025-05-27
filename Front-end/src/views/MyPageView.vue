<template>
  <div class="user-info-container">
    <h4>회원 정보</h4>
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
    
    <div v-else-if="userInfo" class="profile-container">
      <!-- 회원정보 카드 -->
      <div class="member-info-card">
        <div class="card-content">
          <div class="profile-section">
            <div class="profile-details">
              <h3 class="user-name">{{ userInfo.name }} 님</h3>
              <div class="info-row">
                <span class="label">아이디:</span>
                <span class="value">{{ userInfo.username }}</span>
              </div>
              <div class="info-row">
                <span class="label">이메일:</span>
                <span class="value">{{ userInfo.email }}</span>
              </div>
              <div class="info-row">
                <span class="label">전화번호:</span>
                <span class="value">{{ formatPhoneNumber(userInfo.phonenumber) }}</span>
              </div>
              <div class="info-row">
                <span class="label">자산총액:</span>
                <span class="value wealth">{{ formatCurrency(userInfo.wealth) }} 만원</span>
              </div>
            </div>
            <div class="profile-avatar">
              <div class="avatar-circle">
                <i class="user-icon"><img src="@/assets/user_icon.png"  width='80px' height="80px" alt="이미지"></i>
              </div>
            </div>
          </div>
          <div class="action-buttons">
            <RouterLink to="/userdetail" class="btn btn-outline">수정하기</RouterLink>
            <button class="btn btn-outline" @click="confirmDeleteAccount">탈퇴하기</button>
          </div>
        </div>
      </div>

      <!-- 탭 버튼 섹션 -->
      <div class="tab-buttons">
        <button 
          :class="['tab-btn', { active: activeTab === 'deposit' }]" 
          @click="setActiveTab('deposit'), $router.push('/mypage')"
        >
          예금상품
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'security' }]" 
          @click="setActiveTab('security'), $router.push('/InterestYoutubeView')"
          
        >
          관심분야
        </button>
      </div>
    </div>

    <!-- 회원탈퇴 확인 모달 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content" @click.stop>
        <h3>회원탈퇴 확인</h3>
        <p>정말로 탈퇴하시겠습니까?</p>
        <p class="warning-text">탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.</p>
        <div class="modal-buttons">
          <button class="btn btn-secondary" @click="closeDeleteModal">취소</button>
          <button class="btn btn-danger" @click="deleteAccount" :disabled="deleteLoading">
            {{ deleteLoading ? '처리중...' : '탈퇴하기' }}
          </button>
        </div>
      </div>
    </div>
    <RouterView/>
  </div>

</template>




<script>
import axios from 'axios';
import { logout } from '@/stores/auth';

export default {
  name: 'UserInfo',
  data() {
    return {
      userInfo: null,
      loading: false,
      error: null,
      activeTab: 'deposit', // 기본값을 'deposit'으로 설정
      showDeleteModal: false,
      deleteLoading: false
    };
  },
  
  methods: {
    // 탭 변경 메서드
    setActiveTab(tab) {
      this.activeTab = tab;
      
      // 탭에 따른 추가 로직 실행
      if (tab === 'deposit') {
        console.log('예금 상품 탭 선택됨');
        // 예금 상품 관련 로직 실행
      } else if (tab === 'security') {
        console.log('금융 보안 탭 선택됨');
        // 금융 보안 관련 로직 실행
      }
    },

    async fetchUserInfo() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('authToken');
        
        if (!token) {
          throw new Error('토큰이 없습니다. 로그인이 필요합니다.');
        }
        
        const response = await axios.get('http://127.0.0.1:8000/accounts/user_info/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        this.userInfo = response.data;
        
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

    // 회원탈퇴 확인 모달 열기
    confirmDeleteAccount() {
      this.showDeleteModal = true;
    },

    // 회원탈퇴 확인 모달 닫기
    closeDeleteModal() {
      this.showDeleteModal = false;
    },

    // 회원탈퇴 실행
    async deleteAccount() {
      this.deleteLoading = true;
      
      try {
        const token = localStorage.getItem('authToken');
        
        if (!token) {
          throw new Error('토큰이 없습니다. 로그인이 필요합니다.');
        }
        
        const response = await axios.delete('http://127.0.0.1:8000/accounts/delete/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        logout();
        alert('회원탈퇴가 완료되었습니다.');
        this.$router.push('/');
        
      } catch (error) {
        console.error('회원탈퇴 실패:', error);
        
        let errorMessage = '회원탈퇴 중 오류가 발생했습니다.';
        
        if (error.response) {
          if (error.response.status === 401) {
            errorMessage = '인증이 만료되었습니다. 다시 로그인해주세요.';
          } else if (error.response.status === 403) {
            errorMessage = '탈퇴 권한이 없습니다.';
          } else if (error.response.status === 404) {
            errorMessage = '사용자를 찾을 수 없습니다.';
          } else {
            errorMessage = `서버 오류: ${error.response.status}`;
          }
        } else if (error.request) {
          errorMessage = '서버에 연결할 수 없습니다.';
        }
        
        alert(errorMessage);
        
      } finally {
        this.deleteLoading = false;
        this.showDeleteModal = false;
      }
    },
    
    formatPhoneNumber(phone) {
      if (!phone) return '';
      return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
    },
    
    formatCurrency(amount) {
      if (!amount && amount !== 0) return '0';
      return new Intl.NumberFormat('ko-KR').format(amount);
    }
  },
  
  mounted() {
    this.fetchUserInfo();
  }
};
</script>
<style scoped>
.user-info-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
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
  background: white;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

/* 메인 프로필 컨테이너 */
.profile-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 회원정보 카드 */
.member-info-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-content {
  padding: 30px;
  background: #E8E8E4;
}

.profile-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
}

.profile-details {
  flex: 1;
}

.user-name {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin: 0 0 20px 0;
}

.info-row {
  display: flex;
  margin-bottom: 12px;
  align-items: center;
}

.label {
  font-weight: 500;
  color: #666;
  width: 100px;
  font-size: 14px;
}

.value {
  color: #333;
  font-size: 14px;
}

.value.wealth {
  font-weight: 600;
  color: #28a745;
}

.profile-avatar {
  margin-left: 20px;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #007bff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

/* 탭 버튼 스타일 */
.tab-buttons {
  display: flex;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-top: 20px;
}

.tab-btn {
  flex: 1;
  padding: 16px 24px;
  border: none;
  background: #f8f9fa;
  color: #6c757d;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border-right: 1px solid #e9ecef;
  position: relative;
}

.tab-btn:last-child {
  border-right: none;
}

.tab-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.tab-btn.active {
  background: #22356F;
  color: white;
  font-weight: 600;
}

.tab-btn.active:hover {
  background: #0056b3;
}

/* 버튼 스타일 */
.btn {
  padding: 5px 25px;
  border-radius: 40px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline {
  background: #E0E0DE;
  border: 1px solid #585857;
  color: #666;
}

.btn-outline:hover {
  background: #f8f9fa;
}

.btn-danger {
  background: #f50000;
  border: 1px solid #585857;
  color: white;
}

.btn-danger:hover {
  background: #f8f9fa;
}

.btn-secondary {
  background: #6c757d;
  border: 1px solid #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #685a5a;
  border-color: #545b62;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-content h3 {
  margin: 0 0 15px 0;
  color: #333;
}

.modal-content p {
  margin: 10px 0;
  color: #666;
}

.warning-text {
  color: #dc3545;
  font-weight: 500;
  font-size: 14px;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .user-info-container {
    padding: 10px;
  }
  
  .profile-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .profile-avatar {
    margin: 20px 0 0 0;
  }
  
  .action-buttons {
    justify-content: center;
  }

  .modal-content {
    margin: 20px;
    width: calc(100% - 40px);
  }

  .modal-buttons {
    flex-direction: column;
  }

  .tab-buttons {
    flex-direction: column;
  }
  
  .tab-btn {
    border-right: none;
    border-bottom: 1px solid #e9ecef;
  }
  
  .tab-btn:last-child {
    border-bottom: none;
  }
}
</style>

