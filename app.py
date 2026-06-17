import streamlit as st
import numpy as np

# 1. 앱 기본 설정
st.set_page_config(page_title="은재의 보드게임 카페", layout="centered")

# 세션 상태 초기화 (게임 선택 및 데이터 저장용)
if 'game_choice' not in st.session_state:
    st.session_state.game_choice = "홈"

# --- 사이드바: 게임 메뉴 선택 ---
with st.sidebar:
    st.title("🎮 게임 메뉴")
    st.write("하고 싶은 게임을 골라보세요!")
    
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.game_choice = "홈"
        st.rerun()
    if st.button("⚫ 오목 (Omok)", use_container_width=True):
        st.session_state.game_choice = "오목"
        # 오목 데이터 초기화
        st.session_state.omok_board = np.zeros((10, 10))
        st.session_state.omok_turn = 1
        st.session_state.omok_winner = None
        st.rerun()
    if st.button("👑 체스 (Chess)", use_container_width=True):
        st.session_state.game_choice = "체스"
        # 체스 데이터 초기화 (간단한 8x8 말 배치)
        # 1: 폰, 2: 룩, 3: 나이트, 4: 비숍, 5: 퀸, 6: 킹 (양수는 백, 음수는 흑)
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

# --- 메인 화면: 선택한 게임 보여주기 ---

# [1] 홈 화면
if st.session_state.game_choice == "홈":
    st.title("✨ 은재의 미니 보드게임 카페 ✨")
    st.subheader("왼쪽 메뉴에서 게임을 선택해 주세요!")
    st.write("친구와 한 컴퓨터에서 번갈아 가며 둘 수 있는 2인용 게임 전용 공간입니다.")
    st.info("💡 팁: 오목은 10x10 격자로, 체스는 기본적인 말 움직임을 시각화해서 즐길 수 있어요!")

# [2] 오목 게임 영역
elif st.session_state.game_choice == "오목":
    st.title("⚫ 미니 오목 게임 ⚪")
    
    # 승리 판정 함수
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
        st.success(f"🎊 {st.session_state.omok_winner} 승리! 🎊")
    else:
        st.info(f"현재 턴: {'⚫ 흑' if st.session_state.omok_turn == 1 else '⚪ 백'}")

    # 10x10 바둑판 그리기
    for r in range(10):
        cols = st.columns(10)
        for c in range(10):
            val = st.session_state.omok_board[r][c]
            label = "●" if val == 1 else ("○" if val == 2 else " ")
            
            if cols[c].button(label, key=f"o-{r}-{c}"):
                if st.session_state.omok_board[r][c] == 0 and not st.session_state.omok_winner:
                    st.session_state.omok_board[r][c] = st.session_state.omok_turn
                    if check_omok_win(r, c, st.session_state.omok_turn):
                        st.session_state.omok_winner = "흑(Black)" if st.session_state.omok_turn == 1 else "백(White)"
                    else:
                        st.session_state.omok_turn = 3 - st.session_state.omok_turn
                    st.rerun()

# [3] 체스 게임 영역
elif st.session_state.game_choice == "체스":
    st.title("👑 미니 자유 체스판 ♟️")
    st.caption("※ 이 체스판은 룰 제한 없이 말을 자유롭게 옮길 수 있는 연습용 보드입니다.")
    
    if st.session_state.selected_piece:
        st.warning(f"선택된 말: {st.session_state.selected_piece['piece']} (위치: {st.session_state.selected_piece['r']}행 {st.session_state.selected_piece['c']}열) -> 이동할 칸을 누르세요.")
    else:
        st.info("움직일 말을 먼저 마우스로 클릭하세요!")

    # 8x8 체스판 그리기
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            piece = st.session_state.chess_board[r][c]
            # 체스판 체크무늬 배경 흉내내기
            bg = "🟫" if (r+c)%2 == 0 else "⬜"
            label = piece if piece != " " else bg
            
            if cols[c].button(label, key=f"c-{r}-{c}"):
                # 말을 처음 선택할 때
                if st.session_state.selected_piece is None:
                    if piece != " ":
                        st.session_state.selected_piece = {"r": r, "c": c, "piece": piece}
                        st.rerun()
                # 이미 말을 선택한 상태에서 다른 칸을 눌러 이동할 때
                else:
                    sr, sc = st.session_state.selected_piece['r'], st.session_state.selected_piece['c']
                    sp = st.session_state.selected_piece['piece']
                    
                    # 원래 위치 비우고 새 위치로 말 이동
                    st.session_state.chess_board[sr][sc] = " "
                    st.session_state.chess_board[r][c] = sp
                    st.session_state.selected_piece = None
                    st.rerun()

    if st.button("🔄 체스판 초기화"):
        st.session_state.selected_piece = None
        st.rerun()
