import json
import os
import random
import string
import streamlit as st  # streamlit import 필요

ROOM_FILE = "rooms.json"

# 🔄 방 정보 로드 함수
def load_rooms():
    if not os.path.exists(ROOM_FILE):
        return {}
    with open(ROOM_FILE, "r") as f:
        return json.load(f)

# 💾 방 정보 저장 함수
def save_rooms(rooms):
    with open(ROOM_FILE, "w") as f:
        json.dump(rooms, f, indent=2)

# 🏗 방 생성 함수 (중복 방지)
def create_room():
    rooms = load_rooms()
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if code not in rooms:
            rooms[code] = {"players": []}
            save_rooms(rooms)
            return code

# 🚪 방 입장 함수
def join_room(code, name):
    # ✅ 디버깅: 들어온 파라미터 확인
    st.write("🧪 [join_room] room_code =", repr(code))
    st.write("🧪 [join_room] player_name =", repr(name))

    rooms = load_rooms()
    if code in rooms:
        if name not in rooms[code]["players"]:
            rooms[code]["players"].append(name)
            save_rooms(rooms)
        return True
    return False

# 👥 플레이어 목록 반환 함수
def get_players(code):
    rooms = load_rooms()
    return rooms.get(code, {}).get("players", [])
