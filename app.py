import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Perfect Omok", layout="centered")

st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🧱 진짜 격자선 위에 놓이는 오목방</h2>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["⚫ 오목 (Omok)", "👑 체스 (Chess)"])

with tab1:
    st.subheader("🪵 교차점 착수 오목판")
    st.caption("네모 칸 안이 아니라, 선과 선이 만나는 '교차점' 위에 돌이 올라갑니다!")
    
    omok_html = """
    <div class="main-container">
        <h3 class="status-title" id="o-turn">차례: ⚫ 흑돌</h3>
        <div class="board-wood-frame">
            <div id="o-grid" class="omok-grid-system"></div>
        </div>
        <button class="reset-btn" onclick="resetOmok()">🔄 오목판 초기화</button>
    </div>

    <style>
    .main-container { text-align: center; font-family: sans-serif; }
    .status-title { color: #333; margin-bottom: 10px; font-size: 20px; }
    
    /* 실제 나무 바둑판 프레임 */
    .board-wood-frame {
        background-color: #e8c39e; /* 따뜻한 나무색 */
        padding: 20px;
        border-radius: 8px;
        width: fit-content;
        margin: 0 auto;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        border: 2px solid #b58863;
    }
    
    /* 10x10 교차점을 만들기 위한 그리드 시스템 */
    .omok-grid-system {
        display: grid;
        grid-template-columns: repeat(10, 42px);
        grid-template-rows: repeat(10, 42px);
        position: relative;
    }
    
    /* 선과 선이 만나는 교차점 칸 디자인 */
    .omok-tile {
        position: relative;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    /* 십자가 격자선 그리기 (핵심 테크닉!) */
    .omok-tile::before {
        content: "";
        position: absolute;
        background-color: #4a3411; /* 선 색상 */
        width: 100%;
        height: 1px; /* 가로선 */
        top: 50%;
        left: 0;
        z-index: 1;
    }
    .omok-tile::after {
        content: "";
        position: absolute;
        background-color: #4a3411; /* 선 색상 */
        width: 1px; /* 세로선 */
        height: 100%;
        top: 0;
        left: 50%;
        z-index: 1;
    }
    
    /* 진짜 입체 바둑돌 (선 위로 올라오도록 z-index 설정) */
    .stone { 
        width: 36px; 
        height: 36px; 
        border-radius: 50%; 
        position: relative;
        z-index: 5; /* 선보다 위로 올라오게 함 */
        box-shadow: 1px 2px 4px rgba(0,0,0,0.4); 
    }
    .b-stone { background: radial-gradient(circle at 30% 30%, #555, #111); }
    .w-stone { background: radial-gradient(circle at 30% 30%, #fff, #ccc); border: 1px solid #999; }
    
    .reset-btn { margin-top: 15px; padding: 8px 16px; font-size: 14px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background: #fff; }
    .reset-btn:hover { background: #f0f0f0; }
    </style>

    <script>
    let oTurn = 1; 
    let gameOver = false;
    let oBoard = Array(10).fill(0).map(() => Array(10).fill(0));
    const oGrid = document.getElementById('o-grid');
    const oTxt = document.getElementById('o-turn');

    function checkWin(r, c, color) {
        const dir = [[0,1], [1,0], [1,1], [1,-1]];
        for(let [dr, dc] of dir) {
            let count = 1;
            let nr = r + dr, nc = c + dc;
            while(nr>=0 && nr<10 && nc>=0 && nc<10 && oBoard[nr][nc] === color) { count++; nr+=dr; nc+=dc; }
            nr = r - dr; nc = c - dc;
            while(nr>=0 && nr<10 && nc>=0 && nc<10 && oBoard[nr][nc] === color) { count++; nr-=dr; nc-=dc; }
            if(count >= 5) return true;
        }
        return false;
    }

    function buildBoard() {
        oGrid.innerHTML = '';
        for(let r=0; r<10; r++) {
            for(let c=0; c<10; c++) {
                const tile = document.createElement('div');
                tile.className = 'omok-tile';
                
                if(oBoard[r][c] === 1) {
                    const stn = document.createElement('div'); stn.className = 'stone b-stone'; tile.appendChild(stn);
                } else if(oBoard[r][c] === 2) {
                    const stn = document.createElement('div'); stn.className = 'stone w-stone'; tile.appendChild(stn);
                }

                tile.onclick = () => {
                    if(oBoard[r][c] === 0 && !gameOver) {
                        oBoard[r][c] = oTurn;
                        if(checkWin(r, c, oTurn)) {
                            buildBoard();
                            oTxt.innerHTML = "🎉 " + (oTurn === 1 ? "흑돌(Black)" : "백돌(White)") + " 승리!!!";
                            gameOver = true;
                            return;
                        }
                        oTurn = 3 - oTurn;
                        oTxt.innerText = "차례: " + (oTurn === 1 ? "⚫ 흑돌" : "⚪ 백돌");
                        buildBoard();
                    }
                };
                oGrid.appendChild(tile);
            }
        }
    }

    function resetOmok() {
        oTurn = 1;
        gameOver = false;
        oBoard = Array(10).fill(0).map(() => Array(10).fill(0));
        oTxt.innerText = "차례: ⚫ 흑돌";
        buildBoard();
    }

    buildBoard();
    </script>
    """
    components.html(omok_html, height=580)

