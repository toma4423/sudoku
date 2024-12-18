# system.py

import numpy as np
import random


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
