import streamlit as st
from view.language import get_text
from view.ui.bg import bg2, bg_cl  # type: ignore

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")
    
    st.title(get_text("slide3_title"))

    username = st.session_state.get("name", None)
    room_code = st.session_state.get("room_code", "DEFAULT")

    if "input_survive" not in st.session_state:
        st.session_state.input_survive = {}

    strategy = st.text_area(get_text("slide3_content"), height=150)

    if st.button(get_text("next_round")):
        if strategy:
            st.session_state.input_survive[username] = strategy
            st.session_state.page = "result"
            st.rerun()
        else:
            st.warning(get_text("error_occurred_restart"))
