import openai
import os

API_KEY = os.getenv("API_KEY_GPT")

print("API_KEY:", API_KEY)  # Debugging line to check if the API key is loaded correctly

client = openai.OpenAI(api_key=os.getenv("API_KEY_GPT"))

def summarize_deposit_product(name, bank, etc_note, spcl_cnd, join_member, join_way):
    prompt = f"""
    아래는 예금 상품에 대한 상세 설명입니다.
    이를 참고해 **은행 이름이나 상품명을 제외하고**, 해당 상품의 특징을 **한 줄로 간단하고 실용적인 스타일**로 요약해 주세요.

    ✅ 주의사항:
    - 은행명, 상품명은 절대 포함하지 마세요
    - 핵심 특징 위주로 간결하게 적어주세요
    - 예: "복잡한 우대조건 없이 목돈을 굴릴 수 있는 정기예금", "회전주기를 직접 선택할 수 있는 실세금리 적용 상품" 등

    --- 예금 상품 설명 ---
    기타 설명: {etc_note}
    우대 조건: {spcl_cnd}
    가입 대상: {join_member}
    가입 방법: {join_way}
    -----------------------

    한 줄 요약:
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100,
    )

    return response.choices[0].message.content.strip()
