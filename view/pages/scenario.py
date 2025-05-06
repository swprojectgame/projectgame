import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import submit_scenario
from logic.room_manager import load_rooms

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")
    st.title("🧠 위기 상황에 대처하세요!")

    # 🔐 필수 세션 정보
    code = st.session_state.room_code
    name = st.session_state.player_name

    # ✅ 현재 플레이어의 상황 불러오기
    rooms = load_rooms()
    situation = rooms[code]["players"][name].get("situation", "상황 정보를 불러올 수 없습니다.")
    st.markdown(f"### 📖 현재 상황: {situation}")

    # ✅ 사용자 행동 입력
    action = st.text_area("💬 당신의 행동은?", key="action_input")

    # ✅ 제출 버튼 클릭 시 행동 저장 및 다음 페이지 이동
    if st.button("제출") and action.strip():
        submit_scenario(code, name, action.strip())
        st.session_state.page = "prompf"  # 대기 화면으로 전환
        st.rerun()
