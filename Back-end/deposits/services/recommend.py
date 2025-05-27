import openai
import os

client = openai.OpenAI(api_key=os.getenv("API_KEY_GPT"))

def recommend_products(profile):
    prompt = f"""
    아래 사용자 조건에 맞는 예금 금융상품 3개를 추천해 주세요. 
    각 상품은 간단한 설명(한 줄 요약 포함)을 함께 제공해 주세요.

    [사용자 조건]
    - 연령대: {profile['age']}
    - 자산 규모: {profile['asset']}
    - 금융 목적: {profile['goal']}
    - 상품 유형: {profile['type']}

    [출력 형식 예시]
    1. 상품명: OO예금 / 설명: 복잡한 조건 없이 자유롭게 가입 가능한 간편 예금
    2. 상품명: OO적금 / 설명: 젊은 세대가 소액으로 시작할 수 있는 생활비 절약형 상품
    3. 상품명: OO예금 / 설명: 실세금리를 적용받을 수 있는 단기 수익형 예금
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
