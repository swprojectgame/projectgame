import streamlit as st
import time
import os
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import submit_scenario
from logic.room_manager import load_rooms, assign_random_situation_to_all, get_current_round_situation, save_rooms
from logic.utils import get_random_situation, SITUATIONS
from view.language import get_text

TIME_LIMIT = 45  # 제한 시간 (초)
MAX_LENGTH = 140  # 최대 글자 수 제한

# 불필요한 UI 요소 숨기기 함수
def hide_lobby_elements():
    # 특별한 클래스를 가진 모든 컨테이너를 찾아서 제거하는 JS 코드
    hide_js = """
    <script>
    function hideElements() {
        // 게임 시작 버튼을 직접 타겟팅
        document.querySelectorAll('button').forEach(btn => {
            if (btn.innerText.includes('게임 시작') || btn.innerText.includes('🚀')) {
                // 버튼 자체 숨기기
                btn.style.display = 'none';
                btn.style.visibility = 'hidden';
                
                // 부모 요소들 모두 숨기기 (3단계 상위까지)
                let parent = btn.parentElement;
                for (let i = 0; i < 5; i++) {
                    if (parent) {
                        parent.style.display = 'none';
                        parent = parent.parentElement;
                    }
                }
            }
        });
        
        // 라운드 설정 관련 요소 숨기기
        document.querySelectorAll('.stNumberInput, input[type="number"]').forEach(el => {
            el.style.display = 'none';
            let container = el.closest('.element-container');
            if (container) container.style.display = 'none';
            
            // 부모 요소들도 확인
            let parent = el.parentElement;
            for (let i = 0; i < 3; i++) {
                if (parent) {
                    parent.style.display = 'none';
                    parent = parent.parentElement;
                }
            }
        });
        
        // 모든 요소 검사해서 특정 텍스트 포함된 요소와 컨테이너 제거
        const textsToHide = ['게임 시작', '게임 방법', '라운드 수', '진행할 라운드', '🚀'];
        document.querySelectorAll('*').forEach(el => {
            if (el.innerText) {
                for (const text of textsToHide) {
                    if (el.innerText.includes(text)) {
                        el.style.display = 'none';
                        
                        // 부모 요소들도 숨기기
                        let parent = el.parentElement;
                        for (let i = 0; i < 3; i++) {
                            if (parent) {
                                parent.style.display = 'none';
                                parent = parent.parentElement;
                            }
                        }
                        break;
                    }
                }
            }
        });
    }
    
    // 즉시 실행 함수로 등록
    (function() {
        // 페이지 로드 시 실행
        if (document.readyState === "loading") {
            document.addEventListener('DOMContentLoaded', hideElements);
        } else {
            hideElements();
        }
        
        // 0.5초 간격으로 10초간 반복 실행 (동적으로 로드되는 요소 처리)
        let count = 0;
        const interval = setInterval(() => {
            hideElements();
            count++;
            if (count > 20) clearInterval(interval);
        }, 500);
        
        // Mutation Observer로 DOM 변경 감지
        const observer = new MutationObserver(hideElements);
        observer.observe(document.body, { 
            childList: true, 
            subtree: true,
            attributes: true
        });
    })();
    </script>
    
    <style>
    /* 게임 시작 버튼 및 관련 요소 완전 제거 */
    button:has(span:contains("게임 시작")),
    button:has(span:contains("🚀")),
    div:has(> button:contains("게임 시작")),
    div:has(> button:contains("🚀")),
    div.element-container:has(button:contains("게임 시작")),
    div.element-container:has(button:contains("🚀")),
    [data-testid="stHorizontalBlock"]:has(button:contains("게임 시작")),
    [data-testid="stHorizontalBlock"]:has(button:contains("🚀")),
    .stButton:has(button:contains("게임 시작")),
    .stButton:has(button:contains("🚀")) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        pointer-events: none !important;
        z-index: -9999 !important;
        overflow: hidden !important;
        clip: rect(0, 0, 0, 0) !important;
    }
    
    /* 모든 버튼 스타일에 적용될 수 있는 보다 일반적인 선택자 */
    [role="button"]:has(> span:contains("게임 시작")),
    [role="button"]:has(> span:contains("🚀")),
    [type="button"]:has(> span:contains("게임 시작")),
    [type="button"]:has(> span:contains("🚀")) {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """
    st.markdown(hide_js, unsafe_allow_html=True)
    
    # 추가 CSS 직접 주입 - 모든 버튼을 숨기지 않고 특정 버튼만 숨기도록 수정
    additional_css = """
    <style>
    /* 특정 버튼만 숨기기 - 제출 버튼은 유지하도록 선택자 범위 제한 */
    button:contains("게임 시작"), 
    button:contains("🚀"), 
    button:contains("게임 방법"),
    .stButton:has(button:contains("게임 시작")),
    .stButton:has(button:contains("🚀")),
    .stButton:has(button:contains("게임 방법")),
    [role="button"]:has(span:contains("게임 시작")),
    [role="button"]:has(span:contains("🚀")),
    [type="button"]:has(span:contains("게임 시작")),
    [type="button"]:has(span:contains("🚀")) {
        opacity: 0 !important;
        visibility: hidden !important;
        display: none !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
    }
    
    /* React로 동적 생성되는 특정 요소만 숨김 */
    div[data-baseweb="button"]:has(span:contains("게임 시작")),
    div[data-baseweb="button"]:has(span:contains("🚀")),
    div[data-testid="stHorizontalBlock"]:has(button:contains("게임 시작")),
    div[data-testid="stHorizontalBlock"]:has(button:contains("🚀")) {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """
    st.markdown(additional_css, unsafe_allow_html=True)

