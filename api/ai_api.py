# 🔁 GPT API 없이 테스트 가능한 더미 버전

def generate_response(prompt):
    # 테스트용 고정 응답 반환
    return (
        "테스트용 결과입니다.\n"
        "- 제임스: 생존. 침착하게 대처했다!\n"
        "- 민지: 사망. AI는 그녀를 외면했다...\n"
        "- 태훈: 생존. 깃털 한 장으로 기적을 만들었다!\n"
    )

# ✅ 실제 API 호출용 코드 (나중에 활성화하면 됨)
"""
from openai import OpenAI

client = OpenAI(api_key="sk-여기에_너의_키")

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 죽음의 게임을 운영하는 AI 심판입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT 오류] {e}"
"""

## api 호출하는 법
## from api.ai_api import generate_response

## st.write(generate_response("이 상황에서 어떻게 해야 살아남을까?"))
