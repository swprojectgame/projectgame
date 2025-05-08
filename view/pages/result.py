import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, get_result, reset_submissions
from logic.utils import get_random_situation
from logic.room_manager import assign_situation, load_rooms, save_rooms
import re

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "📢 AI의 판단 결과!",
        "restart": "처음으로",
        "next_round": "다음 라운드",
        "game_end": "🎉 모든 라운드가 종료되었습니다!",
        "game_over": "🔚 게임 종료",
        "result_heading": "🧠 결과",
        "survived": "생존",
        "died": "사망",
        "round_info": "라운드 {current} / {max}"
    },
    "en": {
        "title": "📢 AI Judgment Result!",
        "restart": "Restart",
        "next_round": "Next Round",
        "game_end": "🎉 All rounds have been completed!",
        "game_over": "🔚 Game Over",
        "result_heading": "🧠 Results",
        "survived": "Survived",
        "died": "Died",
        "round_info": "Round {current} / {max}"
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

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title(get_text("title"))

    code = st.session_state.room_code
    rooms = load_rooms()

    # ✅ 결과 불러오기 또는 생성
    result = get_result(code)
    if not result:
        result = generate_result(code)

    # 🔢 현재 라운드 / 총 라운드 수
    current_round = rooms[code].get("current_round", 1)
    max_round = rooms[code].get("total_rounds", 3)

    st.markdown(get_text("round_info", current=current_round, max=max_round))

    # ✅ 결과 표시 - 생존/사망 강조 표시
    st.subheader(get_text("result_heading"))
    
    # 결과에서 각 플레이어의 생존/사망 여부를 색상으로 강조
    highlighted_result = result
    
    # 생존/사망 판정 결과를 파싱하여 강조 표시
    lines = result.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip().startswith('-') or line.strip().startswith('*'):
            # 플레이어 결과 라인 형식: "- 플레이어이름: 생존/사망. 설명..."
            if "생존" in line or "survived" in line.lower() or "Survived" in line:
                formatted_lines.append(f"<div style='color: #00cc00; padding: 5px;'>{line}</div>")
            elif "사망" in line or "died" in line.lower() or "Died" in line:
                formatted_lines.append(f"<div style='color: #ff5555; padding: 5px;'>{line}</div>")
            else:
                formatted_lines.append(line)
        else:
            formatted_lines.append(line)
    
    # 강조된 결과 표시
    st.markdown("\n".join(formatted_lines), unsafe_allow_html=True)

    # ✅ 마지막 라운드일 경우: 종료 안내 및 버튼 제공
    if current_round >= max_round:
        st.success(get_text("game_end"))
        if st.button(get_text("game_over")):
            st.session_state.page = "end"
            st.rerun()
    else:
        # ✅ 다음 라운드로 진행
        if st.button(get_text("next_round")):
            assign_situation(code, get_random_situation())
            reset_submissions(code)
            rooms[code]["current_round"] = current_round + 1
            save_rooms(rooms)

            st.session_state.page = "scenario"
            st.rerun()
