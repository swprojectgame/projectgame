import streamlit as st
from view.ui.hide_bar import hide_bar_ui
from view.ui.bg import bg
from view.pages import start, lobby, scenario, prompt, result, end 
from logic.url_router import handle_url_params

# 트랜지션 관련 페이지 이동 로직이 있다면 초기화
handle_url_params()

# UI 요소
hide_bar_ui()  # 상단 바 숨김

# 세션에 page가 없으면 시작 페이지로 설정
if "page" not in st.session_state:
    st.session_state.page = "start"

# 페이지 전환 처리
if st.session_state.page == "start":
    start.a1()
elif st.session_state.page == "lobby":
    lobby.a2()
elif st.session_state.page == "scenario":
    scenario.a3()
elif st.session_state.page == "prompt":
    prompt.a4()
elif st.session_state.page == "result":
    result.a5()
elif st.session_state.page == "end":
    end.a6()
