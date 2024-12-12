import streamlit as st
import numpy as np
import random

# ページの設定
st.set_page_config(page_title="数独ゲーム")

# CSSスタイルの定義
st.markdown(
    """
<style>
    .invalid-input {
        color: red !important;
    }
    .stTextInput input {
        text-align: center;
        font-size: 20px;
    }
    .fixed-number {
        text-align: center;
        font-size: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def create_empty_grid():
    return np.zeros((9, 9), dtype=int)


def is_valid(grid, row, col, num):
    # 現在のセルの値を一時的に0にして検証
    original_value = grid[row, col]
    grid[row, col] = 0

    # 行チェック
    if num in grid[row]:
        grid[row, col] = original_value
        return False

    # 列チェック
    if num in grid[:, col]:
        grid[row, col] = original_value
        return False

    # 3x3ブロックチェック
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
    # 難易度に応じて残す数字の数を決定
    if difficulty == "小盛":
        remove_count = 30
    elif difficulty == "並盛":
        remove_count = 40
    else:  # "大盛"
        remove_count = 50

    # 空のグリッドを作成
    grid = create_empty_grid()

    # 最初の行をランダムに埋める
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    grid[0] = numbers

    # 解を求める
    solve_sudoku(grid)

    # 難易度に応じて数字を削除
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)

    solution = grid.copy()

    for pos in positions[:remove_count]:
        grid[pos] = 0

    return grid, solution


def reset_game(difficulty):
    # 新しい問題を生成
    puzzle, solution = generate_sudoku(difficulty)
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.invalid_cells = set()


def main():
    st.title("数独ゲーム")

    # 難易度選択
    difficulties = ["小盛", "並盛", "大盛"]
    selected_difficulty = st.selectbox(
        "難易度を選択してください：", difficulties, index=1
    )

    # 初期化
    if "puzzle" not in st.session_state or "solution" not in st.session_state:
        reset_game(selected_difficulty)

    # リスタートボタン
    if (
        st.button("リスタート")
        or st.session_state.get("last_difficulty") != selected_difficulty
    ):
        reset_game(selected_difficulty)
        st.session_state.last_difficulty = selected_difficulty

    # グリッドの表示
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            with cols[j]:
                if st.session_state.puzzle[i, j] != 0:
                    st.markdown(
                        f'<div class="fixed-number">{st.session_state.puzzle[i, j]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    # ユーザー入力用のテキストボックス
                    key = f"input_{i}_{j}"
                    current_value = st.session_state.user_input[i][j]

                    # 入力が無効な場合のスタイル
                    is_invalid = (i, j) in st.session_state.invalid_cells
                    style = "invalid-input" if is_invalid else ""

                    value = st.text_input(
                        f"Cell {i}-{j}",
                        value=current_value,
                        key=key,
                        max_chars=1,
                        label_visibility="collapsed",
                        help="1-9の数字を入力してください",
                    )

                    if value != current_value:  # 値が変更された場合
                        if value:
                            try:
                                num = int(value)
                                if 1 <= num <= 9:
                                    # 入力値の検証
                                    temp_grid = st.session_state.puzzle.copy()
                                    for x in range(9):
                                        for y in range(9):
                                            if st.session_state.user_input[x][y]:
                                                temp_grid[x, y] = int(
                                                    st.session_state.user_input[x][y]
                                                )
                                    temp_grid[i, j] = num

                                    if is_valid(temp_grid, i, j, num):
                                        st.session_state.invalid_cells.discard((i, j))
                                    else:
                                        st.session_state.invalid_cells.add((i, j))
                                else:
                                    st.session_state.invalid_cells.add((i, j))
                            except ValueError:
                                st.session_state.invalid_cells.add((i, j))
                        else:
                            st.session_state.invalid_cells.discard((i, j))

                        st.session_state.user_input[i][j] = value

                    # 無効な入力のスタイリング
                    if is_invalid:
                        st.markdown(
                            f"""
                            <style>
                                div[data-testid="stText"] input#{key} {{
                                    color: red !important;
                                }}
                            </style>
                        """,
                            unsafe_allow_html=True,
                        )

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

    if (
        is_complete
        and np.array_equal(filled_grid, st.session_state.solution)
        and not st.session_state.invalid_cells
    ):
        st.success("おめでとうございます！")


if __name__ == "__main__":
    main()
