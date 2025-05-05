import streamlit as st
from logic.room_manager import get_players, start_game, is_game_started
from view.ui.bg import bg  # type: ignore
from streamlit_autorefresh import st_autorefresh

def a2():
    bg()
    st.title("🧑‍🤝‍🧑 Death by AI - 로비")

    # 🔄 1초마다 자동 새로고침
    st_autorefresh(interval=1000, limit=None, key="lobby_autorefresh")

    # 🔐 필수 정보 확인
    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error("방 코드 또는 닉네임 정보가 없습니다. 다시 시작해주세요.")
        return

    room_code = st.session_state.room_code
    player_name = st.session_state.player_name

    # ✅ 참가자도 게임 시작 여부 확인 후 자동 이동
    if is_game_started(room_code):
        st.session_state.page = "scenario"
        st.rerun()

    # 🎮 방 코드 표시
    st.markdown(f"### 🔑 방 코드: `{room_code}`")
    st.button("📋 코드 복사하기", on_click=lambda: st.toast("복사되었습니다! (직접 복사해주세요)", icon="📎"))

    # 👥 플레이어 목록 표시
    st.markdown("---")
    st.subheader("👥 현재 참가자")
    players = get_players(room_code)

    for p in players:
        st.markdown(f"- {p}")

    st.markdown("---")

    # 🧑‍💼 방장만 게임 시작 가능 (첫 입장자)
    if players and players[0] == player_name:
        if st.button("🚀 게임 시작"):
            start_game(room_code)
            st.session_state.page = "scenario"
            st.rerun()
    else:
        st.info("방장이 게임 시작을 눌러야 시작됩니다. 기다려주세요!")
