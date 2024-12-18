# app.py

import streamlit as st
import numpy as np
from css_style import get_css_styles
from system import generate_sudoku

# ページの設定
st.set_page_config(page_title="数独ゲーム", layout="centered")


def reset_game(difficulty):
    """
    ゲームの完全リセット
    - セッション状態をクリア
    - 新しいパズルを生成
    - 入力フィールドをリセット
    """
    # セッション状態を完全にクリア（テキストカラーは保持）
    text_color = st.session_state.get("text_color", "#000000")
    game_related_keys = [
        key for key in st.session_state.keys() if key not in ["text_color"]
    ]
    for key in game_related_keys:
        del st.session_state[key]

    # テキストカラーを復元
    st.session_state.text_color = text_color

    # 新しいパズルを生成
    puzzle, solution = generate_sudoku(difficulty)

    # セッション状態を新しく設定
    st.session_state.puzzle = puzzle
    st.session_state.solution = solution
    st.session_state.user_input = [["" for _ in range(9)] for _ in range(9)]
    st.session_state.invalid_cells = set()
    st.session_state.last_difficulty = difficulty

    # 入力フィールドの初期化
    for i in range(9):
        for j in range(9):
            key = f"input_{i}_{j}"
            if key in st.session_state:
                del st.session_state[key]

    # 強制的に再描画を要求
    st.rerun()


def main():
    st.title("数独ゲーム")

    # カラーピッカーを追加
    if "text_color" not in st.session_state:
        st.session_state.text_color = "#000000"

    # コントロールパネル
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        difficulties = ["小盛", "並盛", "大盛"]
        selected_difficulty = st.selectbox(
            "難易度を選択してください：", difficulties, index=1
        )

    with col2:
        if st.button("リスタート", use_container_width=True):
            reset_game(selected_difficulty)

    with col3:
        text_color = st.color_picker("文字色", value=st.session_state.text_color)
        if text_color != st.session_state.text_color:
            st.session_state.text_color = text_color
            st.rerun()  # experimental_rerun()から変更

    st.markdown("</div>", unsafe_allow_html=True)

    # CSSの適用
    st.markdown(get_css_styles(st.session_state.text_color), unsafe_allow_html=True)

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

                            # 数独セルの入力フィールド部分
                            value = st.text_input(
                                f"セル {i+1}-{j+1}",  # アクセシビリティのためのラベル追加
                                value=current_value,
                                key=key,
                                max_chars=1,
                                label_visibility="collapsed",
                                placeholder="",  # プレースホルダーを追加
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
