import streamlit as st
from logic.room_manager import get_players, start_game, is_game_started, load_rooms, save_rooms, assign_random_situation_to_all
from view.ui.bg import bg  # type: ignore
from streamlit_autorefresh import st_autorefresh
import time
from datetime import datetime
import json
from streamlit.components.v1 import html
from view.language import get_text

def a2():
    bg()
    
    # CSS 스타일 추가: 라운드 선택란에서 - + 버튼만 작동하도록 설정
    st.markdown("""
    <style>
    /* 라운드 선택 input 숨기고 스텝퍼(-/+) 버튼만 표시 */
    .stNumberInput input[type="number"] {
        pointer-events: none;
        background-color: #f0f2f6;
        color: #31333F;
    }
    
    /* 숨겨진 -/+ 버튼은 활성화 */
    .stNumberInput [data-testid="stNumberInputIncrement"], 
    .stNumberInput [data-testid="stNumberInputDecrement"] {
        pointer-events: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 설정 상태 관리
    if "show_settings" not in st.session_state:
        st.session_state.show_settings = False
    
    # 언어 설정 초기화
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    # 🔄 1초마다 자동 새로고침 (설정 화면에서는 새로고침 안함)
    if not st.session_state.show_settings:
        st_autorefresh(interval=1000, limit=None, key="lobby_autorefresh")
    
    # 🔐 필수 정보 확인
    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error(get_text("room_code_missing"))
        return
    
    room_code = st.session_state.room_code
    player_name = st.session_state.player_name
    
    # ✅ 참가자도 게임 시작 여부 확인 후 자동 이동
    if is_game_started(room_code):
        st.session_state.page = "scenario"
        st.rerun()
    
    # 게임 방법 슬라이드 상태 관리
    if "show_game_rules" not in st.session_state:
        st.session_state.show_game_rules = False
    if "rule_slide" not in st.session_state:
        st.session_state.rule_slide = 0
    if "slide_start_time" not in st.session_state:
        st.session_state.slide_start_time = datetime.now()
    
    # 설정 화면 또는 로비 화면 표시
    if st.session_state.show_settings:
        show_settings_screen()
    else:
        show_lobby_screen(room_code, player_name)

def show_settings_screen():
    """설정 화면을 표시합니다."""
    # 헤더 부분
    st.title(get_text("settings_title"))
    
    # 설정 컨테이너 스타일링 - 배경색 제거
    settings_container_style = """
    <style>
    .settings-container {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .settings-section {
        margin-bottom: 20px;
    }
    </style>
    """
    st.markdown(settings_container_style, unsafe_allow_html=True)
    
    # 메인 설정 컨테이너
    st.markdown('<div class="settings-container">', unsafe_allow_html=True)
    
    # 언어 설정 섹션
    st.subheader(get_text("language_settings"))
    
    # 언어 선택 라디오 버튼
    selected_language = st.selectbox(
        get_text("select_language"),
        options=["ko", "en"],
        format_func=lambda x: get_text("korean") if x == "ko" else get_text("english"),
        index=0 if st.session_state.language == "ko" else 1
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 버튼 컨테이너
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(get_text("back_to_lobby"), use_container_width=True):
            st.session_state.show_settings = False
            st.rerun()
            
    with col2:
        if st.button(get_text("save_settings"), use_container_width=True):
            # 언어 설정 저장
            st.session_state.language = selected_language
            st.success(get_text("settings_saved"))
            time.sleep(1)
            st.rerun()

def show_lobby_screen(room_code, player_name):
    """로비 화면을 표시합니다."""
    # 헤더 부분에 제목과 설정 버튼 배치
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.title(get_text("title"))
    
    with col2:
        if st.button(get_text("settings"), key="settings_title_btn"):
            st.session_state.show_settings = True
            st.rerun()
    
    # 자동 슬라이드 타이머 체크 (3초)
    if st.session_state.show_game_rules:
        current_time = datetime.now()
        time_diff = (current_time - st.session_state.slide_start_time).total_seconds()
        
        if time_diff >= 3 and st.session_state.rule_slide < 4:  # 마지막 슬라이드 전까지만 자동 넘김
            st.session_state.rule_slide += 1
            st.session_state.slide_start_time = current_time
            st.rerun()
    
    # 🎮 방 코드 표시
    st.markdown(f"### 🔑 {get_text('room_code_label')}: `{room_code}`")
    st.button("📋 " + get_text("copy_code"), on_click=lambda: st.toast(get_text("copied"), icon="📎"))

    # 👥 플레이어 목록 표시
    st.markdown("---")
    st.subheader("👥 " + get_text("participants"))
    players = get_players(room_code)

    for p in players:
        st.markdown(f"- {p}")

    st.markdown("---")
    
    # 버튼 행 만들기 - 게임 방법 버튼만 표시
    if st.button("🎲 " + get_text("game_rules"), key="game_rules_btn"):
        st.session_state.show_game_rules = True
        st.session_state.rule_slide = 0
        st.session_state.slide_start_time = datetime.now()
        st.rerun()
    
    # 게임 방법 슬라이드 표시
    if st.session_state.show_game_rules:
        show_game_rules_slides()

    # 🧑‍💼 방장만 게임 시작 가능 (첫 입장자)
    if players and players[0] == player_name:
        # 라운드 수 설정 추가 - 기존 UI 복원
        rounds = st.number_input(get_text("select_rounds"), min_value=1, max_value=5, value=3, step=1)
        
        if st.button("🚀 " + get_text("start_game")):
            # rooms.json에 라운드 수 설정 저장
            rooms = load_rooms()
            rooms[room_code]["status"] = "started"
            rooms[room_code]["current_round"] = 1
            rooms[room_code]["total_rounds"] = rounds  # ✅ 라운드 수 설정
            
            # round_situations 필드 초기화
            if "round_situations" not in rooms[room_code]:
                rooms[room_code]["round_situations"] = {}
            
            # 방정보 저장
            save_rooms(rooms)
            
            # 첫 라운드 상황을 즉시 할당
            assign_random_situation_to_all(room_code)
            
            st.session_state.page = "scenario"
            st.rerun()
    else:
        st.info(get_text("wait_for_host"))

def show_game_rules_slides():
    """게임 규칙을 슬라이드쇼 형식으로 표시합니다."""
    
    # 슬라이드 내용
    slides = [
        {
            "title": get_text("slide1_title"),
            "content": get_text("slide1_content"),
            "image": "👥"
        },
        {
            "title": get_text("slide2_title"),
            "content": get_text("slide2_content"),
            "image": "🏚️"
        },
        {
            "title": get_text("slide3_title"),
            "content": get_text("slide3_content"),
            "image": "💡"
        },
        {
            "title": get_text("slide4_title"),
            "content": get_text("slide4_content"),
            "image": "🤖"
        },
        {
            "title": get_text("slide5_title"),
            "content": get_text("slide5_content"),
            "image": "🏆"
        }
    ]
    
    # 현재 슬라이드 표시
    current_slide = slides[st.session_state.rule_slide]
    
    # 타이머 계산
    current_time = datetime.now()
    elapsed_seconds = (current_time - st.session_state.slide_start_time).total_seconds()
    remaining_seconds = max(0, 3 - elapsed_seconds)
    progress_percentage = (3 - remaining_seconds) / 3 * 100  # 진행도 퍼센트
    
    # 슬라이드 컨테이너
    with st.container():
        st.markdown(f"## {current_slide['image']} {current_slide['title']}")
        st.info(current_slide['content'])
        
        # 네비게이션 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.rule_slide > 0:
                if st.button("◀️ " + get_text("prev"), key="prev_slide"):
                    st.session_state.rule_slide -= 1
                    st.session_state.slide_start_time = datetime.now()
                    st.rerun()
        
        with col2:
            # 진행 표시기 및 타이머
            progress_dots = []
            for i in range(len(slides)):
                if i == st.session_state.rule_slide:
                    # 현재 슬라이드 - 물이 차오르는 효과로 변경
                    water_color = "#1E90FF"  # 더 푸른 색으로 변경
                    wave_bottom = progress_percentage-5 if progress_percentage > 5 else 0
                    
                    # 물이 차오르는 효과를 위한 스타일 추가
                    timer_circle = f"""
                    <div style="position: relative; display: inline-block; margin: 0 5px;">
                        <div style="width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; position: relative; overflow: hidden;">
                            <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: {progress_percentage}%; background-color: {water_color}; 
                                transition: height 0.3s ease-out; box-shadow: 0 0 5px rgba(30, 144, 255, 0.5) inset; z-index: 1;">
                            </div>
                            <!-- 물결 효과 -->
                            <div style="position: absolute; bottom: {wave_bottom}%; left: -5px; width: 130%; height: 3px; 
                                background-color: rgba(255, 255, 255, 0.4); border-radius: 50%; z-index: 2;
                                animation: wave1 1.5s infinite ease-in-out;">
                            </div>
                            <div style="position: absolute; bottom: {wave_bottom-2 if wave_bottom > 2 else 0}%; left: -5px; width: 130%; height: 2px; 
                                background-color: rgba(255, 255, 255, 0.3); border-radius: 50%; z-index: 2;
                                animation: wave2 1.8s infinite ease-in-out;">
                            </div>
                        </div>
                    </div>
                    <style>
                    @keyframes wave1 {{
                        0% {{ transform: translateX(-5px); }}
                        50% {{ transform: translateX(5px); }}
                        100% {{ transform: translateX(-5px); }}
                    }}
                    @keyframes wave2 {{
                        0% {{ transform: translateX(5px); }}
                        50% {{ transform: translateX(-5px); }}
                        100% {{ transform: translateX(5px); }}
                    }}
                    </style>
                    """
                    progress_dots.append(timer_circle)
                else:
                    # 다른 슬라이드 - 일반 동그라미
                    progress_dots.append('<div style="display: inline-block; margin: 0 5px;"><span style="color: white;">○</span></div>')
            
            st.markdown(f"<div style='text-align: center;'>{''.join(progress_dots)}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.session_state.rule_slide < len(slides) - 1:
                if st.button(get_text("next") + " ▶️", key="next_slide"):
                    st.session_state.rule_slide += 1
                    st.session_state.slide_start_time = datetime.now()
                    st.rerun()
            else:
                if st.button("✖️ " + get_text("close"), key="close_slides"):
                    st.session_state.show_game_rules = False
                    st.rerun()
