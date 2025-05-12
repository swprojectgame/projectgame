import streamlit as st
from view.ui.bg import bg


def a2():
    bg("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXJqNTJibWh3bmtncHdyN2VwczN0azlzaWt0NGVyYnh6c2ozd3ByMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l3vRnoppYtfEbemBO/giphy.gif")
    st.title("ㅁㄴㅇㅀㄴㅁㅇㄹ")

    if st.button("참가"):
        st.session_state.page = "scenario"
        st.rerun()
