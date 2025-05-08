#result.py 이후로 나오는 게임 종료 화면
import streamlit as st
from view.ui.bg import bg  # 배경 유지
from logic.room_manager import load_rooms
from logic.game_flow import get_survival_count

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "🏁 게임 종료",
        "game_end": "모든 라운드가 종료되었습니다!",
        "congrats": "🎉 생존과 죽음의 AI 게임이 끝났습니다.",
        "restart_info": "🔁 다시 시작하려면 아래 버튼을 클릭하세요.",
        "restart": "다시 시작하기",
        "thanks": "감사합니다! 😊",
        "results_title": "📊 플레이어 생존 결과",
        "player": "플레이어",
        "survived": "생존",
        "died": "사망",
        "total_rounds": "총 라운드: {rounds}"
    },
    "en": {
        "title": "🏁 Game Over",
        "game_end": "All rounds have been completed!",
        "congrats": "🎉 The AI game of survival and death has ended.",
        "restart_info": "🔁 Click the button below to restart.",
        "restart": "Restart Game",
        "thanks": "Thank you! 😊",
        "results_title": "📊 Player Survival Results",
        "player": "Player",
        "survived": "Survived",
        "died": "Died",
        "total_rounds": "Total Rounds: {rounds}"
    }
}

def get_text(key, **kwargs):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    text = TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환
    
    # 포맷팅이 필요한 경우 처리
    if kwargs:
        text = text.format(**kwargs)
        
    return text

def a6():
    bg()
    st.title(get_text("title"))

    st.success(get_text("game_end"))
    st.markdown(f"### {get_text('congrats')}")

    # 방 정보 가져오기
    if "room_code" in st.session_state:
        room_code = st.session_state.room_code
        rooms = load_rooms()
        
        if room_code in rooms:
            # 결과 표시 구역
            st.markdown("---")
            st.subheader(get_text("results_title"))
            
            # 총 라운드 수 표시
            total_rounds = rooms[room_code].get("total_rounds", 5)
            st.markdown(get_text("total_rounds", rounds=total_rounds))
            
            # 플레이어 간단 결과 표시
            for player_name, player_data in rooms[room_code]["players"].items():
                survived_count = player_data.get("survived_count", 0)
                died_count = total_rounds - survived_count
                
                # 생존/사망 이모티콘 생성
                survived_emoji = "😄 " * survived_count
                died_emoji = "💀 " * died_count
                
                # 플레이어 결과 표시 (생존이 먼저 오도록 순서 변경)
                st.markdown(f"**{player_name}**: {survived_emoji}{died_emoji}")

    st.markdown("---")
    st.info(get_text("restart_info"))
    
    if st.button(get_text("restart")):
        # 언어 설정을 제외한 세션 상태 초기화
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
        
    st.markdown(get_text("thanks"))
