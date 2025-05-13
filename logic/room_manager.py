import json
import os
import random
import string
import streamlit as st  # streamlit import 필요
from logic.utils import get_random_situation, get_different_situation

ROOM_FILE = "rooms.json"

# 🔄 JSON 파일에서 방 정보 불러오기
def load_rooms():
    if not os.path.exists(ROOM_FILE):
        return {}
    
    try:
        with open(ROOM_FILE, "r") as f:
            rooms = json.load(f)
        
        # 기존 방 구조 업그레이드 (round_situations 필드 추가)
        upgraded = False
        for code in rooms:
            if "round_situations" not in rooms[code]:
                rooms[code]["round_situations"] = {}
                upgraded = True
        
        # 변경된 경우 저장
        if upgraded:
            with open(ROOM_FILE, "w") as f:
                json.dump(rooms, f, indent=2)
        
        return rooms
    except Exception as e:
        return {}

# 💾 JSON 파일에 방 정보 저장
def save_rooms(rooms):
    with open(ROOM_FILE, "w") as f:
        json.dump(rooms, f, indent=2)

# 🏗 방 생성 (중복 없는 랜덤 코드)
def create_room(rounds=3):
    rooms = load_rooms()
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if code not in rooms:
            rooms[code] = {
                "players": {},          # 각 플레이어 정보 (딕셔너리)
                "status": "waiting",    # 대기 상태
                "situation": "",        # 현재 라운드 상황 (방 전체 기준)
                "result": "",           # GPT 결과 저장용
                "current_round": 1,     # 현재 라운드
                "total_rounds": rounds, # 총 라운드 수
                "round_situations": {}  # 라운드별 상황 저장 (추가)
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
                "situation": "",
                "survived_count": 0  # 생존 횟수 초기화
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
        # 게임 시작시 첫 라운드의 상황 초기화
        if "round_situations" not in rooms[code]:
            rooms[code]["round_situations"] = {}
        save_rooms(rooms)

# 🔍 방의 게임 상태가 '시작됨'인지 확인
def is_game_started(code):
    rooms = load_rooms()
    return rooms.get(code, {}).get("status") == "started"

# 🎲 상황을 모든 플레이어에게 동일하게 배정 (기존 함수)
def assign_situation(code, situation):
    rooms = load_rooms()
    if code in rooms:
        current_round = rooms[code].get("current_round", 1)
        
        # 현재 라운드 상황 저장
        if "round_situations" not in rooms[code]:
            rooms[code]["round_situations"] = {}
        rooms[code]["round_situations"][str(current_round)] = situation
        
        # 방 전체 상황 업데이트
        rooms[code]["situation"] = situation
        
        # 각 플레이어 상황 업데이트
        for player in rooms[code]["players"].values():
            player["situation"] = situation
            
        save_rooms(rooms)

# 현재 라운드의 상황 가져오기
def get_current_round_situation(code):
    rooms = load_rooms()
    if code in rooms:
        current_round = rooms[code].get("current_round", 1)
        round_situations = rooms[code].get("round_situations", {})
        
        # 현재 라운드 상황 반환
        situation = round_situations.get(str(current_round), "")
        return situation
    return ""

# 라운드별 상황 정보 모두 가져오기
def get_all_round_situations(code):
    rooms = load_rooms()
    if code in rooms:
        return rooms[code].get("round_situations", {})
    return {}

# 🎲 라운드마다 새로운 무작위 상황을 모든 플레이어에게 동일하게 배정
def assign_random_situation_to_all(code):
    rooms = load_rooms()
    if code in rooms:
        # 현재 라운드 확인
        current_round = rooms[code].get("current_round", 1)
        
        # 현재 상황 가져오기
        current_situation = rooms[code].get("situation", "")
        
        # round_situations 필드가 없으면 초기화
        if "round_situations" not in rooms[code]:
            rooms[code]["round_situations"] = {}
        
        # 이미 사용된 모든 상황 목록 (중복 방지)
        used_situations = list(rooms[code]["round_situations"].values())
        
        # 현재 상황과 이전에 사용한 모든 상황이 아닌 새로운 상황 선택
        available_situations = []
        
        if "language" in st.session_state and st.session_state.language == "en":
            from logic.utils import SITUATIONS_EN
            all_situations = SITUATIONS_EN
            available_situations = [s for s in SITUATIONS_EN if s not in used_situations]
        else:
            from logic.utils import SITUATIONS
            all_situations = SITUATIONS
            available_situations = [s for s in SITUATIONS if s not in used_situations]
        
        # 사용 가능한 상황이 없으면 모든 상황에서 현재 상황만 제외하고 선택
        if not available_situations:
            available_situations = [s for s in all_situations if s != current_situation]
            
        # 혹시라도 available_situations가 비어 있을 경우 (매우 드문 경우)
        if not available_situations and len(all_situations) > 1:
            available_situations = [s for s in all_situations if s != current_situation]
        elif not available_situations and len(all_situations) <= 1:
            # 상황이 1개뿐이면 어쩔 수 없이 그것을 사용
            available_situations = all_situations
        
        # 새 상황 선택
        new_situation = random.choice(available_situations)
        
        # 현재 선택된 상황과 이전 라운드 상황이 같은지 확인
        prev_round = current_round - 1
        prev_situation = rooms[code]["round_situations"].get(str(prev_round), "")
        
        # 만약 이전 라운드와 같은 상황이 선택되었다면, 다시 선택 시도
        max_attempts = 5  # 최대 5번 시도
        attempts = 0
        
        while new_situation == prev_situation and attempts < max_attempts and len(available_situations) > 1:
            new_situation = random.choice(available_situations)
            attempts += 1
        
        # 라운드별 상황 저장
        rooms[code]["round_situations"][str(current_round)] = new_situation
        
        # 방 전체의 상황 저장
        rooms[code]["situation"] = new_situation
        
        # 모든 플레이어에게 같은 상황 배정
        for player_name in rooms[code]["players"]:
            rooms[code]["players"][player_name]["situation"] = new_situation
        
        save_rooms(rooms)
        return True
    return False
