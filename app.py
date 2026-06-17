import streamlit as st
import numpy as np

# 1. 페이지 설정 및 반응형 레이아웃
st.set_page_config(page_title="Cross-Grid Games", layout="centered")

# --- 에러 없이 완벽한 격자 그래픽을 구현하는 CSS와 스타일 ---
st.markdown("""
    <style>
    .stApp { background-color: #f5f6f8; }
    
    /* 실제 보드게임 판 테두리 */
    .game-outer-frame {
        background-color: #f1c40f;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.2);
        border: 4px solid #d4ac0d;
        width: fit-content;
        margin: 20px auto;
    }

    /* 오목 격자판 */
    .omok-board {
        display: grid;
        grid-template-columns: repeat(10, 45px);
        gap: 1px;
        background-color: #4a3728; /* 선 색깔 */
        border: 2px solid #4a3728;
    }

    /* 체스 격자판 */
    .chess-board {
        display: grid;
        grid-template-columns: repeat(8, 55px);
        gap: 0px;
        border: 3px solid #3d2f21;
    }

    /* 이미지 스타일 공통 */
    .cell-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
    }
    
    /* 스트림릿 버튼의 텍스트 테두리 지우고 빈 공간 채우기 */
    .stButton > button {
        width: 100% !important;
        height: 100% !important;
        border: none !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 4px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 오목 버튼 배경 */
    .omok-cell > button { background-color: #e8c39e !important; height: 45px !important; }
    .omok-cell > button:hover { background-color: #dbb38a !important; }

    /* 체스판 타일 배경 */
    .chess-dark > button { background-color: #b58863 !important; height: 55px !important; }
    .chess-light > button { background-color: #f0d9b5 !important; height: 55px !important; }
    .chess-dark > button:hover { background-color: #9c714c !important; }
    .chess-light > button:hover { background-color: #e1c7a1 !important; }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'game_choice' not in st.session_state:
    st.session_state.game_choice = "홈"

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.title("🏁 Cross-Grid")
    st.write("---")
    if st.button("🏠 홈으로 이동", use_container_width=True):
        st.session_state.game_choice = "홈"
        st.rerun()
    if st.button("⚫ 오목 (Omok)", use_container_width=True):
        st.session_state.game_choice = "오목"
        st.session_state.omok_board = np.zeros((10, 10))
        st.session_state.omok_turn = 1
        st.session_state.omok_winner = None
        st.rerun()
    if st.button("👑 체스 (Chess)", use_container_width=True):
        st.session_state.game_choice = "체스"
        # 위키미디어 고화질 체스 아이콘 주소
        img_base = "https://upload.wikimedia.org/wikipedia/commons"
        st.
