import numpy as np
import re
from typing import List, Tuple


class XMASFinder:
    DIRECTIONS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
    TARGET = 'XMAS'

    def __init__(self, file_path):
        self.grid = self.read_data(file_path)
        self.rows, self.cols = self.grid.shape
        self.masmatches = []

    def read_data(self, file_path: str):
        with open(file_path) as f:
            lines = [x.strip() for x in f.readlines()]
        grid = np.array([[x for x in line] for line in lines])

        return grid

    def is_valid_pos(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def check_direction(self, start_row: int, start_col: int, delta_row: int, delta_col: int) -> bool:
        for idx, letter in enumerate(self.TARGET):
            row = start_row + delta_row * idx
            col = start_col + delta_col * idx
            if not self.is_valid_pos(row, col) or self.grid[row, col] != letter:
                return False
        return True

    def count_paths(self) -> int:
        count = 0
        x_positions = np.argwhere(self.grid == 'X')

        for row, col in x_positions:
            for delta_row, delta_col in self.DIRECTIONS:
                if self.check_direction(row, col, delta_row, delta_col):
                    count += 1

        return count

    def get_corners(self, r1, c1, r2, c2):
        corners=[self.grid[r1, c1], self.grid[r1, c2], self.grid[r2, c1], self.grid[r2, c2]]
        return corners

    def find_mas(self):
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                # Check if center is 'A'
                if self.grid[i, j] != 'A':
                    continue

                # Check corners
                corners = self.get_corners(i-1, j-1, i+1, j+1)
                if corners in (['M', 'M', 'S', 'S'], ['S', 'S', 'M', 'M'],
                               ['S', 'M', 'S', 'M'], ['M', 'S', 'M', 'S']):

                    self.masmatches.append((i, j))

        return len(self.masmatches)


if __name__ == '__main__':
    xf = XMASFinder('input_d04.txt')
    paths =  xf.count_paths()
    print(paths)
    # print(xf.grid)
    print(xf.find_mas())
