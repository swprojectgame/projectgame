import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, get_result, reset_submissions
from logic.utils import get_random_situation
from logic.room_manager import assign_situation, load_rooms, save_rooms

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title("📢 AI의 판단 결과!")

    code = st.session_state.room_code
    rooms = load_rooms()

    # ✅ 결과 불러오기 또는 생성
    result = get_result(code)
    if not result:
        result = generate_result(code)

    # 🔢 현재 라운드 / 총 라운드 수
    current_round = rooms[code].get("current_round", 1)
    max_round = rooms[code].get("total_rounds", 3)

    st.markdown(f"**라운드 {current_round} / {max_round}**")

    # ✅ 결과 표시
    st.text_area("🧠 결과", result, height=300)

    # ✅ 마지막 라운드일 경우: 종료 안내 및 버튼 제공
    if current_round >= max_round:
        st.success("🎉 모든 라운드가 종료되었습니다!")
        if st.button("🔚 게임 종료"):
            st.session_state.page = "end"
            st.rerun()
    else:
        # ✅ 다음 라운드로 진행
        if st.button("다음 라운드"):
            assign_situation(code, get_random_situation())
            reset_submissions(code)
            rooms[code]["current_round"] = current_round + 1
            save_rooms(rooms)

            st.session_state.page = "scenario"
            st.rerun()
