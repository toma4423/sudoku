import streamlit as st
import numpy as np
import random

# ページの設定
st.set_page_config(page_title="数独ゲーム", layout="centered")

# CSSスタイルの定義
st.markdown(
    """
    <style>
    /* 入力フィールドのスタイル */
    .stTextInput > div > div > input {
        min-height: 40px !important;
        width: 40px !important;
        padding: 0 !important;
        text-align: center !important;
        font-size: 20px !important;
        margin: 1px !important;
        color: #FFFFFF !important;  /* 入力テキストを黒に */
    }
    
    /* 固定数字のスタイル */
    .fixed-number {
        background-color: #f0f0f0;
        min-height: 40px;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        margin: 1px;
        border: 1px solid #ddd;
        border-radius: 4px;
        color: #000000;  /* 固定数字を黒に */
    }

    /* 3x3ブロックの区切り線用のスペース */
    .block-divider {
        margin: 3px 0;
    }

    .vertical-divider {
        margin: 0 3px;
    }

    /* コンテナの余白調整 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Streamlitのデフォルトの余白を調整 */
    .stTextInput > div {
        padding: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def create_empty_grid():
    return np.zeros((9, 9), dtype=int)


def is_valid(grid, row, col, num):
    original_value = grid[row, col]
    grid[row, col] = 0

    if num in grid[row] or num in grid[:, col]:
        grid[row, col] = original_value
        return False

    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i, j] == num:
                grid[row, col] = original_value
                return False

    grid[row, col] = original_value
    return True


def solve_sudoku(grid):
    empty = find_empty(grid)
    if not empty:
        return True

    row, col = empty
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row, col] = num
            if solve_sudoku(grid):
                return True
            grid[row, col] = 0
    return False


def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i, j] == 0:
                return (i, j)
    return None


def generate_sudoku(difficulty):
    if difficulty == "小盛":
        remove_count = 30
    elif difficulty == "並盛":
        remove_count = 40
    else:  # "大盛"
        remove_count = 50

    grid = create_empty_grid()
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    grid[0] = numbers

    solve_sudoku(grid)
    solution = grid.copy()

    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)

    for pos in positions[:remove_count]:
        grid[pos] = 0

    return grid, solution


def reset_game(difficulty):
    puzzle, solution = generate_sudoku(difficulty)
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.invalid_cells = set()


def main():
    st.title("数独ゲーム")

    # コントロールパネル
    col1, col2 = st.columns([2, 1])
    with col1:
        difficulties = ["小盛", "並盛", "大盛"]
        selected_difficulty = st.selectbox(
            "難易度を選択してください：", difficulties, index=1
        )

    with col2:
        if st.button("リスタート", use_container_width=True):
            reset_game(selected_difficulty)

    # 初期化
    if "puzzle" not in st.session_state or "solution" not in st.session_state:
        reset_game(selected_difficulty)

    if st.session_state.get("last_difficulty") != selected_difficulty:
        reset_game(selected_difficulty)
        st.session_state.last_difficulty = selected_difficulty

    # 数独グリッドの表示
    st.write("")  # スペースを追加

    # 9x9のグリッドを3x3のブロックに分けて表示
    for block_row in range(3):
        if block_row > 0:
            st.markdown('<div class="block-divider"></div>', unsafe_allow_html=True)

        for row in range(3):
            i = block_row * 3 + row
            cols = st.columns([1, 1, 1, 0.2, 1, 1, 1, 0.2, 1, 1, 1])

            col_index = 0
            for block_col in range(3):
                if block_col > 0:
                    col_index += 1  # 区切り線用の列をスキップ

                for col in range(3):
                    j = block_col * 3 + col
                    with cols[col_index]:
                        if st.session_state.puzzle[i, j] != 0:
                            st.markdown(
                                f'<div class="fixed-number">{st.session_state.puzzle[i, j]}</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            key = f"input_{i}_{j}"
                            current_value = st.session_state.user_input[i][j]

                            value = st.text_input(
                                "",
                                value=current_value,
                                key=key,
                                max_chars=1,
                                label_visibility="collapsed",
                            )

                            if value != current_value:
                                if value:
                                    try:
                                        num = int(value)
                                        if 1 <= num <= 9:
                                            st.session_state.user_input[i][j] = value
                                        else:
                                            st.session_state.user_input[i][j] = ""
                                    except ValueError:
                                        st.session_state.user_input[i][j] = ""
                                else:
                                    st.session_state.user_input[i][j] = ""

                    col_index += 1

    # ゲームクリアチェック
    filled_grid = st.session_state.puzzle.copy()
    is_complete = True

    for i in range(9):
        for j in range(9):
            if st.session_state.puzzle[i, j] == 0:
                if not st.session_state.user_input[i][j]:
                    is_complete = False
                    break
                try:
                    filled_grid[i, j] = int(st.session_state.user_input[i][j])
                except ValueError:
                    is_complete = False
                    break

    if is_complete and np.array_equal(filled_grid, st.session_state.solution):
        st.success("おめでとうございます！🎉")
        st.balloons()


if __name__ == "__main__":
    main()
