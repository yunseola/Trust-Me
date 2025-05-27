<template>
  <div class="bank-finder">
    <!-- 헤더 섹션 -->
    <div class="header-section">
      <div class="header-content">
        <h1 class="page-title">🏦 내 주변 은행 찾기</h1>
        <p class="page-description">현재 위치를 기반으로 가까운 은행을 찾아보세요</p>
        <button @click="getCurrentLocation" :disabled="loading" class="location-btn">
          <span v-if="loading" class="loading-text">
            <div class="spinner"></div>
            위치 확인 중...
          </span>
          <span v-else>📍 현재 위치에서 은행 찾기</span>
        </button>
      </div>
    </div>
    
    <!-- 상태 메시지 -->
    <div v-if="statusMessage" class="status-card">
      <div class="status-content">
        <div class="status-icon">ℹ️</div>
        <span>{{ statusMessage }}</span>
      </div>
    </div>
    
    <!-- 지도 컨테이너 -->
    <div class="map-section">
      <div class="map-container">
        <div id="map" ref="map"></div>
      </div>
    </div>
    
    <!-- 은행 목록 -->
    <div v-if="banks.length > 0" class="results-section">
      <div class="results-header">
        <h3 class="results-title">주변 은행 목록</h3>
        <span class="results-count">{{ banks.length }}개의 은행이 검색되었습니다</span>
      </div>
      
      <div class="bank-grid">
        <div 
          v-for="(bank, index) in banks" 
          :key="index" 
          class="bank-card"
          @click="moveToBank(bank)"
        >
          <div class="bank-header">
            <div class="bank-icon">🏦</div>
            <div class="bank-distance">{{ bank.distance }}m</div>
          </div>
          
          <div class="bank-content">
            <h4 class="bank-name">{{ bank.place_name }}</h4>
            <p class="bank-address">{{ bank.address_name }}</p>
            <p v-if="bank.phone" class="bank-phone">
              <span class="phone-icon">📞</span>
              {{ bank.phone }}
            </p>
          </div>
          
          <div class="bank-actions">
            <button class="map-view-btn">
              지도에서 보기
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 에러 메시지 -->
    <div v-if="error" class="error-card">
      <div class="error-content">
        <div class="error-icon">⚠️</div>
        <div class="error-text">
          <h4>오류가 발생했습니다</h4>
          <p>{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import config from '@/api/apikeys.js';

export default {
  name: 'SearchBankView',
  data() {
    return {
      map: null,
      ps: null,
      userLocation: null,
      banks: [],
      loading: false,
      error: null,
      markers: [],
      statusMessage: '',
      mapInitialized: false
    }
  },
  mounted() {
    this.statusMessage = '카카오맵 API를 로드하는 중...';
    this.initMap();
  },
  methods: {
    initMap() {
      if (window.kakao && window.kakao.maps && window.kakao.maps.services) {
        this.statusMessage = '지도를 초기화하는 중...';
        this.createMap();
        return;
      }

      const script = document.createElement('script');
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${config.apiKey}&libraries=services&autoload=false`;
      
      script.onload = () => {
        if (window.kakao && window.kakao.maps) {
          window.kakao.maps.load(() => {
            this.statusMessage = '지도를 초기화하는 중...';
            this.createMap();
          });
        } else {
          this.error = '카카오맵 API 로드에 실패했습니다.';
          this.statusMessage = '';
        }
      };
      
      script.onerror = () => {
        this.error = '카카오맵 스크립트 로드에 실패했습니다. 네트워크 연결을 확인해주세요.';
        this.statusMessage = '';
      };
      
      document.head.appendChild(script);
    },
    
    createMap() {
      if (!window.kakao || !window.kakao.maps) {
        this.error = '카카오맵 API가 정상적으로 로드되지 않았습니다.';
        this.statusMessage = '';
        return;
      }

      try {
        const container = this.$refs.map;
        if (!container) {
          this.error = '지도 컨테이너를 찾을 수 없습니다.';
          this.statusMessage = '';
          return;
        }

        const options = {
          center: new window.kakao.maps.LatLng(37.5665, 126.9780),
          level: 3
        };
        
        this.map = new window.kakao.maps.Map(container, options);
        
        if (window.kakao.maps.services) {
          this.ps = new window.kakao.maps.services.Places();
        } else {
          this.error = '카카오맵 Places 서비스를 사용할 수 없습니다.';
          this.statusMessage = '';
          return;
        }
        
        this.mapInitialized = true;
        this.statusMessage = '';
        this.getCurrentLocation();
        
      } catch (error) {
        console.error('지도 생성 오류:', error);
        this.error = '지도 생성 중 오류가 발생했습니다.';
        this.statusMessage = '';
      }
    },
    
    getCurrentLocation() {
      if (!this.mapInitialized || !window.kakao || !window.kakao.maps) {
        this.error = '지도가 아직 준비되지 않았습니다. 잠시 후 다시 시도해주세요.';
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.statusMessage = '현재 위치를 확인하는 중...';
      
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            try {
              const lat = position.coords.latitude;
              const lng = position.coords.longitude;
              
              this.userLocation = new window.kakao.maps.LatLng(lat, lng);
              this.map.setCenter(this.userLocation);
              
              this.statusMessage = '사용자 위치 마커를 표시하는 중...';
              this.addUserMarker();
              
              this.statusMessage = '주변 은행을 검색하는 중...';
              this.searchNearbyBanks();
              
            } catch (error) {
              console.error('위치 처리 오류:', error);
              this.loading = false;
              this.error = '위치 정보 처리 중 오류가 발생했습니다.';
              this.statusMessage = '';
            }
          },
          (error) => {
            this.loading = false;
            this.statusMessage = '';
            
            switch(error.code) {
              case error.PERMISSION_DENIED:
                this.error = '위치 접근이 거부되었습니다. 브라우저 설정에서 위치 권한을 허용해주세요.';
                break;
              case error.POSITION_UNAVAILABLE:
                this.error = '위치 정보를 사용할 수 없습니다.';
                break;
              case error.TIMEOUT:
                this.error = '위치 정보 요청이 시간 초과되었습니다.';
                break;
              default:
                this.error = '위치 정보를 가져올 수 없습니다.';
                break;
            }
            console.error('위치 오류:', error);
          },
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 300000
          }
        );
      } else {
        this.loading = false;
        this.statusMessage = '';
        this.error = '이 브라우저는 위치 서비스를 지원하지 않습니다.';
      }
    },
    
    addUserMarker() {
      if (!this.userLocation || !window.kakao || !window.kakao.maps) {
        return;
      }

      try {
        const userMarker = new window.kakao.maps.Marker({
          position: this.userLocation,
          map: this.map
        });
        
        const userInfoWindow = new window.kakao.maps.InfoWindow({
          content: '<div style="padding:8px 12px; font-size:13px; font-weight:500; color:#22356F;">📍 현재 위치</div>'
        });
        
        userInfoWindow.open(this.map, userMarker);
        
      } catch (error) {
        console.error('사용자 마커 생성 오류:', error);
      }
    },
    
    searchNearbyBanks() {
      if (!this.ps || !this.userLocation || !window.kakao || !window.kakao.maps) {
        this.loading = false;
        this.error = '검색 서비스가 준비되지 않았습니다.';
        this.statusMessage = '';
        return;
      }

      const options = {
        location: this.userLocation,
        radius: 2000,
        sort: window.kakao.maps.services.SortBy.DISTANCE
      };
      
      this.ps.keywordSearch('은행', (data, status) => {
        this.loading = false;
        this.statusMessage = '';
        
        if (status === window.kakao.maps.services.Status.OK) {
          this.banks = data;
          this.displayBankMarkers(data);
        } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
          this.error = '주변 2km 내에서 은행을 찾을 수 없습니다.';
        } else if (status === window.kakao.maps.services.Status.ERROR) {
          this.error = '검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
        } else {
          this.error = '은행 검색에 실패했습니다.';
        }
      }, options);
    },
    
    displayBankMarkers(banks) {
      if (!window.kakao || !window.kakao.maps) {
        return;
      }

      try {
        this.markers.forEach(marker => marker.setMap(null));
        this.markers = [];
        
        banks.forEach((bank, index) => {
          const position = new window.kakao.maps.LatLng(bank.y, bank.x);
          
          const marker = new window.kakao.maps.Marker({
            position: position,
            map: this.map
          });
          
          const infoWindow = new window.kakao.maps.InfoWindow({
            content: `
              <div style="padding:12px 15px; min-width:200px; font-size:13px; font-family: 'Noto Sans KR', sans-serif;">
                <div style="font-weight:600; color:#22356F; margin-bottom:6px;">${bank.place_name}</div>
                <div style="color:#666; margin-bottom:4px; line-height:1.4;">${bank.address_name}</div>
                <div style="color:#D32F2F; font-weight:500; font-size:12px;">거리: ${bank.distance}m</div>
              </div>
            `
          });
          
          window.kakao.maps.event.addListener(marker, 'click', () => {
            infoWindow.open(this.map, marker);
          });
          
          this.markers.push(marker);
        });
        
      } catch (error) {
        console.error('마커 표시 오류:', error);
      }
    },
    
    moveToBank(bank) {
      if (!this.map || !window.kakao || !window.kakao.maps) {
        return;
      }

      try {
        const position = new window.kakao.maps.LatLng(bank.y, bank.x);
        this.map.setCenter(position);
        this.map.setLevel(2);
      } catch (error) {
        console.error('지도 이동 오류:', error);
      }
    }
  }
}
</script>

<style scoped>
.bank-finder {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
  min-height: 100vh;
}

/* 헤더 섹션 */
.header-section {
  background: linear-gradient(135deg, #22356F 0%, #1A2A5A 100%);
  border-radius: 16px;
  padding: 40px 30px;
  margin-bottom: 30px;
  text-align: center;
  box-shadow: 0 8px 25px rgba(34, 53, 111, 0.15);
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
}

.page-title {
  color: white;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.page-description {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  margin: 0 0 30px 0;
  line-height: 1.5;
}

.location-btn {
  background: white;
  color: #22356F;
  border: none;
  padding: 16px 32px;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.location-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.location-btn:disabled {
  background: rgba(255, 255, 255, 0.7);
  cursor: not-allowed;
  transform: none;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #E0E0E0;
  border-top: 2px solid #22356F;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 상태 메시지 */
.status-card {
  background: #E8F4FD;
  border: 1px solid #B3D9F7;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 20px;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #1565C0;
  font-size: 14px;
  font-weight: 500;
}

.status-icon {
  font-size: 18px;
}

/* 지도 섹션 */
.map-section {
  margin-bottom: 30px;
}

.map-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
}

#map {
  width: 100%;
  height: 450px;
}

/* 결과 섹션 */
.results-section {
  background: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #E0E0E0;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #F0F0F0;
}

.results-title {
  color: #22356F;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.results-count {
  color: #666;
  font-size: 14px;
  font-weight: 500;
  background: #F8F9FA;
  padding: 8px 16px;
  border-radius: 20px;
}

/* 은행 카드 그리드 */
.bank-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.bank-card {
  background: #FDFBF5;
  border: 1px solid #E8E6E0;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.bank-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(34, 53, 111, 0.12);
  border-color: #22356F;
}

.bank-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.bank-icon {
  font-size: 24px;
  padding: 8px;
  background: rgba(34, 53, 111, 0.1);
  border-radius: 8px;
}

.bank-distance {
  background: #D32F2F;
  color: white;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
}

.bank-content {
  margin-bottom: 20px;
}

.bank-name {
  color: #22356F;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.bank-address {
  color: #666;
  font-size: 14px;
  margin: 0 0 8px 0;
  line-height: 1.5;
}

.bank-phone {
  color: #27AE60;
  font-size: 14px;
  font-weight: 500;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.phone-icon {
  font-size: 12px;
}

.bank-actions {
  margin-top: auto;
}

.map-view-btn {
  width: 100%;
  background: #22356F;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.map-view-btn:hover {
  background: #1A2A5A;
}

/* 에러 카드 */
.error-card {
  background: #FFEBEE;
  border: 1px solid #FFCDD2;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
}

.error-content {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.error-icon {
  font-size: 24px;
  color: #D32F2F;
  flex-shrink: 0;
}

.error-text h4 {
  color: #D32F2F;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.error-text p {
  color: #B71C1C;
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .bank-finder {
    padding: 15px;
  }
  
  .header-section {
    padding: 30px 20px;
  }
  
  .page-title {
    font-size: 26px;
  }
  
  .results-section {
    padding: 20px;
  }
  
  .results-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
    text-align: center;
  }
  
  .bank-grid {
    grid-template-columns: 1fr;
  }
  
  #map {
    height: 350px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 22px;
  }
  
  .page-description {
    font-size: 14px;
  }
  
  .location-btn {
    padding: 14px 24px;
    font-size: 14px;
  }
  
  .bank-card {
    padding: 16px;
  }
  
  #map {
    height: 300px;
  }
}
</style>
