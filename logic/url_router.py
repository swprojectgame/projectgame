import streamlit as st
from logic.room_manager import join_room

def handle_url_params():
    # ✅ Streamlit URL 쿼리 파라미터에서 값을 꺼낼 때 리스트일 수도 있어서 첫 번째 값만 추출해주는 함수
    def normalize_param(value):
        if isinstance(value, list):
            return value[0]
        return value

    # 🔍 현재 URL의 쿼리 파라미터 추출 (?room=XXXX&name=YYYY)
    params = st.query_params
    room = normalize_param(params.get("room"))  # 방 코드
    name = normalize_param(params.get("name"))  # 플레이어 이름

    # 🐞 디버깅용 로그 출력
    st.write("🛠️ [디버깅] room (raw):", repr(room))
    st.write("🛠️ [디버깅] name (raw):", repr(name))

    # ✅ 방 코드와 이름이 모두 있고, 아직 방에 들어간 상태가 아니라면 자동 입장 처리
    if room and name and "room_code" not in st.session_state:
        # 디버깅 로그 출력
        st.write("🧪 [join_room] room_code =", room)
        st.write("🧪 [join_room] player_name =", name)

        # 🚪 join_room() 함수로 서버에 입장 시도
        joined = join_room(room, name)
        st.write("🧩 [디버깅] join_room 성공 여부:", joined)

        if joined:
            # ✅ 세션 상태에 사용자 정보 저장
            st.session_state.room_code = room
            st.session_state.player_name = name
            st.session_state.page = "lobby"  # 👉 로비 페이지로 자동 이동