with tab2:
    st.subheader("🏁 체스판 (클래식 체크무늬)")
    st.caption("체스는 오목과 달리 칸(네모 상자) 안에 말을 배치하는 것이 정상 규칙입니다.")
    
    chess_html = """
    <div class="main-container">
        <h3 class="status-title" id="c-status">움직일 말을 선택하세요</h3>
        <div class="chess-wood-frame">
            <div id="c-grid" class="chess-grid-system"></div>
        </div>
    </div>

    <style>
    .chess-wood-frame {
        background-color: #d4ac0d;
        padding: 12px;
        border-radius: 10px;
        width: fit-content;
        margin: 0 auto;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }
    .chess-grid-system {
        display: grid;
        grid-template-columns: repeat(8, 52px);
        grid-template-rows: repeat(8, 52px);
        border: 2px solid #3d2f21;
    }
    .chess-tile { display: flex; align-items: center; justify-content: center; cursor: pointer; }
    .white-tile { background-color: #f0d9b5; }
    .dark-tile { background-color: #b58863; }
    .active-select { background-color: #769656 !important; }
    .p-img { width: 46px; height: 46px; object-fit: contain; }
    </style>

    <script>
    const base = "https://upload.wikimedia.org/wikipedia/commons";
    const cImgs = {
        'r': base + "/a/a0/Chess_rdt45.svg", 'n': base + "/e/ef/Chess_ndt45.svg",
        'b': base + "/9/9b/Chess_bdt45.svg", 'q': base + "/4/47/Chess_qdt45.svg",
        'k': base + "/f/f0/Chess_kdt45.svg", 'p': base + "/c/c7/Chess_pdt45.svg",
        'R': base + "/7/72/Chess_rlt45.svg", 'N': base + "/7/70/Chess_nlt45.svg",
        'B': base + "/b/b1/Chess_blt45.svg", 'Q': base + "/1/15/Chess_qlt45.svg",
        'K': base + "/4/42/Chess_klt45.svg", 'P': base + "/4/45/Chess_plt45.svg"
    };

    let cBoard = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R']
    ];

    let selectState = null;
    const cGrid = document.getElementById('c-grid');
    const cTxt = document.getElementById('c-status');

    function renderChess() {
        cGrid.innerHTML = '';
        for(let r=0; r<8; r++) {
            for(let c=0; c<8; c++) {
                const tile = document.createElement('div');
                tile.className = 'chess-tile ' + ((r+c)%2 === 1 ? 'dark-tile' : 'white-tile');
                
                if(selectState && selectState.r === r && selectState.c === c) {
                    tile.classList.add('active-select');
                }

                const p = cBoard[r][c];
                if(p) {
                    const img = document.createElement('img');
                    img.src = cImgs[p];
                    img.className = 'p-img';
                    tile.appendChild(img);
                }

                tile.onclick = () => {
                    if(selectState === null) {
                        if(cBoard[r][c] !== '') {
                            selectState = {r, c};
                            cTxt.innerText = "이동할 목표 칸을 누르세요.";
                            renderChess();
                        }
                    } else {
                        const targetPiece = cBoard[selectState.r][selectState.c];
                        cBoard[selectState.r][selectState.c] = '';
                        cBoard[r][c] = targetPiece;
                        selectState = null;
                        cTxt.innerText = "말을 움직였습니다.";
                        renderChess();
                    }
                };
                cGrid.appendChild(tile);
            }
        }
    }
    renderChess();
    </script>
    """
    components.html(chess_html, height=550)
