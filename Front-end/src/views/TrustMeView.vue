<template>
  <div class="trustme-page">
    <div class="slogan">
      믿을 수 있게, 고를 수 있게<br />믿고름
    </div>

    <div class="description">
      믿고름은 금융의 세계에 첫 발을 내딛는 사람들에게,<br />
      가장 먼저 떠올릴 수 있는 든든한 길잡이가 되고자 합니다.<br /><br />
      믿고름은 또 하나의 금융 플랫폼이 아니라<br />
      내가 믿고 고르는 방법의 시작입니다.
    </div>

    <div class="bi-wrapper">
    <div class="bi-title">
      BI소개<br />
      <span class="underline">────────────</span>
    </div>

    <div class="bi-gradient-box"></div>

    <img class="bi-image" src="@/assets/logo_icon.png" alt="믿고름 BI 이미지" />

    <div class="bi-subtitle">Symbol & Wordmark</div>

    <div class="bi-description">
      신뢰(✓)와 탐색(🔎)을 형상화한 심볼과, 따뜻한 금융 경험을 담은 워드마크가 만나<br />
      믿고름의 브랜드 가치를 표현합니다.
    </div>
    </div>
  </div>
</template>

<script setup>
// No JS needed
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.trustme-page {
  max-width: 100vw;
  background: #EDF0F2;
  font-family: 'Inter', sans-serif;
  text-align: center;
  box-sizing: border-box;
  overflow-x: hidden;
  position: relative;
  padding-top: 90px;
}

.slogan {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 40px;
  color: #000;
}

.bi-wrapper {
  padding: 0 20px;
}

.description {
  font-size: 1.25rem;
  font-weight: 300;
  line-height: 1.8;
  margin-bottom: 80px;
  color: #222;
}

.bi-title {
  font-size: 2.2rem;
  font-weight: 500;
  margin-top: 150px;
  margin-bottom: 10px;
  color: #000;
}

.underline {
  display: block;
  margin-top: 10px;
  font-size: 1.5rem;
}

.bi-gradient-box {
  width: 100vw;
  height: 300px;
  background: linear-gradient(90deg, #22356F 0%, #4166D5 90%);
  display: flex;
  justify-content: center;
  align-items: flex-start; /* ← 여기서 center → flex-start */
  padding-top: 20px; /* 여백 조절 가능 */
  box-sizing: border-box;
}

.bi-gradient-box {
  width: 100vw;
  height: 270px;
  background: linear-gradient(90deg, #22356F 0%, #4166D5 90%);
  z-index: 1; /* 박스는 뒤쪽에 */
  position: relative;
  margin-bottom: 30px;
}

.bi-image {
  position: absolute;
  top: 750px; /* 필요시 조절 */
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999; /* 가장 앞쪽 */
  max-width: 300px;
  pointer-events: none; /* 클릭 방해 안 되게 하려면 */
}

.bi-subtitle {
  font-size: 1.75rem;
  font-weight: 300;
  margin-bottom: 20px;
}

.bi-description {
  font-size: 1.25rem;
  font-weight: 300;
  line-height: 2;
  color: #333;
}
</style>
