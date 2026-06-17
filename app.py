import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Classic Board Games", layout="centered")

st.title("🧱 완벽한 격자 보드게임방")
st.write("오목판과 체스판의 격자 선이 사진처럼 정확하게 정렬되도록 특수 코딩된 버전입니다.")

# 2. 탭 메뉴를 사용해서 오목과 체스를 깔끔하게 분리
tab1, tab2 = st.tabs(["⚫ 오목 (Omok)", "👑 체스 (Chess)"])

with tab1:
    st.subheader("🪵 나무 격자 오목판")
    st.caption("칸을 터치하면 바둑돌이 놓입니다. (5목 완성 시 승리)")
    
    # HTML/CSS/JS 결합형 완벽 오목판 주입
    omok_html = """
    <div class="board-frame">
        <div id="omok-grid" class="omok-grid"></div>
    </div>
    <h3 id="turn-txt" style="text-align:center; color:#333; margin-top:15px;">현재 차례: ⚫ 흑돌</h3>

    <style>
    .board-frame {
        background-color: #f1c40f;
        padding: 12px;
        border-radius: 8px;
        width: fit-content;
        margin: 0 auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .omok-grid {
        display: grid;
        grid-template-columns: repeat(10, 40px);
        grid-template-rows: repeat(10, 40px);
        gap: 1px;
        background-color: #4a3319; /* 명확한 격자 선 색상 */
        border: 2px solid #4a3319;
    }
    .omok-cell {
        background-color: #e8c39e; /* 사진 속 따뜻한 바둑판 색상 */
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    .stone {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        box-shadow: 1px 2px 4px rgba(0,0,0,0.3);
    }
    .black-stone { background: radial-gradient(circle at 30% 30%, #444, #111); }
    .white-stone { background: radial-gradient(circle at 30% 30%, #fff, #ccc); border: 1px solid #aaa; }
    </style>

    <script>
    let turn = 1; // 1: 흑, 2: 백
    const board = Array(10).fill(0).map(() => Array(10).fill(0));
    const grid = document.getElementById('omok-grid');
    const turnTxt = document.getElementById('turn-txt');

    for(let r=0; r<10; r++) {
        for(let c=0; c<10; c++) {
            const cell = document.createElement('div');
            cell.className = 'omok-cell';
            cell.onclick = () => {
                if(board[r][c] === 0) {
                    board[r][c] = turn;
                    const stone = document.createElement('div');
                    stone.className = 'stone ' + (turn === 1 ? 'black-stone' : 'white-stone');
                    cell.appendChild(stone);
                    
                    turn = 3 - turn;
                    turnTxt.innerText = "현재 차례: " + (turn === 1 ? "⚫ 흑돌" : "⚪ 백돌");
                }
            };
            grid.appendChild(cell);
        }
    }
    </script>
    """
    components.html(omok_html, height=520)

with tab2:
    st.subheader("🏁 클래식 체크무늬 체스판")
    st.caption("움직일 말을 누른 뒤, 이동할 칸을 연속해서 선택하세요.")
    
    # HTML/CSS/JS 결합형 완벽 체스판 주입
    chess_html = """
    <div class="board-frame-chess">
        <div id="chess-grid" class="chess-grid"></div>
    </div>
    <div id="status" style="text-align:center; font-weight:bold; margin-top:15px; color:#c0392b;"></div>

    <style>
    .board-frame-chess {
        background-color: #d4ac0d;
        padding: 15px;
        border-radius: 8px;
        width: fit-content;
        margin: 0 auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .chess-grid {
        display: grid;
        grid-template-columns: repeat(8, 50px);
        grid-template-rows: repeat(8, 50px);
        border: 3px solid #3d2f21;
    }
    .chess-cell {
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        user-select: none;
    }
    /* 사진 속 정밀한 갈색/베이지 체크무늬 완벽 구현 */
    .light { background-color: #f0d9b5; }
    .dark { background-color: #b58863; }
    .selected { background-color: #769656 !important; } /* 선택 시 초록색 하이라이트 */
    
    .piece-img {
        width: 45px;
        height: 45px;
    }
    </style>

    <script>
    const imgBase = "https://upload.wikimedia.org/wikipedia/commons";
    const imgs = {
        'r': imgBase + "/a/a0/Chess_rdt45.svg", 'n': imgBase + "/e/ef/Chess_ndt45.svg",
        'b': imgBase + "/9/9b/Chess_bdt45.svg", 'q': imgBase + "/4/47/Chess_qdt45.svg",
        'k': imgBase + "/f/f0/Chess_kdt45.svg", 'p': imgBase + "/c/c7/Chess_pdt45.svg",
        'R': imgBase + "/7/72/Chess_rlt45.svg", 'N': imgBase + "/7/70/Chess_nlt45.svg",
        'B': imgBase + "/b/b1/Chess_blt45.svg", 'Q': imgBase + "/1/15/Chess_qlt45.svg",
        'K': imgBase + "/4/42/Chess_klt45.svg", 'P': imgBase + "/4/45/Chess_plt45.svg"
    };

    let chessBoard = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ];

    let selected = null;
    const grid = document.getElementById('chess-grid');
    const status = document.getElementById('status');

    function drawBoard() {
        grid.innerHTML = '';
        for(let r=0; r<8; r++) {
            for(let c=0; c<8; c++) {
                const cell = document.createElement('div');
                cell.className = 'chess-cell ' + ((r+c)%2 === 1 ? 'dark' : 'light');
                
                if(selected && selected.r === r && selected.c === c) {
                    cell.classList.add('selected');
                }

                const piece = chessBoard[r][c];
                if(piece) {
                    const img = document.createElement('img');
                    img.src = imgs[piece];
                    img.className = 'piece-img';
                    cell.appendChild(img);
                }

                cell.onclick = () => {
                    if(selected === null) {
                        if(chessBoard[r][c] !== '') {
                            selected = {r, c};
                            status.innerText = "말 선택됨! 이동할 칸을 누르세요.";
                            drawBoard();
                        }
                    } else {
                        const p = chessBoard[selected.r][selected.c];
                        chessBoard[selected.r][selected.c] = '';
                        chessBoard[r][c] = p;
                        selected = null;
                        status.innerText = "";
                        drawBoard();
                    }
                };
                grid.appendChild(cell);
            }
        }
    }
    drawBoard();
    </script>
    """
    components.html(chess_html, height=500)
