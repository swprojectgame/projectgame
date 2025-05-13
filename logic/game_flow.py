from logic.room_manager import (
    load_rooms,
    save_rooms
)
from api.ai_api import generate_response  # 🔁 GPT API 호출 함수 사용
import re
import streamlit as st

# ✅ 유저가 행동을 제출
def submit_scenario(code, name, scenario):
    rooms = load_rooms()
    if code in rooms and name in rooms[code]["players"]:
        rooms[code]["players"][name]["scenario"] = scenario
        rooms[code]["players"][name]["submitted"] = True
        save_rooms(rooms)
        return True
    return False

# ✅ 모든 유저가 제출 완료했는지 확인
def check_all_submitted(code):
    rooms = load_rooms()
    if code in rooms:
        return all(p.get("submitted", False) for p in rooms[code]["players"].values())
    return False

# ✅ 결과 생성 (GPT 호출)
def generate_result(code):
    rooms = load_rooms()
    if code not in rooms:
        return None

    # 언어 확인
    is_english = "language" in st.session_state and st.session_state.language == "en"

    # 프롬프트 구성
    if is_english:
        prompt = "You are a fair and creative judge of death.\n"
        prompt += "Here are the players' responses to crisis situations:\n\n"

        for name, player in rooms[code]["players"].items():
            situation = player.get("situation", "")
            action = player.get("scenario", "")
            prompt += f"Player '{name}'\n"
            prompt += f"Situation: {situation}\n"
            prompt += f"Action: {action}\n"
            prompt += f"Result: "

        prompt += (
            "\n\nPlease judge each player's survival in a humorous and dramatic way. "
            "Format the results as follows:\n"
            "- James: Died. The shotgun was fake...\n"
            "- Minji: Survived. The trap she set earlier caught the lion!\n"
        )
    else:
        prompt = "당신은 공정하고 창의적인 죽음의 심판관입니다.\n"
        prompt += "다음은 플레이어들이 위기 상황에 대응한 내용입니다.\n\n"

        for name, player in rooms[code]["players"].items():
            situation = player.get("situation", "")
            action = player.get("scenario", "")
            prompt += f"플레이어 '{name}'\n"
            prompt += f"상황: {situation}\n"
            prompt += f"행동: {action}\n"
            prompt += f"결과: "

        prompt += (
            "\n\n각 플레이어의 생존 여부를 유머러스하고 극적으로 판단해 주세요. "
            "결과는 다음과 같이 출력합니다:\n"
            "- 제임스: 사망. 샷건은 가짜였다...\n"
            "- 민지: 생존. 미리 설치해둔 덫이 사자를 잡았다!\n"
        )

    try:
        result_text = generate_response(prompt)  # ✅ ai_api.py에서 GPT 호출
    except Exception as e:
        if is_english:
            result_text = f"[GPT Error] {e}"
        else:
            result_text = f"[GPT 오류] {e}"

    rooms[code]["result"] = result_text
    
    # ✅ 결과 파싱하여 생존 여부 기록
    update_survival_records(code, result_text)
    
    save_rooms(rooms)
    return result_text

# ✅ 저장된 결과 불러오기
def get_result(code):
    rooms = load_rooms()
    return rooms.get(code, {}).get("result", "")

# ✅ 다음 라운드를 위해 제출 상태 초기화
def reset_submissions(code):
    rooms = load_rooms()
    if code in rooms:
        # 현재 라운드 정보 확인
        current_round = rooms[code].get("current_round", 1)
        
        # 각 플레이어의 제출 상태 초기화
        for player_name, player_data in rooms[code]["players"].items():
            player_data["submitted"] = False
            player_data["scenario"] = ""
            
            # 이전 라운드 결과가 다음 라운드에 영향을 미치지 않도록
            # 라운드별 결과가 올바르게 저장되었는지 확인
            if "rounds_results" not in player_data:
                player_data["rounds_results"] = {}
                
            # 생존 카운트가 올바른지 확인하고 필요하면 재계산
            survived_rounds = sum(1 for round_num, survived in player_data.get("rounds_results", {}).items() if survived)
            player_data["survived_count"] = survived_rounds
            
        # 결과 텍스트 초기화 (새 라운드를 위해)
        rooms[code]["result"] = ""
        
        save_rooms(rooms)

