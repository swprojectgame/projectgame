import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import submit_scenario
from logic.room_manager import load_rooms

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "🧠 위기 상황에 대처하세요!",
        "current_situation": "📖 현재 상황: {situation}",
        "action_input": "💬 당신의 행동은?",
        "submit": "제출"
    },
    "en": {
        "title": "🧠 Deal with the Crisis!",
        "current_situation": "📖 Current Situation: {situation}",
        "action_input": "💬 What's your action?",
        "submit": "Submit"
    }
}

def get_text(key, **kwargs):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    text = TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환
    
    # 포맷팅이 필요한 경우 처리
    if kwargs:
        text = text.format(**kwargs)
        
    return text

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")
    st.title(get_text("title"))

    # 🔐 필수 세션 정보
    code = st.session_state.room_code
    name = st.session_state.player_name

    # ✅ 현재 플레이어의 상황 불러오기
    rooms = load_rooms()
    situation = rooms[code]["players"][name].get("situation", "상황 정보를 불러올 수 없습니다.")
    st.markdown(get_text("current_situation", situation=situation))

    # ✅ 사용자 행동 입력
    action = st.text_area(get_text("action_input"), key="action_input")

    # ✅ 제출 버튼 클릭 시 행동 저장 및 다음 페이지 이동
    if st.button(get_text("submit")) and action.strip():
        submit_scenario(code, name, action.strip())
        st.session_state.page = "prompf"  # 대기 화면으로 전환
        st.rerun()