def a3():
    # 페이지 로드 시 불필요한 요소 숨기기
    hide_lobby_elements()
    
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")

    # 🔐 필수 세션 정보
    code = st.session_state.room_code
    name = st.session_state.player_name
    
    # 현재 상황 및 라운드 정보 로드
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)
    
    # 이전 라운드 추적
    if "last_game_round" not in st.session_state:
        st.session_state.last_game_round = 0
    
    # 라운드가 변경되었는지 확인
    round_changed = current_round != st.session_state.last_game_round
    if round_changed:
        st.session_state.last_game_round = current_round
    
    # 현재 라운드의 상황 가져오기
    current_round_situation = get_current_round_situation(code)
    
    # 첫 게임 시작 시 또는 현재 라운드에 할당된 상황이 없는 경우 무작위 상황 할당
    if not current_round_situation or (round_changed and current_round > 1):
        # 무작위 상황 할당 시도
        assign_success = assign_random_situation_to_all(code)
        if assign_success:
            # 최신 정보로 rooms 갱신
            rooms = load_rooms()
            # 다시 현재 라운드 상황 가져오기
            current_round_situation = get_current_round_situation(code)
            
            # 할당된 상황이 비어있으면 더 강력하게 재시도
            if not current_round_situation:
                for _ in range(2):  # 최대 2번 더 시도
                    assign_random_situation_to_all(code)
                    rooms = load_rooms()
                    current_round_situation = get_current_round_situation(code)
                    if current_round_situation:
                        break
    
    # 현재 플레이어의 상황 확인
    player_situation = ""
    if "players" in rooms[code] and name in rooms[code]["players"]:
        player_situation = rooms[code]["players"][name].get("situation", "")
    
    # 플레이어 상황이 현재 라운드 상황과 다르면 업데이트
    if player_situation != current_round_situation and current_round_situation:
        rooms[code]["players"][name]["situation"] = current_round_situation
        save_rooms(rooms)
        player_situation = current_round_situation
    
    # 새 라운드 감지 및 입력값 초기화 로직
    if "last_situation" not in st.session_state:
        st.session_state.last_situation = ""
    
    if "last_round" not in st.session_state:
        st.session_state.last_round = 0
    
    # 상황이 변경되거나 라운드가 변경되면 입력값 초기화
    if (player_situation != st.session_state.last_situation or 
        current_round != st.session_state.last_round):
        
        # 입력값 완전 초기화
        if "user_input" in st.session_state:
            del st.session_state.user_input
        if "start_time" in st.session_state:
            del st.session_state.start_time
        
        # 현재 상황과 라운드 기록
        st.session_state.last_situation = player_situation
        st.session_state.last_round = current_round
    
    # 상태 초기화
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # 시간 계산
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TIME_LIMIT - elapsed)

    # 깜빡임 스타일 정의
    st.markdown("""
    <style>
    @keyframes blink {
        0% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    .blinking-bar {
        animation: blink 1s infinite alternate;
    }
    </style>
    """, unsafe_allow_html=True)

    # 영어로 표시되도록 언어 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"

    st.title(get_text("title_scenario"))
    
    # 라운드 표시
    st.subheader(f"Round {current_round}")

    # 타이머 바 표시
    percent = int((remaining / TIME_LIMIT) * 100)
    blink_class = "blinking-bar" if remaining < 10 else ""
    bar_html = f"""
    <div style="background-color:#eee; border-radius:10px; height:20px; width:100%; margin-bottom: 20px;">
        <div class="{blink_class}" style="
            width:{percent}% ;
            background-color:#ff4d4d;
            height:100%;
            border-radius:10px;
            transition: width 1s linear;
        "></div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)
    
    # 타이머 숫자 표시
    st.markdown(f"<h1 style='text-align: center; font-size: 72px; color: black;'>{remaining}</h1>", unsafe_allow_html=True)

    # ✅ 현재 플레이어의 상황 표시
    st.markdown(get_text("current_situation", situation=player_situation))

    # ✅ 사용자 행동 입력 - key를 고유하게 만들어 캐시 이슈 방지
    input_key = f"input_{current_round}_{name}"
    user_input = st.text_area(get_text("action_input"), key=input_key, value=st.session_state.user_input, max_chars=MAX_LENGTH)
    st.session_state.user_input = user_input  # 입력값 업데이트
    
    char_count = len(user_input)
    st.markdown(
        f"<div style='text-align: right; font-size: 14px; color: #888;'>{char_count} / {MAX_LENGTH}자</div>",
        unsafe_allow_html=True
    )

    # ✅ 제출 버튼 클릭 시 행동 저장 및 다음 페이지 이동
    if st.button(get_text("submit")):
        if user_input.strip():
            submit_scenario(code, name, user_input.strip())
            st.session_state.page = "prompt"  # 대기 화면으로 전환
            st.rerun()

    # 시간 종료 처리
    if remaining == 0 and not user_input.strip():
        st.session_state.page = "result"
        st.rerun()

    # CSS로 시작 화면과 라운드 관련 UI 요소 숨기기
    st.markdown("""
    <style>
    /* 시작 화면 숨기기 */
    .stApp header {
        display: none !important;
    }
    
    /* 로비 UI 요소 전체 숨기기 - 더 강력한 선택자 사용 */
    div[data-testid="stExpander"], 
    div.stNumberInput, 
    button:contains("게임 방법"), 
    button:contains("게임 시작"),
    button:contains("방 만들기"),
    button:contains("입장하기"),
    button:contains("방법"),
    button:contains("시작"),
    [data-testid="stHorizontalBlock"] button,
    [data-testid="baseButton-secondary"],
    div:has(> p:contains("진행할 라운드")),
    div:has(> p:contains("라운드 수")),
    div:has(> label:contains("라운드")),
    div:has(> button:contains("게임")),
    div:has(> button:contains("방법")),
    input[type="number"],
    div:has(input[type="number"]),
    div:has(button:contains("게임 시작")),
    div:has(button:contains("🚀")),
    [data-testid="stVerticalBlock"]:has(div.stNumberInput),
    footer {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        position: absolute !important;
        z-index: -9999 !important;
        pointer-events: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        max-height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 특정 컨테이너 요소에 대해 더 강력한 숨김 처리 */
    div:has(> div:has(> button:contains("게임 시작"))),
    div:has(> div:has(> button:contains("게임 방법"))),
    div:has(> p:contains("참가자")),
    div:has(> h3:contains("방 코드")),
    div:has(> div.stSlider),
    div.row-widget.stNumberInput,
    div.element-container:has(div.stNumberInput) {
        display: none !important;
        visibility: hidden !important;
        max-height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 슬라이드쇼 관련 요소 숨기기 */
    div.element-container:has(div.slide-container),
    div:has(> div:contains("슬라이드")) {
        display: none !important;
    }
    
    /* 추가적인 숨김 처리 - UI 영역 전체 숨김 */
    div.element-container:has(p:contains("진행할 라운드")),
    div.element-container:has(button:contains("게임 시작")),
    div.element-container:has(button:contains("🚀")),
    div.element-container:has(div.stNumberInput) {
        display: none !important;
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }
    </style>
    
    <script>
    // 자바스크립트로 추가 제거
    window.addEventListener('DOMContentLoaded', (event) => {
        setTimeout(() => {
            // 게임 시작 버튼 및 라운드 선택 요소 제거
            const removeElements = () => {
                // 텍스트 내용으로 요소 찾기
                document.querySelectorAll('p, button, div, label').forEach(el => {
                    if (el.innerText && (
                        el.innerText.includes('게임 시작') || 
                        el.innerText.includes('라운드 수') ||
                        el.innerText.includes('진행할 라운드') ||
                        el.innerText.includes('🚀')
                    )) {
                        const parent = el.closest('.element-container') || el.parentElement;
                        if (parent) parent.style.display = 'none';
                    }
                });
                
                // 숫자 입력 필드 제거
                document.querySelectorAll('input[type="number"]').forEach(el => {
                    const container = el.closest('.row-widget.stNumberInput');
                    if (container) {
                        const parent = container.closest('.element-container');
                        if (parent) parent.style.display = 'none';
                    }
                });
            };
            
            // 즉시 실행 및 500ms 간격으로 재실행 (동적 로딩 요소 처리)
            removeElements();
            setInterval(removeElements, 500);
        }, 100);
    });
    </script>
    """, unsafe_allow_html=True)

    # 1초마다 화면 갱신
    if remaining > 0:
        time.sleep(1)
        st.rerun()