# ✅ 결과 텍스트를 파싱하여 생존 여부 판단 및 기록
def update_survival_records(code, result_text):
    rooms = load_rooms()
    if code not in rooms:
        return
    
    # 현재 라운드 확인
    current_round = rooms[code].get("current_round", 1)
    
    # 플레이어 목록 가져오기
    players = list(rooms[code]["players"].keys())
    
    # 언어 확인
    is_english = "language" in st.session_state and st.session_state.language == "en"
    
    # GPT 오류 확인 - 오류인 경우 처리하지 않음
    if "[GPT 오류]" in result_text or "[GPT Error]" in result_text:
        return
    
    # 생존 여부 확인
    for player_name in players:
        # AI의 판정 결과 추출을 위한 패턴들
        if is_english:
            # 영어 버전 패턴
            survived_patterns = [
                r"[-\*•]\s*" + re.escape(player_name) + r".*?[Ss]urvived",
                r"Player\s+['\"]" + re.escape(player_name) + r"['\"].*?[Ss]urvived",
                r"" + re.escape(player_name) + r".*?[Ss]urvived",
                r".*?" + re.escape(player_name) + r".*?[Ss]urvived"
            ]
            died_patterns = [
                r"[-\*•]\s*" + re.escape(player_name) + r".*?[Dd]ied",
                r"Player\s+['\"]" + re.escape(player_name) + r"['\"].*?[Dd]ied",
                r"" + re.escape(player_name) + r".*?[Dd]ied",
                r".*?" + re.escape(player_name) + r".*?[Dd]ied"
            ]
            survived_keywords = ["survived", "made it", "alive", "lives", "success"]
            died_keywords = ["died", "dead", "death", "killed", "lost", "unfortunate"]
        else:
            # 한국어 버전 패턴
            survived_patterns = [
                r"[-\*•]\s*" + re.escape(player_name) + r".*?생존",
                r"플레이어\s+['\"]" + re.escape(player_name) + r"['\"].*?생존",
                r"" + re.escape(player_name) + r".*?생존",
                r".*?" + re.escape(player_name) + r".*?생존"
            ]
            died_patterns = [
                r"[-\*•]\s*" + re.escape(player_name) + r".*?사망",
                r"플레이어\s+['\"]" + re.escape(player_name) + r"['\"].*?사망",
                r"" + re.escape(player_name) + r".*?사망",
                r".*?" + re.escape(player_name) + r".*?사망"
            ]
            survived_keywords = ["생존", "살아남", "탈출", "성공"]
            died_keywords = ["사망", "죽음", "죽었", "패배", "실패"]
        
        # 플레이어 섹션 추출
        player_section = ""
        for line in result_text.split('\n'):
            if player_name in line:
                player_section = line
                # 다음 줄이 있다면 포함
                idx = result_text.find(line)
                next_section = result_text[idx:].split('\n\n')[0]
                if next_section:
                    player_section = next_section
                break
        
        # 1. 패턴 매칭으로 먼저 확인
        survived_match = False
        for pattern in survived_patterns:
            if re.search(pattern, result_text, re.IGNORECASE | re.DOTALL):
                survived_match = True
                break
        
        died_match = False
        for pattern in died_patterns:
            if re.search(pattern, result_text, re.IGNORECASE | re.DOTALL):
                died_match = True
                break
        
        # 2. 키워드 기반 분석
        if player_section:
            # 생존/사망 키워드 검사
            survived_found = any(keyword.lower() in player_section.lower() for keyword in survived_keywords)
            died_found = any(keyword.lower() in player_section.lower() for keyword in died_keywords)
        
        # 최종 판정
        survived = False
        
        # 패턴 매칭 우선
        if survived_match and not died_match:
            survived = True
        elif died_match and not survived_match:
            survived = False
        # 키워드 기반 판정
        elif player_section:
            if survived_found and not died_found:
                survived = True
            elif died_found and not survived_found:
                survived = False
            # 둘 다 없는 경우 텍스트 분석
            else:
                # 긍정적/부정적 단어 분석
                if is_english:
                    positive_words = ["success", "manage", "lucky", "fortunate", "clever", "smart", "escape", "avoid"]
                    negative_words = ["fail", "unlucky", "terrible", "tragic", "pain", "hurt", "suffer"]
                else:
                    positive_words = ["성공", "운이 좋", "똑똑", "탈출", "피했", "해결"]
                    negative_words = ["실패", "불운", "비극", "고통", "아픔", "상처"]
                    
                positive_count = sum(1 for word in positive_words if word.lower() in player_section.lower())
                negative_count = sum(1 for word in negative_words if word.lower() in player_section.lower())
                
                if positive_count > negative_count:
                    survived = True
        
        # 플레이어의 라운드별 결과 기록
        if "rounds_results" not in rooms[code]["players"][player_name]:
            rooms[code]["players"][player_name]["rounds_results"] = {}
        
        # 현재 라운드의 결과 기록 (라운드는 1부터 시작)
        rooms[code]["players"][player_name]["rounds_results"][str(current_round)] = survived
        
        # 생존 카운트 재계산 - 현재 라운드까지의 결과만 반영
        survived_count = 0
        for r in range(1, current_round + 1):
            if str(r) in rooms[code]["players"][player_name]["rounds_results"] and rooms[code]["players"][player_name]["rounds_results"][str(r)]:
                survived_count += 1
        
        rooms[code]["players"][player_name]["survived_count"] = survived_count
    
    save_rooms(rooms)

# ✅ 생존 횟수 조회
def get_survival_count(code, player_name):
    rooms = load_rooms()
    if code in rooms and player_name in rooms[code]["players"]:
        return rooms[code]["players"][player_name].get("survived_count", 0)
    return 0 
