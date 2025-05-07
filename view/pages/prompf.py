import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import check_all_submitted

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")
    st.title("⏳ 다른 플레이어들의 입력을 기다리는 중...")

    # 🔐 필수 정보
    code = st.session_state.room_code

    # ✅ 모든 플레이어가 제출했는지 확인
    if check_all_submitted(code):
        st.session_state.page = "result"
        st.rerun()
    else:
        time.sleep(2)  # 2초 대기 후 새로고침
        st.rerun()
