import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "시나리오 작성",
        "submit": "제출"
    },
    "en": {
        "title": "Write a Scenario",
        "submit": "Submit"
    }
}

def get_text(key):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    return TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")
    st.title(get_text("title"))

    if st.button(get_text("submit")):
        st.session_state.page = "prompf"
        st.rerun()