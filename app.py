import streamlit as st
import numpy as np

# 페이지 기본 설정
st.set_page_config(page_title="Rule Based Board Games", layout="centered")

# --- 세션 상태 시스템 초기화 ---
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
    st.session_state.c_turn = "white"
if 'c_msg' not in st.session_state:
    st.session_state.c_msg = "움직일 말을 선택하세요 (백돌 차례)"

st.title("🧱 완벽 작동 규칙 보드게임방")

# 안전한 탭 레이아웃 사용
tab1, tab2 = st.tabs(["⚫ 초대형 오목 (15x15)", "👑 진짜 규칙 체스"])

# --- [1] 오목 파트 ---
with tab1:
    st.subheader("🪵 15x15 정식 격자선 오목")
    if st.session_state.o_winner:
        st.success(f"🎉 {st.session_state.o_winner}")
    else:
        st.info(f"현재 차례: {'⚫ 흑돌' if st.session_state.o_turn == 1 else '⚪ 백돌'}")

    # 15x15 오목 격자판 그리기
    for r in range(15):
        cols = st.columns(15)
        for c in range(15):
            val = st.session_state.o_board[r][c]
            # 격자선 느낌을 주기 위해 빈 칸은 ┼ 로 표시
            lbl = "⚫" if val == 1 else ("⚪" if val == 2 else "┼")
            
            with cols[c]:
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
                        
    if st.button("🔄 오목판 초기화"):
        st.session_state.o_board = np.zeros((15, 15))
        st.session_state.o_turn = 1
        st.session_state.o_winner = None
        st.rerun()

# --- [2] 체스 파트 ---
with tab2:
    st.subheader("🏁 체스 규칙 검증 모드")
    st.write(st.session_state.c_msg)

    # 파이썬 체스 규칙 검증 함수 (에러 완벽 수정)
    def check_chess_move(f_r, f_c, t_r, t_c, piece):
        if f_r == t_r and f_c == t_c: return False
        dr, dc = t_r - f_r, t_c - f_c
        abs_dr, abs_dc = abs(dr), abs(dc)
        
        target = st.session_state.c_board[t_r][t_c]
        white_pieces = ["♖", "♘", "♗", "♕", "♔", "♙"]
        black_pieces = ["♜", "♞", "♝", "♛", "♚", "♟"]
        
        if piece in white_pieces and target in white_pieces: return False
        if piece in black_pieces and target in black_pieces: return False
        
        p_type = piece
        # 1. 폰 규칙
        if p_type == "♙":
            if dc == 0 and dr == -1 and target == " ": return True
            if dc == 0 and dr == -2 and f_r == 6 and st.session_state.c_board[5][f_c] == " " and target == " ": return True
            if abs_dc == 1 and dr == -1 and target in black_pieces: return True
            return False
        if p_type == "♟":
            if dc == 0 and dr == 1 and target == " ": return True
            if dc == 0 and dr == 2 and f_r == 1 and st.session_state.c_board[2][f_c] == " " and target == " ": return True
            if abs_dc == 1 and dr == 1 and target in white_pieces: return True
            return False
            
        # 2. 룩 규칙
        if p_type in ["♖", "♜"]:
            if f_r != t_r and f_c != t_c: return False
            sr = 0 if dr == 0 else (1 if dr > 0 else -1)
            sc = 0 if dc == 0 else (1 if dc > 0 else -1)
            cr, cc = f_r + sr, f_c + sc
            while cr != t_r or cc != t_c:
                if st.session_state.c_board[cr][cc] != " ": return False
                cr += sr; cc += sc
            return True
            
        # 3. 비숍 규칙
        if p_type in ["♗", "♝"]:
            if abs_dr != abs_dc: return False
            sr = 1 if dr > 0 else -1
            sc = 1 if dc > 0 else -1
            cr, cc = f_r + sr, f_c + sc
            while cr != t_r:
                if st.session_state.c_board[cr][cc] != " ": return False
                cr += sr; cc += sc
            return True
            
        # 4. 나이트 규칙
        if p_type in ["♘", "♞"]:
            return (abs_dr == 2 and abs_dc == 1) or (abs_dr == 1 and abs_dc == 2)
            
        # 5. 퀸 규칙
        if p_type in ["♕", "♛"]:
            if abs_dr == abs_dc or f_r == t_r or f_c == t_c:
                sr = 0 if dr == 0 else (1 if dr > 0 else -1)
                sc = 0 if dc == 0 else (1 if dc > 0 else -1)
                cr, cc = f_r + sr, f_c + sc
                while cr != t_r or cc != t_c:
                    if st.session_state.c_board[cr][cc] != " ": return False
                    cr += sr; cc += sc
                return True
            return False
            
        # 6. 킹 규칙
        if p_type in ["♔", "♚"]:
            return abs_dr <= 1 and abs_dc <= 1
            
        return False

    # 8x8 체스판 그리기
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            piece = st.session_state.c_board[r][c]
            
            # 선택된 칸 표시
            if st.session_state.c_select == (r, c):
                button_label = f"📍{piece}" if piece != " " else "📍"
            else:
                button_label = piece if piece != " " else "  "
                
            with cols[c]:
                if st.button(button_label, key=f"c-{r}-{c}", use_container_width=True):
                    white_pieces = ["♖", "♘", "♗", "♕", "♔", "♙"]
                    black_pieces = ["♜", "♞", "♝", "♛", "♚", "♟"]
                    
                    if st.session_state.c_select is None:
                        if piece != " " and ((st.session_state.c_turn == "white" and piece in white_pieces) or (st.session_state.c_turn == "black" and piece in black_pieces)):
                            st.session_state.c_select = (r, c)
                            st.session_state.c_msg = f"선택된 말: {piece} ➡️ 어디로 이동할까요?"
                            st.rerun()
                    else:
                        fr, fc = st.session_state.c_select
                        src_p = st.session_state.c_board[fr][fc]
                        
                        if check_chess_move(fr, fc, r, c, src_p):
                            st.session_state.c_board[fr][fc] = " "
                            st.session_state.c_board[r][c] = src_p
                            st.session_state.c_turn = "black" if st.session_state.c_turn == "white" else "white"
                            st.session_state.c_msg = f"이동 완료! 다음 차례: {'백돌 ⚪' if st.session_state.c_turn == 'white' else '흑돌 ⚫'}"
                        else:
                            st.session_state.c_msg = "❌ 올바른 규칙의 행마가 아닙니다! 다시 하세요."
                        
                        st.session_state.c_select = None
                        st.rerun()

    if st.button("🔄 체스판 초기화"):
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
        st.session_state.c_select = None
        st.session_state.c_turn = "white"
        st.session_state.c_msg = "체스판이 초기화되었습니다. (백돌 차례)"
        st.rerun()
    
        
       

         
