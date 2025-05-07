import json
import os
import random
import string

ROOM_FILE = "rooms.json"

# 🔄 JSON 파일에서 방 정보 불러오기
def load_rooms():
    if not os.path.exists(ROOM_FILE):
        return {}
    with open(ROOM_FILE, "r") as f:
        return json.load(f)

# 💾 JSON 파일에 방 정보 저장
def save_rooms(rooms):
    with open(ROOM_FILE, "w") as f:
        json.dump(rooms, f, indent=2)

# 🏗 방 생성 (중복 없는 랜덤 코드)
def create_room(rounds=3):  # 기본값으로 3라운드
    rooms = load_rooms()
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if code not in rooms:
            rooms[code] = {
                "players": {},
                "status": "waiting",
                "situation": "",
                "result": "",
                "current_round": 1,
                "total_rounds": rounds  # ✅ total_rounds는 이후 lobby에서 수정됨
            }
            save_rooms(rooms)
            return code



# 🚪 플레이어가 방에 입장
def join_room(code, name):
    rooms = load_rooms()
    if code in rooms:
        if name not in rooms[code]["players"]:
            rooms[code]["players"][name] = {
                "submitted": False,
                "scenario": "",
                "situation": ""
            }
            save_rooms(rooms)
        return True
    return False

# 👥 현재 플레이어 목록 반환
def get_players(code):
    rooms = load_rooms()
    return list(rooms.get(code, {}).get("players", {}).keys())

# 🚀 방의 게임 상태를 '시작됨'으로 설정
def start_game(code):
    rooms = load_rooms()
    if code in rooms:
        rooms[code]["status"] = "started"
        save_rooms(rooms)

# 🔍 방의 게임 상태가 '시작됨'인지 확인
def is_game_started(code):
    rooms = load_rooms()
    return rooms.get(code, {}).get("status") == "started"

# 🎲 주어진 상황을 모든 플레이어에게 배정
def assign_situation(code, situation):
    rooms = load_rooms()
    if code in rooms:
        rooms[code]["situation"] = situation
        for player in rooms[code]["players"].values():
            player["situation"] = situation
        save_rooms(rooms)
