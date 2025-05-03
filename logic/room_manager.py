import json
import os
import random
import string

# 저장할 JSON 파일 경로
ROOM_FILE = "rooms.json"

# 🔄 방 정보 로드 함수
def load_rooms():
    """
    rooms.json 파일에서 모든 방 정보를 불러온다.
    파일이 없으면 빈 딕셔너리를 반환.
    """
    if not os.path.exists(ROOM_FILE):
        return {}
    with open(ROOM_FILE, "r") as f:
        return json.load(f)

# 💾 방 정보 저장 함수
def save_rooms(rooms):
    """
    전체 방 정보를 rooms.json에 저장한다.
    """
    with open(ROOM_FILE, "w") as f:
        json.dump(rooms, f)

# 🏗 방 생성 함수
def create_room():
    """
    랜덤한 4자리 코드로 방을 생성하고, 초기화된 방 정보를 저장한다.
    """
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    rooms = load_rooms()
    rooms[code] = {"players": []}
    save_rooms(rooms)
    return code

# 🚪 방 입장 함수
def join_room(code, name):
    """
    주어진 방 코드에 유저를 참가시킨다.
    유효한 방 코드일 경우 True, 아니면 False 반환.
    """
    rooms = load_rooms()
    if code in rooms:
        if name not in rooms[code]["players"]:
            rooms[code]["players"].append(name)
            save_rooms(rooms)
        return True
    return False

# 👥 플레이어 목록 반환 함수
def get_players(code):
    """
    방 코드에 해당하는 플레이어 목록을 반환한다.
    존재하지 않는 방일 경우 빈 리스트 반환.
    """
    rooms = load_rooms()
    return rooms.get(code, {}).get("players", [])
