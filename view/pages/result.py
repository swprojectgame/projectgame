import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, get_result, reset_submissions
from logic.utils import get_random_situation, get_different_situation
from logic.room_manager import assign_situation, load_rooms, save_rooms
from view.language import get_text

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title(get_text("title_result"))

    code = st.session_state.room_code
    rooms = load_rooms()

    # ✅ 결과 불러오기 또는 생성
    result = get_result(code)
    if not result:
        result = generate_result(code)

    # 🔢 현재 라운드 / 총 라운드 수
    current_round = rooms[code].get("current_round", 1)
    max_round = rooms[code].get("total_rounds", 3)

    # ✅ 결과 표시
    st.subheader(get_text("result_heading"))
    st.text_area("", result, height=300)

    # ✅ 마지막 라운드일 경우: 종료 안내 및 버튼 제공
    if current_round >= max_round:
        st.success(get_text("game_end"))
        if st.button(get_text("game_over")):
            st.session_state.page = "end"
            st.rerun()
    else:
        # ✅ 다음 라운드로 진행
        if st.button(get_text("next_round")):
            # 현재 시나리오 확인
            current_situation = rooms[code].get("situation", "")
            
            # 항상 이전과 다른 시나리오 할당
            new_situation = get_different_situation(current_situation)
            
            # 상황 적용
            assign_situation(code, new_situation)
            reset_submissions(code)
            rooms[code]["current_round"] = current_round + 1
            save_rooms(rooms)
            
            # 다음 라운드 화면으로 이동
            st.session_state.page = "scenario"
            st.rerun()
            
    # CSS로 라운드 선택 및 표시 UI 요소 숨기기
    st.markdown("""
    <style>
    /* 불필요한 라운드 선택 및 표시 UI 요소 숨기기 */
    div.stNumberInput, p:contains("진행할 라운드 수를 선택하세요"), 
    div:contains("라운드"), p:contains("라운드") {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
