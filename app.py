import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pro Grid Games", layout="centered")

st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🏁 대형 오목판 & 진짜 규칙 체스</h2>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["⚫ 초대형 오목 (15x15)", "👑 진짜 규칙 체스 (Chess)"])

with tab1:
    st.subheader("🪵 15x15 정식 규격 오목판")
    st.caption("판이 훨씬 넓어졌습니다! 진짜 바둑판처럼 선과 선이 만나는 교차점 위에 돌을 놓으세요.")
    
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
    .status-title { color: #333; margin-bottom: 10px; font-size: 20px; font-weight: bold; }
    
    .board-wood-frame {
        background-color: #e8c39e;
        padding: 20px;
        border-radius: 8px;
        width: fit-content;
        margin: 0 auto;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        border: 2px solid #b58863;
    }
    
    /* 15x15 대형 격자 시스템 */
    .omok-grid-system {
        display: grid;
        grid-template-columns: repeat(15, 32px);
        grid-template-rows: repeat(15, 32px);
        position: relative;
    }
    
    .omok-tile {
        position: relative;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    /* 교차점 십자가 선 */
    .omok-tile::before {
        content: ""; position: absolute; background-color: #4a3411;
        width: 100%; height: 1px; top: 50%; left: 0; z-index: 1;
    }
    .omok-tile::after {
        content: ""; position: absolute; background-color: #4a3411;
        width: 1px; height: 100%; top: 0; left: 50%; z-index: 1;
    }
    
    .stone { 
        width: 28px; height: 28px; border-radius: 50%; position: relative;
        z-index: 5; box-shadow: 1px 2px 3px rgba(0,0,0,0.4); 
    }
    .b-stone { background: radial-gradient(circle at 30% 30%, #555, #111); }
    .w-stone { background: radial-gradient(circle at 30% 30%, #fff, #ccc); border: 1px solid #999; }
    
    .reset-btn { margin-top: 15px; padding: 8px 16px; font-size: 14px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background: #fff; }
    .reset-btn:hover { background: #f0f0f0; }
    </style>

    <script>
    let oTurn = 1; 
    let gameOver = false;
    let oBoard = Array(15).fill(0).map(() => Array(15).fill(0));
    const oGrid = document.getElementById('o-grid');
    const oTxt = document.getElementById('o-turn');

    function checkWin(r, c, color) {
        const dir = [[0,1], [1,0], [1,1], [1,-1]];
        for(let [dr, dc] of dir) {
            let count = 1;
            let nr = r + dr, nc = c + dc;
            while(nr>=0 && nr<15 && nc>=0 && nc<15 && oBoard[nr][nc] === color) { count++; nr+=dr; nc+=dc; }
            nr = r - dr; nc = c - dc;
            while(nr>=0 && nr<15 && nc>=0 && nc<15 && oBoard[nr][nc] === color) { count++; nr-=dr; nc-=dc; }
            if(count >= 5) return true;
        }
        return false;
    }

    function buildBoard() {
        oGrid.innerHTML = '';
        for(let r=0; r<15; r++) {
            for(let c=0; c<15; c++) {
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
                            oTxt.innerHTML = "🎉 " + (oTurn === 1 ? "흑돌" : "백돌") + " 승리!!!";
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
        oTurn = 1; gameOver = false;
        oBoard = Array(15).fill(0).map(() => Array(15).fill(0));
        oTxt.innerText = "차례: ⚫ 흑돌";
        buildBoard();
    }
    buildBoard();
    </script>
    """
