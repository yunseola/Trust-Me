import openai
import os

client = openai.OpenAI(api_key=os.getenv("API_KEY_GPT"))

def summarize_deposit_product(name, bank, etc_note, spcl_cnd, join_member, join_way):
    prompt = f"""
당신은 금융상품 소개를 위한 마케팅 문구를 작성하는 요약 전문가입니다.
아래 예금 상품 정보를 바탕으로 **은행명과 상품명을 제외한**, 핵심 특징을 **20자 이내로 매우 간단하게** 요약해 주세요.

✅ 조건:
- 최대 30자
- 문장은 하나
- 핵심 기능 또는 장점만 담기
- 불필요한 수식어, 접속사, 설명 절대 금지
- 예시:
  - "우대조건 없는 단순예금"
  - "자유로운 회전기간 설정가능한 예금"
  - "실세금리 적용 예금"

--- 예금 상품 설명 ---
기타 설명: {etc_note}
우대 조건: {spcl_cnd}
가입 대상: {join_member}
가입 방법: {join_way}
-----------------------

한 줄 요약 (30자 이내):
"""


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100,
    )

    return response.choices[0].message.content.strip()
