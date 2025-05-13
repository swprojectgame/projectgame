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
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")
    
    st.title(get_text("slide3_title"))

    username = st.session_state.get("name", None)
    room_code = st.session_state.get("room_code", "DEFAULT")

    if "input_survive" not in st.session_state:
        st.session_state.input_survive = {}

    strategy = st.text_area(get_text("slide3_content"), height=150)

    if st.button(get_text("next_round")):
        if strategy:
            st.session_state.input_survive[username] = strategy
            st.session_state.page = "result"
            st.rerun()
        else:
            st.warning(get_text("error_occurred_restart"))
