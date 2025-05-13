import streamlit as st
from view.ui.hide_bar import hide_bar_ui
from view.ui.bg import bg
from view.pages import start, lobby, scenario, prompt, result, end  # ✅ prompf 제거

# logic
from logic.url_router import handle_url_params
handle_url_params()

# ui
hide_bar_ui()  # 상단 바 숨김

# page 시작
if "page" not in st.session_state:
    st.session_state.page = "start"

# 페이지 전환 처리
if st.session_state.page == "start":
    start.a1()
elif st.session_state.page == "lobby":
    lobby.a2()
elif st.session_state.page == "scenario":
    scenario.a3()
elif st.session_state.page == "prompt":  # ✅ prompf → prompt
    prompt.a4()
elif st.session_state.page == "result":
    result.a5()
elif st.session_state.page == "end":
    end.a6()
