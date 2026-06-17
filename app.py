import streamlit as st
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="Classic Grid Games", layout="centered")

# --- 게임판을 실제 사진처럼 만들어주는 세련된 CSS 스타일 ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    
    /* 보드판 외곽 프레임 (노란색 나무 테두리 느낌) */
    .game-frame {
        background-color: #f1c40f;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.2);
        border: 4px solid #d4ac0d;
        width: fit-content;
        margin: 20px auto;
    }

    /* 오목판 격자 */
    .omok-board {
        display: grid;
        grid-template-columns: repeat(10, 45px);
        grid-template-rows: repeat(10, 45px);
        gap: 1px;
        background-color: #4a3728; /* 선 색상 */
        border: 2px solid #4a3728;
    }

    /* 오목 칸 (기본 나무 배경) */
    .omok-cell button {
        width: 45px !important;
        height: 45px !important;
        background-color: #e8c39e !important;
        border: none !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .omok-cell button:hover { background-color: #dbb38a !important; }

    /* 체스판 격자 */
    .chess-board {
        display: grid;
        grid-template-columns: repeat(8, 55px);
        grid-template-rows: repeat(8, 55px);
        gap: 0px;
        border: 3px solid #3d2f21;
    }

    /* 체스 칸 공통 */
    .chess-cell button {
        width: 55px !important;
        height: 55px !important;
        border: none !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 4px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 체스판 체크무늬 색상 */
    .chess-dark button { background-color: #b58863 !important; }
    .chess-light button { background-color: #f0d9b5 !important; }
    .chess-dark button:hover { background-color: #9c714c !important; }
    .chess-light button:hover { background-color: #e1c7a1 !important; }

    /* 이미지 크기 알맞게 조절 */
    .game-img {
        width: 90%;
        height: 90%;
        object-fit: contain;
        pointer-events: none; /* 클릭 방해 금지 */
    }
    
    /* 스트림릿 기본 여백 완전 제거 */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'game_choice' not in st.session_state:
    st.session_state.game_choice = "홈"

# --- 사이드바 내비게이션 ---
with st.sidebar:
    st.title("🏁 Grid Board")
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
        # 체스 말 이미지 URL 매핑 데이터 세팅
        # b=black, w=white / r=rook, n=knight, b=bishop, q=queen, k=king, p=pawn
        img_base = "https://upload.wikimedia.org/wikipedia/commons"
        st.session_state.chess_imgs = {
            "♜": f"{img_base}/a/a0/Chess_rdt45.svg", "♞": f"{img_base}/e/ef/Chess_ndt45.svg",
            "♝": f"{img_base}/9/9b/Chess_bdt45.svg", "♛": f"{img_base}/4/47/Chess_qdt45.svg",
            "♚": f"{img_base}/f/f0/Chess_kdt45.svg", "♟": f"{img_base}/c/c7/Chess_pdt45.svg",
            "♖": f"{img_base}/7/72/Chess_rlt45.svg", "♘": f"{img_base}/7/70/Chess_nlt45.svg",
            "♗": f"{img_base}/b/b1/Chess_blt45.svg", "♕": f"{img_base}/1/15/Chess_qlt45.svg",
            "♔": f"{img_base}/4/42/Chess_klt45.svg", "♙": f"{img_base}/4/45/Chess_plt45.svg"
        }
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

# --- 화면 출력부 ---
if st.session_state.game_choice == "홈":
    st.title("🧱 클래식 그래픽 게임방")
    st.write("보내주신 고품질 그래픽 디자인 레이아웃이 적용되었습니다!")
    st.info("왼쪽 메뉴에서 오목판과 체스판을 골라 실제 게임처럼 즐겨보세요.")

elif st.session_state.game_choice == "오목":
    st.title("🪵 정밀 오목 보드")
    if st.session_state.omok_winner:
        st.balloons()
        st.success(f"🎊 {st.session_state.omok_winner} 승리!")
    else:
        st.info(f"현재 차례: {'⚫ 흑돌' if st.session_state.omok_turn == 1 else '⚪ 백돌'}")

    # 바둑판 렌더링
    st.markdown('<div class="game-frame"><div class="omok-board">', unsafe_allow_html=True)
    for r in range(10):
        for c in range(10):
            val = st.session_state.omok_board[r][c]
            
            # 돌 상태에 따른 이미지 태그 생성
            img_html = " "
            if val == 1:
                img_html = '<img src="https://upload.wikimedia.org/wikipedia/commons/2/20/Go_b_00.svg" class="game-img">'
            elif val == 2:
                img_html = '<img src="https://upload.wikimedia.org/wikipedia/commons/d/d7/Go_w_00.svg" class="game-img">'
                
            st.markdown('<div class="omok-cell">', unsafe_allow_html=True)
            if st.button(img_html, key=f"o-{r}-{c}"):
                if st.session_state.omok_board[r][c] == 0 and not st.session_state.omok_winner:
                    st.session_state.omok_board[r][c] = st.session_state.omok_turn
                    # 5목 체크 로직
                    directions = [(0,1), (1,0), (1,1), (1,-1)]
                    win = False
                    for dr, dc in directions:
                        count = 1
                        for d in [1, -1]:
                            nr, nc = r + dr*d, c + dc*d
                            while 0 <= nr < 10 and 0 <= nc < 10 and st.session_state.omok_board[nr][nc] == st.session_state.omok_turn:
                                count += 1
                                nr, nc = nr + dr*d, nc + dc*d
                        if count >= 5: win = True
                    
                    if win:
                        st.session_state.omok_winner = "흑(Black)" if st.session_state.omok_turn == 1 else "백(White)"
                    else:
                        st.session_state.omok_turn = 3 - st.session_state.omok_turn
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

elif st.session_state.game_choice == "체스":
    st.title("🏁 클래식 그래픽 체스")
    if st.session_state.selected_piece:
        st.warning(f"말 선택됨 ➡️ 이동할 칸을 누르세요.")
    else:
        st.info("움직일 말을 마우스로 터치/클릭하세요.")

    # 체스판 렌더링
    st.markdown('<div class="game-frame"><div class="chess-board">', unsafe_allow_html=True)
    for r in range(8):
        for c in range(8):
            piece = st.session_state.chess_board[r][c]
            is_dark = (r + c) % 2 == 1
            style_class = "chess-dark" if is_dark else "chess-light"
            
            # 말 캐릭터 이미지 태그 매핑
            img_html = " "
            if piece in st.session_state.chess_imgs:
                img_html = f'<img src="{st.session_state.chess_imgs[piece]}" class="game-img">'
                
            st.markdown(f'<div class="chess-cell {style_class}">', unsafe_allow_html=True)
            if st.button(img_html, key=f"c-{r}-{c}"):
                if st.session_state.selected_piece is None:
                    if piece != " ":
                        st.session_state.selected_piece = {"r": r, "c": c, "piece": piece}
                        st.rerun()
                else:
                    sr, sc = st.session_state.selected_piece['r'], st.session_state.selected_piece['c']
                    sp = st.session_state.selected_piece['piece']
                    
                    st.session_state.chess_board[sr][sc] = " "
                    st.session_state.chess_board[r][c] = sp
                    st.session_state.selected_piece = None
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    if st.button("🔄 체스판 초기화", use_container_width=True):
        st.session_state.selected_piece = None
        st.rerun()
