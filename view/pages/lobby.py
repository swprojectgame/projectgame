import streamlit as st
from logic.room_manager import get_players, start_game, is_game_started, load_rooms, save_rooms
from view.ui.bg import bg  # type: ignore
from streamlit_autorefresh import st_autorefresh

def a2():
    bg()
    st.title("🧑‍🤝‍🧑 Death by AI - 로비")

    st_autorefresh(interval=1000, limit=None, key="lobby_autorefresh")

    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error("방 코드 또는 닉네임 정보가 없습니다. 다시 시작해주세요.")
        return

    room_code = st.session_state.room_code
    player_name = st.session_state.player_name
    players = get_players(room_code)

    if is_game_started(room_code):
        st.session_state.page = "scenario"
        st.rerun()

    st.markdown(f"### 🔑 방 코드: `{room_code}`")
    st.button("📋 코드 복사하기", on_click=lambda: st.toast("복사되었습니다! (직접 복사해주세요)", icon="📎"))

    st.markdown("---")
    st.subheader("👥 현재 참가자")
    for p in players:
        st.markdown(f"- {p}")
    st.markdown("---")

    # ✅ 방장만 라운드 수 설정
    if players and players[0] == player_name:
        rounds = st.number_input("진행할 라운드 수를 선택하세요", min_value=1, max_value=10, value=3, step=1)

        if st.button("🚀 게임 시작"):
            rooms = load_rooms()
            rooms[room_code]["status"] = "started"
            rooms[room_code]["current_round"] = 1
            rooms[room_code]["total_rounds"] = rounds  # ✅ 여기서 설정
            save_rooms(rooms)

            st.session_state.page = "scenario"
            st.rerun()
    else:
        st.info("방장이 게임 시작을 눌러야 시작됩니다. 기다려주세요!")
