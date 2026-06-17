import streamlit as st
import numpy as np

# 1. 앱 설정 및 반응형 레이아웃
st.set_page_config(page_title="Cross-Grid Games", layout="centered")

# --- 눈이 편안한 CSS 디자인 스타일 적용 ---
st.markdown("""
    <style>
    /* 전체 버튼 공통 공백 제거 및 글자 크기 키우기 */
    .stButton > button {
        width: 100% !important;
        height: 45px !important;
        padding: 0px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        border: 1px solid #dcdcdc !important;
        transition: all 0.2s ease;
    }
    /* 버튼 위에 마우스 올렸을 때 반응 */
    .stButton > button:hover {
        transform: scale(1.05);
        border-color: #a0a0a0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'game_choice' not in st.session_state:
    st.session_state.game_choice = "홈"

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.title("🏁 Cross-Grid")
    st.caption("눈이 편안한 미니 보드게임")
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
        st.session_state.chess_board = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
        ]
        st.session_state.selected_piece = None
        st.rerun()

# --- [1] 홈 화면 ---
if st.session_state.game_choice == "홈":
    st.title("🧱 Cross-Grid 보드게임 카페")
    st.subheader("심플하고 정갈한 그래픽으로 즐기는 보드게임")
    st.write("왼쪽 사이드바에서 플레이할 게임을 선택해 주세요.")
    st.info("💡 격자무늬 테마에 맞춰 시각적 피로감을 줄이도록 디자인을 개선했습니다.")

# --- [2] 오목 게임 ---
elif st.session_state.game_choice == "오목":
    st.title("🪵 나무 바둑판 오목")
    
    def check_omok_win(r, c, piece):
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            for d in [1, -1]:
                nr, nc = r + dr*d, c + dc*d
                while 0 <= nr < 10 and 0 <= nc < 10 and st.session_state.omok_board[nr][nc] == piece:
                    count += 1
                    nr, nc = nr + dr*d, nc + dc*d
            if count >= 5: return True
        return False

    if st.session_state.omok_winner:
        st.balloons()
        st.success(f"🎊 {st.session_state.omok_winner} 승리!")
    else:
        st.info(f"현재 차례: {'⚫ 흑돌' if st.session_state.omok_turn == 1 else '⚪ 백돌'}")

    # 오목 전용 CSS 스타일 주입 (따뜻한 나무색 격자)
    st.markdown("""
        <style>
        .omok-btn > button {
            background-color: #E8C39E !important; /* 따뜻한 바둑판 색상 */
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 10x10 바둑판 생성
    for r in range(10):
        cols = st.columns(10)
        for c in range(10):
            val = st.session_state.omok_board[r][c]
            label = "⚫" if val == 1 else ("⚪" if val == 2 else " ")
            
            # 레이아웃 깨짐 방지를 위해 격자 컨테이너로 감싸기
            with cols[c]:
                st.markdown('<div class="omok-btn">', unsafe_allow_html=True)
                if st.button(label, key=f"o-{r}-{c}"):
                    if st.session_state.omok_board[r][c] == 0 and not st.session_state.omok_winner:
                        st.session_state.omok_board[r][c] = st.session_state.omok_turn
                        if check_omok_win(r, c, st.session_state.omok_turn):
                            st.session_state.omok_winner = "흑(Black)" if st.session_state.omok_turn == 1 else "백(White)"
                        else:
                            st.session_state.omok_turn = 3 - st.session_state.omok_turn
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# --- [3] 체스 게임 ---
elif st.session_state.game_choice == "체스":
    st.title("🏁 클래식 체크 체스판")
    
    if st.session_state.selected_piece:
        st.warning(f"선택된 말: {st.session_state.selected_piece['piece']} ➡️ 이동할 칸을 누르세요.")
    else:
        st.info("움직일 말을 마우스로 선택해 주세요.")

    # 체스판 전용 흑백 격자 스타일 주입
    st.markdown("""
        <style>
        .chess-dark > button { background-color: #B58863 !important; color: #FFFFFF !important; } /* 갈색 격자 */
        .chess-light > button { background-color: #F0D9B5 !important; color: #000000 !important; } /* 밝은 격자 */
        </style>
    """, unsafe_allow_html=True)

    # 8x8 체스판 생성
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            piece = st.session_state.chess_board[r][c]
            is_dark = (r + c) % 2 == 1
            style_class = "chess-dark" if is_dark else "chess-light"
            
            with cols[c]:
                st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
                if st.button(piece, key=f"c-{r}-{c}"):
                    # 말 선택
                    if st.session_state.selected_piece is None:
                        if piece != " ":
                            st.session_state.selected_piece = {"r": r, "c": c, "piece": piece}
                            st.rerun()
                    # 말 이동
                    else:
                        sr, sc = st.session_state.selected_piece['r'], st.session_state.selected_piece['c']
                        sp = st.session_state.selected_piece['piece']
                        
                        st.session_state.chess_board[sr][sc] = " "
                        st.session_state.chess_board[r][c] = sp
                        st.session_state.selected_piece = None
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 체스판 초기화", use_container_width=True):
        st.session_state.selected_piece = None
        st.rerun()
