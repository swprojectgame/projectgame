import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "생존 전략 작성",
        "submit": "제출"
    },
    "en": {
        "title": "Write a Survival Strategy",
        "submit": "Submit"
    }
}

def get_text(key):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    return TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")
    st.title(get_text("title"))

    if st.button(get_text("submit")):
        st.session_state.page = "result"
        st.rerun()