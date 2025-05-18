import streamlit as st

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        # start.py
        "title": "🎮 A.M.I",
        "nickname": "닉네임을 입력하세요:",
        "create_room": "🆕 방 만들기",
        "join_room": "🔑 방 코드로 입장",
        "room_created": "✅ 방이 생성되었습니다! 코드: {code}",
        "already_in_room": "이미 '{code}' 방에 입장 중입니다.",
        "enter_nickname_first": "닉네임을 먼저 입력하세요.",
        "enter_room_code": "참여할 방 코드를 입력하세요:",
        "enter": "입장하기",
        "invalid_code": "🚫 유효하지 않은 방 코드입니다.",
        
        # lobby.py
        "title_lobby": "A.M.I - 로비",
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
        "slide1_title": "1. 파티 타임",
        "slide1_content": "게임을 만들고 친구를 초대하세요",
        "slide2_title": "2. 치명적인 시나리오",
        "slide2_content": "치명적인 시나리오를 선택하십시오. 예) '좁고 밀폐된 지하 벙커에 갇혔습니다'",
        "slide3_title": "3. 생존 전략",
        "slide3_content": "생존을 위해 전략을 입력하십시오.",
        "slide4_title": "4. AI 판정",
        "slide4_content": "AI가 플레이어의 전략이 생존할 가치가 있는지 여부를 결정합니다.",
        "slide5_title": "5. 승리 조건",
        "slide5_content": "라운드 후 사망 횟수가 가장 적은 플레이어가 승리합니다.",
        
        # scenario.py
        "title_scenario": "어떤 상황을 연출하시겠습니까?",
        "current_situation": "현재 상황: ",
        "submit": "제출",
        "input_label_scenario": "시나리오를 작성해주세요",
        "notice": "타이머가 끝나면 자동으로 다음 페이지로 넘어갑니다.",
        "recommend_button": "추천 시나리오",
        "file_missing": "⚠️ 시나리오 파일이 존재하지 않습니다.",
        "list_empty": "⚠️ 시나리오 리스트가 비어 있습니다.",
        "warning_empty": "시나리오를 입력하거나 추천 시나리오를 선택해주세요.",
        "submit_warning": "제출 버튼을 클릭해야 작성한 내용이 저장됩니다 !!!",

        # prompt.py
        "title_prompt": "⏳ 다른 플레이어들의 입력을 기다리는 중...",
        "waiting": "모든 플레이어의 입력을 기다리고 있습니다.",
        "judging": "판단 중···",
        "finalizing": "당신의 운명이 결정되었습니다!",
        "error_occurred_restart": "오류가 발생했습니다. 게임을 다시 시작해주세요.",
        "survival_strategy": "생존 전략",
        "input_strategy": "생존 전략을 입력하세요.",
        "default_strategy": "적절한 생존 전략을 택한다.",
        
        # result.py
        "title_result": "AI의 판단 결과!",
        "restart": "처음으로",
        "next_round": "다음 라운드",
        "game_end": "🎉 모든 라운드가 종료되었습니다!",
        "game_over": "🔚 게임 종료",
        "survived": "생존",
        "died": "사망",
        "round_info": "라운드 {current} / {max}",
        "back_to_lobby": "로비로 돌아가기",
        "warning_empty": "플레이어 목록 또는 생존 전략이 없습니다.",
        
        # end.py
        "title_end": "🏁 게임 종료",
        "congrats": "🎉 생존과 죽음의 AI 게임이 끝났습니다.",
        "restart_info": "🔁 다시 시작하려면 아래 버튼을 클릭하세요.",
        "restart": "다시 시작하기",
        "thanks": "감사합니다! 😊",
        "results_title": "📊 플레이어 생존 결과",
        "player": "플레이어",
        "total_rounds": "총 라운드: {rounds}"
    },
    "en": {
        # start.py
        "title": "🎮 A.M.I",
        "nickname": "Enter your nickname:",
        "create_room": "🆕 Create Room",
        "join_room": "🔑 Join with Room Code",
        "room_created": "✅ Room created! Code: {code}",
        "already_in_room": "Already in room '{code}'.",
        "enter_nickname_first": "Please enter your nickname first.",
        "enter_room_code": "Enter the room code:",
        "enter": "Enter",
        "invalid_code": "🚫 Invalid room code.",
        
        # lobby.py
        "title_lobby": "A.M.I - Lobby",
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
        "slide1_title": "1. Party Time",
        "slide1_content": "Create a game and invite your friends",
        "slide2_title": "2. Deadly Scenario",
        "slide2_content": "Choose a deadly scenario. Example: 'Trapped in a narrow, enclosed underground bunker'",
        "slide3_title": "3. Survival Strategy",
        "slide3_content": "Enter your strategy for survival.",
        "slide4_title": "4. AI Judgment",
        "slide4_content": "AI determines whether players' strategies are worth surviving.",
        "slide5_title": "5. Victory Condition",
        "slide5_content": "The player with the fewest deaths after rounds wins.",
        
        # scenario.py
        "title_scenario": "What kind of situation do you want to create?",
        "current_situation": "Current Situation: ",
        "submit": "Submit",
        "input_label_scenario": "Please write your scenario",
        "notice": "You will be automatically redirected when the timer runs out.",
        "recommend_button": "Suggest a Scenario",
        "file_missing": "⚠️ Scenario file is missing.",
        "list_empty": "⚠️ Scenario list is empty.",
        "warning_empty": "Please enter a scenario or select a suggested one.",
        "submit_warning": "You must click the submit button to save your input !!!",

        # prompt.py
        "title_prompt": "⏳ Waiting for other players' input...",
        "waiting": "Waiting for all players to submit their actions.",
        "judging": "Judging···",
        "finalizing": "Your fate has been decided!",
        "error_occurred_restart": "An error occurred. Please restart the game.",
        "survival_strategy": "Survival Strategy",
        "input_strategy": "Input your strategy to survive",
        "default_strategy": "Choose an appropriate survival tactic.",
        
        # result.py
        "title_result": "AI Judgment Result!",
        "restart": "Restart",
        "next_round": "Next Round",
        "game_end": "🎉 All rounds have been completed!",
        "game_over": "🔚 Game Over",
        "survived": "Survived",
        "died": "Died",
        "round_info": "Round {current} / {max}",
        "back_to_lobby": "Return to Lobby",
        "warning_empty": "No player list or survival strategies found.",
        
        # end.py
        "title_end": "🏁 Game Over",
        "congrats": "🎉 The AI game of survival and death has ended.",
        "restart_info": "🔁 Click the button below to restart.",
        "restart": "Restart Game",
        "thanks": "Thank you! 😊",
        "results_title": "📊 Player Survival Results",
        "player": "Player",
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