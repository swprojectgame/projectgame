import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import check_all_submitted
from logic.room_manager import load_rooms
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

def a4():
    # 페이지 로드 시 불필요한 요소 숨기기
    hide_lobby_elements()
    
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")

    # 영어로 표시되도록 언어 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"

    # 🔐 필수 정보
    code = st.session_state.room_code
    name = st.session_state.player_name
    
    # 라운드 정보 확인
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)
    
    # 단계 관리
    if "phase" not in st.session_state:
        st.session_state.phase = "input"
    
    # 라운드 변경 감지
    if "last_round" not in st.session_state:
        st.session_state.last_round = 0
        
    # 라운드가 변경되면 phase 초기화
    if current_round != st.session_state.last_round:
        st.session_state.phase = "input"
        st.session_state.last_round = current_round

    # 판단 중인 경우
    if st.session_state.phase == "judging":
        st.markdown("<h1 style='text-align: center; color: white;'>" + get_text("judging") + "</h1>", unsafe_allow_html=True)
        time.sleep(3)
        st.session_state.phase = "finalizing"
        st.rerun()

    # 최종 판단 단계
    elif st.session_state.phase == "finalizing":
        st.markdown("<h1 style='text-align: center; color: white;'>" + get_text("finalizing") + "</h1>", unsafe_allow_html=True)
        time.sleep(3)
        st.session_state.page = "result"
        st.rerun()

    # 입력 단계
    elif st.session_state.phase == "input":
        st.title(get_text("title_prompt"))

        # 모든 플레이어 제출 상태 확인 (문제 방지를 위한 추가 확인)
        submitted = False
        if "players" in rooms[code] and name in rooms[code]["players"]:
            submitted = rooms[code]["players"][name].get("submitted", False)
        
        # 자신이 제출하지 않았는데 다른 화면으로 이동한 경우 수정
        if not submitted and st.session_state.page == "prompt":
            st.info(get_text("waiting"))
            time.sleep(2)
            st.session_state.page = "scenario"
            st.rerun()

        # ✅ 모든 플레이어가 제출했는지 확인
        if check_all_submitted(code):
            st.session_state.phase = "judging"
            st.rerun()
        else:
            time.sleep(2)  # 2초 대기 후 새로고침
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
