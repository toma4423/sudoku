import unittest
import numpy as np
from system import (
    create_empty_grid,
    is_valid,
    solve_sudoku,
    find_empty,
    generate_sudoku,
)


class TestSudokuSystem(unittest.TestCase):
    def setUp(self):
        """テストの前準備"""
        self.empty_grid = create_empty_grid()

        # テスト用の部分的に埋まったグリッド
        self.partial_grid = np.array(
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ]
        )

    def test_create_empty_grid(self):
        """空のグリッド生成のテスト"""
        grid = create_empty_grid()
        self.assertEqual(grid.shape, (9, 9))
        self.assertEqual(np.sum(grid), 0)

    def test_is_valid(self):
        """数字の配置妥当性チェックのテスト"""
        # 行のテスト
        self.assertFalse(is_valid(self.partial_grid, 0, 2, 5))  # 既に行に5が存在
        self.assertTrue(is_valid(self.partial_grid, 0, 2, 1))  # 1は配置可能

        # 列のテスト
        self.assertFalse(is_valid(self.partial_grid, 1, 0, 5))  # 既に列に5が存在
        self.assertTrue(is_valid(self.partial_grid, 1, 0, 2))  # 2は配置可能

        # 3x3ブロックのテスト
        self.assertFalse(is_valid(self.partial_grid, 0, 2, 9))  # ブロックに9が存在
        self.assertTrue(is_valid(self.partial_grid, 0, 2, 4))  # 4は配置可能

    def test_find_empty(self):
        """空のセルを見つけるテストと"""
        pos = find_empty(self.partial_grid)
        self.assertIsNotNone(pos)
        self.assertEqual(self.partial_grid[pos], 0)

        # 全て埋まっているグリッドのテスト
        full_grid = np.ones((9, 9))
        self.assertIsNone(find_empty(full_grid))

    def test_solve_sudoku(self):
        """数独を解くテスト"""
        grid_copy = self.partial_grid.copy()
        self.assertTrue(solve_sudoku(grid_copy))

        # 解けた後のグリッドが正しいかチェック
        for i in range(9):
            # 各行に1-9が含まれているか
            self.assertEqual(set(grid_copy[i]), set(range(1, 10)))
            # 各列に1-9が含まれているか
            self.assertEqual(set(grid_copy[:, i]), set(range(1, 10)))

    def test_generate_sudoku(self):
        """数独パズル生成のテスト"""
        # 各難易度でテスト
        difficulties = ["小盛", "並盛", "大盛"]
        expected_empty = [30, 40, 50]

        for diff, exp_empty in zip(difficulties, expected_empty):
            puzzle, solution = generate_sudoku(diff)

            # パズルと解答が9x9であることを確認
            self.assertEqual(puzzle.shape, (9, 9))
            self.assertEqual(solution.shape, (9, 9))

            # 空のマスの数が正しいことを確認
            empty_count = len(np.where(puzzle == 0)[0])
            self.assertGreaterEqual(empty_count, exp_empty - 5)  # 若干の余裕を持たせる
            self.assertLessEqual(empty_count, exp_empty + 5)

            # 解答が正しい数独であることを確認
            for i in range(9):
                self.assertEqual(set(solution[i]), set(range(1, 10)))
                self.assertEqual(set(solution[:, i]), set(range(1, 10)))


if __name__ == "__main__":
    unittest.main()
