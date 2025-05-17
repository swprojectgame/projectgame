import streamlit as st
import time

# 페이지 전환용 세션 키 초기화
def init_page():
    if "page" not in st.session_state:
        st.session_state.page = "lobby"

# 페이지 이동 함수들
def go_to_lobby2():
    st.session_state.page = "lobby2"

def go_to_scenario():
    st.session_state.page = "scenario"

# 페이드 인 효과 (검정 배경이 서서히 나타남)
def fade_in_background():
    st.markdown("""
    <style>
    .fade-in-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background-color: black;
        opacity: 0;
        animation: fadeIn 1.5s ease-in forwards;
        z-index: 1000;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    <div class="fade-in-bg"></div>
    """, unsafe_allow_html=True)

# 텍스트 슬라이드 효과 포함 검정 배경

def fx1():
    st.markdown("""
        <style>
        .fx1-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: black;
            opacity: 0;
            animation: fadeInOut 6s ease-in-out forwards;
            z-index: 1000;
        }

        .fx1-slide-text {
            position: fixed;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 40px;
            opacity: 0;
            animation: slideDownPause 5s ease-in-out forwards;
            z-index: 1001;
        }

        @keyframes fadeInOut {
            0% { opacity: 0; }
            10% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; }
        }

        @keyframes slideDownPause {
            0% {
                transform: translate(-50%, -200px);
                opacity: 0;
            }
            20% {
                transform: translate(-50%, 150px);
                opacity: 1;
            }
            80% {
                transform: translate(-50%, 200px);
                opacity: 1;
            }
            100% {
                transform: translate(-50%, 500px);
                opacity: 0;
            }
        }
        </style>

        <div class="fx1-overlay"></div>
        <div class="fx1-slide-text">시나리오를 적어주세요!</div>
    """, unsafe_allow_html=True)

# 페이드 아웃 효과 (검정 배경이 서서히 사라짐)
def fade_out_background():
    st.markdown("""
        <style>
        .fade-out-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background-color: black;
            animation: fadeOut 1s forwards;
            z-index: 1000;
        }

        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        </style>

        <div class="fade-out-bg"></div>
    """, unsafe_allow_html=True)

# 각 페이지 동작 정의
def lobby_transition():
    st.title("🎮 Death by AI - Lobby")
    if st.button("다음"):
        fade_in_background()
        time.sleep(1.5)
        go_to_lobby2()
        st.rerun()

def lobby2_transition():
    fx1()
    time.sleep(4.8)
    go_to_scenario()
    st.rerun()

def scenario_transition():
    fade_out_background()
    st.title("📘 시나리오 페이지")
    st.write("이곳에 시나리오 내용을 넣으면 됩니다.")
