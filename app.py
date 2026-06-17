import streamlit as st
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="Rule Based Board Games", layout="centered")

# --- 화면이 칼같이 정렬되고 정갈하게 나오는 CSS 스타일 ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* 외곽 프레임 상자 */
    .board-container {
        border: 4px solid #b58863;
        background-color: #f7e1c6;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.15);
        width: fit-content;
        margin: 20px auto;
    }
    
    /* 오목판 교차선 위에 돌을 올리기 위한 버튼 스타일 설정 */
    .omok-box button {
        width: 34px !important;
        height: 34px !important;
        padding: 0px !important;
        margin: 0px !important;
        font-size: 22px !important;
        border: none !important;
        background: transparent !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative;
    }
    
    /* 바둑판 격자선 배경 (CSS로 십자가 구현) */
    .omok-box {
        width: 34px; height: 34px;
        display: flex; align-items: center; justify-content: center;
        background-image: 
            linear-gradient(to right, transparent 49%, #4a3411 49%, #4a3411 51%, transparent 51%),
            linear-gradient(to bottom, transparent 49%, #4a3411 49%, #4a3411 51%, transparent 51%);
        background-color: #e8c39e;
    }

    /* 체스판 타일 스타일 */
    .chess-tile button {
        width: 52px !important;
        height: 52px !important;
        padding: 0px !important;
        margin: 0px !important;
        font-size: 32px !important;
        border: 1px solid #3d2f21 !important;
        border-radius: 0px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* 레이아웃 틈새 싹 제거 */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 세션 상태 시스템 초기화 ---
if 'board_game' not in st.session_state:
    st.session_state.board_game = "오목"
if 'o_board' not in st.session_state:
    st.session_state.o_board = np.zeros((15, 15))
if 'o_turn' not in st.session_state:
    st.session_state.o_turn = 1 # 1: 흑, 2: 백
if 'o_winner' not in st.session_state:
    st.session_state.o_winner = None

if 'c_board' not in st.session_state:
    st.session_state.c_board = [
        ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
        ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
        ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
    ]
if 'c_select' not in st.session_state:
    st.session_state.c_select = None
if 'c_turn' not in st.session_state:
    st.session_state.c_turn = "white" # white, black
if 'c_msg' not in st.session_state:
    st.session_state.c_msg = "움직일 말을 선택하세요 (백돌 차례)"

# 상단 메뉴 구성
st.title("🧱 완벽 작동 규칙 보드게임방")
menu = st.radio("게임 선택", ["⚫ 초대형 오목 (15x15)", "👑 진짜 규칙 체스"], horizontal=True)

# --- [1] 오목 파트 ---
if "오목" in menu:
    st.subheader("🪵 15x15 정식 격자선 오목")
    if st.session_state.o_winner:
        st.success(f"🎉 {st.session_state.o_winner}")
    else:
        st.info(f"현재 차례: {'⚫ 흑돌' if st.session_state.o_turn == 1 else '⚪ 백돌'}")

    st.markdown('<div class="board-container">', unsafe_allow_html=True)
    
    # 15x15 오목 격자판 그리기
    for r in range(15):
        cols = st.columns(15)
        for c in range(15):
            val = st.session_state.o_board[r][c]
            lbl = "⚫" if val == 1 else ("⚪" if val == 2 else " ")
            
            with cols[c]:
                st.markdown('<div class="omok-box">', unsafe_allow_html=True)
                if st.button(lbl, key=f"o-{r}-{c}", use_container_width=True):
                    if val == 0 and not st.session_state.o_winner:
                        st.session_state.o_board[r][c] = st.session_state.o_turn
                        
                        # 5목 승리 판정 알고리즘
                        dirs = [(0,1), (1,0), (1,1), (1,-1)]
                        win = False
                        for dr, dc in dirs:
                            cnt = 1
                            for d in [1, -1]:
                                nr, nc = r + dr*d, c + dc*d
                                while 0 <= nr < 15 and 0 <= nc < 15 and st.session_state.o_board[nr][nc] == st.session_state.o_turn:
                                    cnt += 1
                                    nr, nc = nr + dr*d, nc + dc*d
                            if cnt >= 5: win = True
                        
                        if win:
                            st.session_state.o_winner = f"{'흑돌(Black)' if st.session_state.o_turn == 1 else '백돌(White)'} 승리!!!"
                        else:
                            st.session_state.o_turn = 3 - st.session_state.o_turn
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 오목판 초기화"):
        st.session_state.o_board = np.zeros((15, 15))
        st.session_state.o_turn = 1
        st.session_state.o_winner = None
        st.rerun()

# --- [2] 체스 파트 (진짜 규칙 검증 엔진) ---
else:
    st.subheader("🏁 체스 규칙 검증 모드")
    st.write(st.session_state.c_msg)

    # 파이썬 체스 규칙 검증 함수
    def check_chess_move(f_r, f_c, t_r, t_c, piece):
        if f_r == t_r and f_c == t_c: return False
        dr, dc = t_r - f_r, t_c - f_c
        abs_dr, abs_dc = abs(dr), abs(dc)
        
        target = st.session_state.c_board[t_r][t_c]
        white_pieces = ["♖", "♘", "♗", "♕", "♔", "♙"]
        black_pieces = ["♜", "♞", "♝", "♛", "♚", "♟"]
        
        # 아군 공격 금지
        if piece in white_pieces and target in white_pieces: return False
        if piece in black_pieces and target in black_pieces: return False
        
        p_type = piece
        # 1. 폰(Pawn) 규칙
        if p_type == "♙": # 백색 폰
            if dc == 0 and dr == -1 and target == " ": return True
            if dc == 0 Arab and dr == -2 and f_r == 6 and st.session_state.c_board[5][f_c] == " " and target == " ": return True
            if abs_dc == 1 and dr == -1 and target in black_pieces: return True
            return False
        if p_type == "♟": # 흑색 폰
            if dc == 0 and dr == 1 and target == " ": return True
            if dc == 0 and dr == 2 and f_r == 1 and st.session_state.c_board[2][f_c] == " " and target == " ": return True
            if abs_dc == 1 and dr == 1 and target in white_pieces: return True
            return False
            
        # 2. 룩(Rook) 규칙
        if p_type in ["♖", "♜"]:
            if f_r != t_r and f_c != t_c: return False
            sr = 0 if dr == 0 else (1 if dr > 0 else -1)
            sc = 0 if dc == 0 else (1 if dc >
