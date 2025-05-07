import streamlit as st
from view.pages import scenario
from view.ui.bg import bg
from view.ui.upd import fx1
import time


def a2():
    bg("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXJqNTJibWh3bmtncHdyN2VwczN0azlzaWt0NGVyYnh6c2ozd3ByMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l3vRnoppYtfEbemBO/giphy.gif")

    if "fx1_phase" not in st.session_state:
        st.session_state.fx1_phase = None

    st.title("ㅁㄴㅇㅀㄴㅁㅇㄹ")

    if st.button("참가"):
        st.session_state.fx1_played = True
        st.session_state.page = "fx1"  # 페이지 상태 fx1으로 전환
        st.rerun()

    elif st.session_state.get("page") == "fx1":
        fx1()
        st.session_state.page = "scenario"  # 애니메이션 후 reload 되면 scenario로 이동

    elif st.session_state.get("page") == "scenario":
        scenario.a3()

