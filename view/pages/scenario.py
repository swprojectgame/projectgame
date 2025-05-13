import streamlit as st
from logic.utils import get_random_situation
from view.language import get_text
from view.ui.bg import bg2, bg_cl  # type: ignore


def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")

    st.title(get_text("title_scenario_input"))

    if "scenario" not in st.session_state:
        st.session_state.scenario = ""

    st.session_state.scenario = st.text_area(
        get_text("input_label_scenario"),
        value=st.session_state.scenario,
        height=200
    )

    if st.button(get_text("recommend_button")):
        st.session_state.scenario = get_random_situation()
        st.rerun()

    if st.button(get_text("submit")):
        if st.session_state.scenario.strip():
            st.session_state.page = "prompf"
            st.rerun()
        else:
            st.warning(get_text("warning_empty"))
