## I. 팀원 정보 및 업무 분담 내역
| 이름 | 역할 | 담당 업무 | 
|------|--------|-----------|
| 김준수 | 팀장 / 백엔드 / 프론트엔드 | 금융상품 비교, 금융상품 소개, 마이페이지, 회원가입, 로그인/아웃, 회원정보 수정
| 윤설아 | 백엔드 / 프론트엔드 | 맞춤형 상품 추천, 환율 정보 조회, 금은시세 조회, 마이페이지, 홈

## II. 설계 내용 (아키텍처 등) 및 실제 구현 정도
### 📄 주요 화면별 기능 설명

| 화면 | 주요 기능 |
|------|-----------|
| 홈 화면 | 서비스 소개, 주요 기능 안내, 각 페이지로 이동할 수 있는 네비게이션 구성 |
| 금융상품 추천 결과 | 사용자 입력(나이, 자산, 목표 등)에 따라 맞춤형 금융상품 추천 결과를 카드 형태로 표시 |
| 금융상품 비교 | 추천된 상품들을 표 형식으로 나열하여 금리, 조건 등을 한눈에 비교 가능 |
| 금융상품 상세 | 개별 상품 클릭 시 상세 정보 출력 및 GPT-4를 통한 핵심 특징 한 줄 요약 제공 |
| 마이페이지 | 사용자가 가입한 예·적금 상품 목록 확인 및 선택 삭제 기능 제공 |
| 은행 검색 | 키워드 기반으로 은행명 검색 가능, 결과에 따라 관련 금융상품 탐색 가능 |
| 프로젝트 소개 | 프로젝트 목적, 팀 구성, 기술 스택 등 브랜딩 중심의 소개 페이지 구성 |
| 회원가입 및 로그인 | 사용자 계정 생성, 로그인, 간단한 유효성 검사 및 인증 흐름 구현 |
| 사용자 정보 관리 | 사용자의 기본 정보(나이, 자산, 성별 등) 확인 및 수정 기능 제공 |
| 금/은 시세 정보 | 실시간 금속 가격(금/은)을 그래프로 시각화, 과거 가격 데이터와 비교 가능 |
| 환율 정보 | 주요 국가 환율 조회 및 미니 차트로 국가별 환율 변동 시각화, 슬라이드 UI 적용 |

## 📊 사용자 흐름 요약 (Financial Flow)
![alt text](./ChatGPT%20Image%202025년%205월%2027일%20오후%2002_37_16.png)

## III. 데이터베이스 모델링 (ERD)
![ERD](./erd.png)

| 테이블명              | 설명                                                                 |
|----------------------|----------------------------------------------------------------------|
| **DepositProducts**  | 예금 상품의 기본 정보를 저장하는 테이블로, 상품명, 은행명, 가입 조건 등을 포함합니다. |
| **DepositOptions**   | 예금 상품의 금리 옵션을 저장하며, 기간별 금리(intr_rate)와 우대금리(intr_rate2)를 포함합니다. |
| **SavingProducts**   | 적금 상품의 기본 정보를 저장하며, 예금과 유사한 구조로 되어 있습니다.               |
| **SavingOptions**    | 적금 상품의 납입 기간 및 금리에 대한 정보를 저장합니다.                            |
| **User**             | 사용자 정보를 저장하는 테이블로, 이름, 나이, 성별, 자산 등의 정보를 포함합니다.     |

각 모델은 실제 금융 데이터 구조와 사용자 데이터를 효과적으로 관리할 수 있도록 설계되어 있으며, 추천 알고리즘과 사용자 인터랙션을 뒷받침하는 핵심적인 역할을 수행합니다.

## IV. 금융 상품 추천 알고리즘에 대한 기술적 설명

본 프로젝트는 사용자의 프로필(나이, 자산 수준, 재무 목표, 예·적금 선호)을 기반으로 맞춤형 금융상품을 추천하는 기능을 제공합니다. 알고리즘은 다음과 같은 순서로 동작합니다.

---

### 🔍 1. 사용자 프로필 입력

사용자는 아래 4가지 정보를 입력합니다:

- **나이(`age`)**: 10대, 20대, 30대, 40대, 50대, 60대 이상
- **자산(`asset`)**: ~300만, ~500만, 1억 이상 등
- **재무 목표(`goal`)**: 생활비, 주택, 노후 준비
- **상품 유형(`type`)**: 예금 or 적금

---

### 🔧 2. 상품 옵션 불러오기

입력된 `type` 값에 따라 다음 모델에서 데이터가 로드됩니다:

- `DepositOptions` (예금 상품)
- `SavingOptions` (적금 상품)

이때 `select_related('fin_prdt_cd')`로 상품 기본 정보와 조인하여 다음 데이터를 수집합니다:

- 상품명, 은행명, 기간(`save_trm`), 최고 우대금리(`intr_rate2`), 기타 정보, 우대 조건 등

---

### 🧠 3. 필터링 로직

사용자 성향에 따라 다단계 필터링을 적용합니다. 모든 조건은 **AND** 조건으로 작동합니다.

#### ✅ 나이에 따른 기간 필터링 이유

| 나이대    | 추천 기준               | 설정 이유 |
|-----------|--------------------------|-----------|
| 10·20대   | 단기 상품 (≤ 12개월)     | 유동성 확보가 중요하며, 목돈이 적고 단기 예치 선호도가 높습니다. 학자금·생활비 목적이 많습니다. |
| 30·40대   | 중기 상품 (12~24개월)    | 결혼·주택 준비 등 중기 자금 운용이 필요한 시기입니다. |
| 50대 이상 | 장기 상품 (≥ 24개월)     | 노후 자산 형성, 안정적 수익 추구를 위한 장기 예치 선호도가 높습니다. |

#### ✅ 재무 목표(goal)에 따른 필터링 이유

| 재무 목표     | 추천 기준                   | 설정 이유 |
|--------------|------------------------------|-----------|
| 생활비        | 단기 상품 (≤ 12개월)         | 자주 인출해야 하므로 유동성이 높은 단기 상품이 적합합니다. |
| 주택          | 장기 상품 (≥ 24개월)         | 장기 계획에 맞춘 자금 준비가 필요합니다. |
| 노후 준비     | 우대금리 3.0% 이상 상품 추천 | 수익률 중심의 자산 운용이 중요합니다. |

#### ✅ 자산 수준(asset)에 따른 필터링 이유

| 자산 수준       | 추천 기준                  | 설정 이유 |
|------------------|-----------------------------|-----------|
| ~300만 / ~500만  | 우대금리 2.0% 이상 추천     | 소액 자산일수록 금리 혜택이 중요한 요소입니다. |
| 1억 이상         | 우대금리 3.5% 이상 추천     | 고자산 보유자는 수익률에 민감하여 더 높은 금리를 선호합니다. |

---

### 🌟 4. 우대금리 기준 상위 추천 상품 추출

- 필터링된 결과를 `intr_rate2` (우대금리) 기준으로 내림차순 정렬
- **중복 상품명을 제거**하여 다양한 상품을 추천
- 상위 3개의 금융 상품을 최종 추천 목록으로 제공합니다

---

### 🧾 5. API 호출 및 응답 예시

- `POST /gpt_recommendation` 요청 시 추천 결과를 반환합니다.

```json
{
  "recommendation": [
    {
      "fin_prdt_cd": "...",
      "fin_prdt_nm": "...",
      "kor_co_nm": "...",
      "save_trm": 12,
      "intr_rate2": 3.2,
      "etc_note": "...",
      "spcl_cnd": "...",
      "join_way": "..."
    },
    ...
  ]
}