import streamlit as st
from view.ui.bg import bg2,bg_cl  # type: ignore

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "결과",
        "restart": "처음으로",
        "next_round": "다음 라운드"
    },
    "en": {
        "title": "Results",
        "restart": "Restart",
        "next_round": "Next Round"
    }
}

def get_text(key):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    return TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title(get_text("title"))

    # 두 개의 버튼을 나란히 배치
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(get_text("restart"), use_container_width=True):
            # 언어 설정을 제외한 세션 상태 초기화
            # 현재 language 값 저장
            current_language = st.session_state.language
            
            # 방 정보 초기화
            if "room_code" in st.session_state:
                del st.session_state.room_code
            if "player_name" in st.session_state:
                del st.session_state.player_name
            
            # 게임 관련 상태 초기화
            for key in list(st.session_state.keys()):
                if key not in ["language", "page"]:
                    del st.session_state[key]
                    
            # language 값 복원
            st.session_state.language = current_language
            
            # 시작 페이지로 이동
            st.session_state.page = "start"
            st.rerun()
    
    with col2:
        if st.button(get_text("next_round"), use_container_width=True):
            # 다음 시나리오 라운드로 이동
            st.session_state.page = "scenario"
            st.rerun()
