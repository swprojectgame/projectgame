# 🔁 GPT API 없이 테스트 가능한 더미 버전

import os
import openai

def generate_response(prompt):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 공정하고 창의적인 죽음의 심판관입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 응답 생성 중 오류 발생: {str(e)}"

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
