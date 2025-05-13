#result.py 이후로 나오는 게임 종료 화면
import streamlit as st
from view.ui.bg import bg  # 배경 유지
from logic.room_manager import load_rooms
from logic.game_flow import get_survival_count
from view.language import get_text

def a6():
    bg()
    
    # 영어로 표시되도록 언어 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    st.title(get_text("title_end"))

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
                
                # 생존/사망 결과를 색상으로 구분하여 표시
                survived_text = f"<span style='color: #00cc00;'>{get_text('survived')}: {survived_count}</span>"
                died_text = f"<span style='color: #ff5555;'>{get_text('died')}: {died_count}</span>"
                
                # 이모티콘 표시
                survived_emoji = "😄 " * survived_count
                died_emoji = "💀 " * died_count
                
                # 플레이어 결과 표시
                st.markdown(f"**{player_name}**: {survived_text} | {died_text}", unsafe_allow_html=True)
                st.markdown(f"{survived_emoji}{died_emoji}")
                
                # 승리 여부 표시 (가장 많이 생존한 플레이어)
                if "max_survived" not in locals() or survived_count > locals()["max_survived"]:
                    locals()["max_survived"] = survived_count
                    locals()["winner"] = player_name
            
            # 승자 표시
            if "winner" in locals():
                st.markdown("---")
                st.markdown(f"### 🏆 {locals()['winner']}")

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
    
    # CSS로 시작 화면과 라운드 관련 UI 요소 숨기기
    st.markdown("""
    <style>
    /* 시작 화면 숨기기 */
    .stApp header {
        display: none !important;
    }
    
    /* 라운드 선택 및 관련 UI 요소 숨기기 */
    div.stNumberInput, p:contains("진행할 라운드 수를 선택하세요"),
    div:contains("라운드"), p:contains("라운드"), input[type="number"] {
        display: none !important;
    }
    
    /* 로비 화면에서 넘어온 요소들 숨기기 */
    div:contains("게임 방법"), div:contains("게임 시작"), button:contains("게임 방법"), button:contains("게임 시작"), 
    div:contains("참가자"), button:contains("복사"), div:contains("방 코드"), 
    div.stSlider, div.element-container:has(button:contains("게임 시작")) {
        display: none !important;
    }
    
    /* 슬라이드 관련 요소 숨기기 */
    div.slide-container, div:contains("슬라이드"), div.element-container:has(div.slide-container) {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
