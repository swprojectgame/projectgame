import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")
    
    st.title("당신은 어떻게 생존하시겠습니까?")

    username = st.session_state.get("name", None)
    room_code = st.session_state.get("room_code", "DEFAULT")

    if "input_survive" not in st.session_state:
        st.session_state.input_survive = {}

    strategy = st.text_area("생존 전략을 세워보세요.", height=150)

    if st.button("전략 제출"):
        if strategy:
            st.session_state.input_survive[username] = strategy
            st.success("전략이 저장되었습니다.")
        else:
            st.warning("오류가 발생했습니다. 게임을 다시 시작해주세요.")

    # 결과 페이지로 이동 및 GPT 호출
    if st.button("제출"):
        st.session_state.page = "result"
        st.rerun()
