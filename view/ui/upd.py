import streamlit as st
import streamlit.components.v1 as components

def fx1():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: transparent;
        }

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
        <div class="fx1-slide-text">시나리오가 오고 있습니다!</div>
    """, unsafe_allow_html=True)

    # JS로 페이지 이동 유도 (6초 후 rerun 유도)
    components.html("""
        <script>
        setTimeout(() => {
            fetch('/_stcore/stream', {
                method: 'POST'
            }).then(() => {
                window.location.reload();
            });
        }, 6000);  // fx1 애니메이션 길이만큼 기다리기
        </script>
    """, height=0)
