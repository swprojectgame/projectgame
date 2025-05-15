import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, get_result, reset_submissions, update_survival_records
from logic.room_manager import load_rooms, save_rooms
from view.language import get_text

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    
    # 영어로 표시되도록 언어 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    st.title(get_text("title_result"))

    code = st.session_state.room_code
    rooms = load_rooms()

    # 🔢 현재 라운드 / 총 라운드 수
    current_round = rooms[code].get("current_round", 1)
    max_round = rooms[code].get("total_rounds", 3)
    
    # ✅ 결과 불러오기 또는 생성
    result_data = get_result(code)
    if not result_data:
        result_data = generate_result(code)

    # 튜플로 반환될 경우 처리
    if isinstance(result_data, tuple):
        result = result_data[0] or "결과가 없습니다."
    else:
        result = result_data

    # ✅ 결과 표시
    st.subheader(get_text("result_heading"))
    st.text_area("", result, height=300)

    # ✅ 플레이어들의 생존 전략 표시
    st.subheader(get_text("submitted_strategies"))
    players = rooms[code]["players"]
    for player_name, player_data in players.items():
        strategy = player_data.get("strategy", get_text("no_strategy"))
        st.markdown(f"**{player_name}**: {strategy}")

    # 라운드 정보 표시
    st.subheader(f"Round {current_round}/{max_round}")

    # ✅ 마지막 라운드일 경우: 종료 안내 및 버튼 제공
    if current_round >= max_round:
        st.success(get_text("game_end"))
        if st.button(get_text("game_over")):
            if result:
                update_survival_records(code, result)
            st.session_state.page = "end"
            st.rerun()
    else:
        if st.button(get_text("next_round")):
            if result:
                update_survival_records(code, result)
            
            # 현재 라운드 결과가 제대로 저장되었는지 확인
            rooms = load_rooms()
            rooms[code]["current_round"] = current_round + 1
            save_rooms(rooms)

            # 제출 상태 초기화
            reset_submissions(code)

            # 다음 라운드 화면으로 이동
            st.session_state.page = "scenario"
            st.rerun()
