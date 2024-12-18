import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from app import reset_game
import streamlit as st


class MockSessionState(dict):
    """セッションステートをモックするためのカスタムクラス"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class TestSudokuApp(unittest.TestCase):
    def setUp(self):
        """テストの前準備"""
        # カスタムモックセッションステートの初期化
        self.mock_session_state = MockSessionState()

        # セッションステートのパッチ
        self.patcher = patch("streamlit.session_state", self.mock_session_state)
        self.mock_st = self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_game_state_initialization(self):
        """ゲーム状態の初期化テスト"""
        # ゲームのリセット
        reset_game("並盛")

        # 基本的な状態変数の存在確認
        self.assertIn("puzzle", self.mock_session_state)
        self.assertIn("solution", self.mock_session_state)
        self.assertIn("user_input", self.mock_session_state)

        # パズルと解答の形状確認
        self.assertEqual(self.mock_session_state["puzzle"].shape, (9, 9))
        self.assertEqual(self.mock_session_state["solution"].shape, (9, 9))

        # ユーザー入力の初期状態確認
        user_input = self.mock_session_state["user_input"]
        self.assertEqual(len(user_input), 9)
        self.assertEqual(len(user_input[0]), 9)
        self.assertTrue(all(cell == "" for row in user_input for cell in row))

    def test_puzzle_generation(self):
        """パズル生成のテスト"""
        # ゲームのリセット
        reset_game("並盛")

        puzzle = self.mock_session_state["puzzle"]
        solution = self.mock_session_state["solution"]

        # 空白セルの数の確認（並盛の場合）
        empty_count = np.count_nonzero(puzzle == 0)
        self.assertGreaterEqual(empty_count, 35)
        self.assertLessEqual(empty_count, 45)

        # 解答の妥当性確認
        for i in range(9):
            # 各行のチェック
            row_values = set(solution[i])
            self.assertEqual(row_values, set(range(1, 10)))

            # 各列のチェック
            col_values = set(solution[:, i])
            self.assertEqual(col_values, set(range(1, 10)))

        # 3x3ブロックのチェック
        for block_row in range(3):
            for block_col in range(3):
                block = solution[
                    block_row * 3 : (block_row + 1) * 3,
                    block_col * 3 : (block_col + 1) * 3,
                ]
                block_values = set(block.flatten())
                self.assertEqual(block_values, set(range(1, 10)))

    def test_user_input_reset(self):
        """ユーザー入力のリセットテスト"""
        # 初期状態を設定
        self.mock_session_state["user_input"] = [
            ["" for _ in range(9)] for _ in range(9)
        ]
        self.mock_session_state["user_input"][0][0] = "5"
        self.mock_session_state["user_input"][1][1] = "3"

        # ゲームのリセット
        reset_game("並盛")

        # リセット後の状態確認
        user_input = self.mock_session_state["user_input"]
        for i in range(9):
            for j in range(9):
                self.assertEqual(
                    user_input[i][j], "", f"セル({i},{j})の入力値がクリアされていません"
                )

    def test_difficulty_settings(self):
        """難易度設定のテスト"""
        difficulties = {"小盛": (25, 35), "並盛": (35, 45), "大盛": (45, 55)}

        for diff, (min_empty, max_empty) in difficulties.items():
            reset_game(diff)
            puzzle = self.mock_session_state["puzzle"]
            empty_count = np.count_nonzero(puzzle == 0)

            self.assertGreaterEqual(
                empty_count, min_empty, f"{diff}の空白セル数が少なすぎます"
            )
            self.assertLessEqual(
                empty_count, max_empty, f"{diff}の空白セル数が多すぎます"
            )

    def test_complete_game_reset(self):
        """完全なゲームリセット機能のテスト"""
        # ゲーム状態を設定
        self.mock_session_state.update(
            {
                "text_color": "#000000",
                "puzzle": np.zeros((9, 9)),
                "solution": np.zeros((9, 9)),
                "user_input": [["5" for _ in range(9)] for _ in range(9)],
                "input_0_0": "5",
                "input_1_1": "3",
            }
        )

        # リセットを実行
        reset_game("並盛")

        # テキストカラー以外のすべての状態がリセットされていることを確認
        self.assertIn("text_color", self.mock_session_state)
        self.assertNotIn("input_0_0", self.mock_session_state)
        self.assertNotIn("input_1_1", self.mock_session_state)

        # ユーザー入力が空の状態であることを確認
        self.assertTrue(
            all(
                cell == ""
                for row in self.mock_session_state["user_input"]
                for cell in row
            )
        )


if __name__ == "__main__":
    unittest.main()
