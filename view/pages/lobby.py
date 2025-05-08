import streamlit as st
from logic.room_manager import get_players, start_game, is_game_started, load_rooms, save_rooms
from view.ui.bg import bg  # type: ignore
from streamlit_autorefresh import st_autorefresh
import time
from datetime import datetime
import json
from streamlit.components.v1 import html

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "🧑‍🤝‍🧑 Death by AI - 로비",
        "settings": "⚙️ 설정",
        "language_settings": "🌐 언어 설정",
        "select_language": "언어 선택",
        "korean": "한국어",
        "english": "영어",
        "save_settings": "설정 저장",
        "settings_saved": "설정이 저장되었습니다!",
        "room_code_missing": "방 코드 또는 닉네임 정보가 없습니다. 다시 시작해주세요.",
        "room_code_label": "방 코드",
        "copy_code": "코드 복사하기",
        "copied": "복사되었습니다! (직접 복사해주세요)",
        "participants": "현재 참가자",
        "game_rules": "게임 방법",
        "start_game": "게임 시작",
        "wait_for_host": "방장이 게임 시작을 눌러야 시작됩니다. 기다려주세요!",
        "prev": "이전",
        "next": "다음",
        "close": "닫기",
        "game_settings": "게임 설정",
        "settings_title": "⚙️ 게임 설정",
        "back_to_lobby": "로비로 돌아가기",
        "game_mode": "게임 모드",
        "normal_mode": "일반 모드",
        "advanced_mode": "고급 모드",
        "personality": "AI 성격",
        "voice_volume": "음성 볼륨",
        "music_volume": "음악 볼륨",
        "round_length": "라운드 길이",
        "short": "짧게",
        "medium": "보통",
        "long": "길게",
        "select_rounds": "진행할 라운드 수를 선택하세요",
        # 슬라이드 내용
        "slide1_title": "1. 파티 타임",
        "slide1_content": "게임을 만들고 친구를 초대하세요",
        "slide2_title": "2. 치명적인 시나리오",
        "slide2_content": "치명적인 시나리오를 선택하십시오. 예) '좁고 밀폐된 지하 벙커에 갇혔습니다'",
        "slide3_title": "3. 생존 전략",
        "slide3_content": "생존을 위해 전략을 입력하십시오.",
        "slide4_title": "4. AI 판정",
        "slide4_content": "AI가 플레이어의 전략이 생존할 가치가 있는지 여부를 결정합니다.",
        "slide5_title": "5. 승리 조건",
        "slide5_content": "라운드 후 사망 횟수가 가장 적은 플레이어가 승리합니다."
    },
    "en": {
        "title": "🧑‍🤝‍🧑 Death by AI - Lobby",
        "settings": "⚙️ Settings",
        "language_settings": "🌐 Language Settings",
        "select_language": "Select Language",
        "korean": "Korean",
        "english": "English",
        "save_settings": "Save Settings",
        "settings_saved": "Settings saved successfully!",
        "room_code_missing": "Room code or nickname information is missing. Please restart.",
        "room_code_label": "Room Code",
        "copy_code": "Copy Code",
        "copied": "Copied! (Please copy manually)",
        "participants": "Current Participants",
        "game_rules": "Game Rules",
        "start_game": "Start Game",
        "wait_for_host": "The host needs to start the game. Please wait!",
        "prev": "Previous",
        "next": "Next",
        "close": "Close",
        "game_settings": "Game Settings",
        "settings_title": "⚙️ Game Settings",
        "back_to_lobby": "Back to Lobby",
        "game_mode": "Game Mode",
        "normal_mode": "Normal Mode",
        "advanced_mode": "Advanced Mode",
        "personality": "AI Personality",
        "voice_volume": "Voice Volume",
        "music_volume": "Music Volume",
        "round_length": "Round Length", 
        "short": "Short",
        "medium": "Medium",
        "long": "Long",
        "select_rounds": "Select the number of rounds to play",
        # 슬라이드 내용
        "slide1_title": "1. Party Time",
        "slide1_content": "Create a game and invite your friends",
        "slide2_title": "2. Deadly Scenario",
        "slide2_content": "Choose a deadly scenario. Example: 'Trapped in a narrow, enclosed underground bunker'",
        "slide3_title": "3. Survival Strategy",
        "slide3_content": "Enter your strategy for survival.",
        "slide4_title": "4. AI Judgment",
        "slide4_content": "AI determines whether players' strategies are worth surviving.",
        "slide5_title": "5. Victory Condition",
        "slide5_content": "The player with the fewest deaths after rounds wins."
    }
}

def get_text(key):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    return TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환

def a2():
    bg()
    
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
            # 언어 설정만 저장
            previous_lang = st.session_state.language
            st.session_state.language = selected_language
            
            st.success(get_text("settings_saved"))
            st.session_state.show_settings = False
            
            # 언어가 변경되었다면 페이지 새로고침
            if previous_lang != selected_language:
                st.rerun()
            else:
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
        # 라운드 수 설정 추가
        rounds = st.number_input(get_text("select_rounds"), min_value=1, max_value=5, value=3, step=1)
        
        if st.button("🚀 " + get_text("start_game")):
            # rooms.json에 라운드 수 설정 저장
            rooms = load_rooms()
            rooms[room_code]["status"] = "started"
            rooms[room_code]["current_round"] = 1
            rooms[room_code]["total_rounds"] = rounds  # ✅ 라운드 수 설정
            save_rooms(rooms)
            
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
