import streamlit as st
from view.ui.bg import bg #type:ignore

def a1():
    bg("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXJqNTJibWh3bmtncHdyN2VwczN0azlzaWt0NGVyYnh6c2ozd3ByMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l3vRnoppYtfEbemBO/giphy.gif")
    st.title("AMI")
    st.write("시작 페이지입니다.")
    
    if st.button("게임 시작"):
        st.session_state.page = "lobby"
        st.rerun()