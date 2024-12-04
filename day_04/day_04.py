import numpy as np
import re
from typing import List, Tuple


class XMASFinder:
    DIRECTIONS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
    TARGET = 'XMAS'

    def __init__(self, file_path):
        self.grid, self.bfstring = self.read_data(file_path)
        self.rows, self.cols = self.grid.shape

    def read_data(self, file_path: str):
        with open(file_path) as f:
            lines = [x.strip() for x in f.readlines()]
        grid = np.array([[x for x in line] for line in lines])
        bigfatstring = ''.join(lines)
        return grid, bigfatstring

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

    def check_a_mas(self, expr):
        start = 0
        while start < len(self.bfstring) + self.cols + 1:
                match = re.search(expr, self.bfstring[start:])
                if match:
                    self.matches += 1
                    if np.mod(match.start() + 4, self.cols) == 0:
                        start += match.start() + 4
                    else:
                        start += match.start() + 1
                    print(match)
                else:
                    break

    def find_masmas(self):

        print(self.bfstring)
        exprs = [r'(M.S).{'+str(self.cols-3)+'}(.A.).{'+str(self.cols-3)+'}(M.S)',
                 r'(S.M).{'+str(self.cols-3)+'}(.A.).{'+str(self.cols-3)+'}(S.M)',
                 r'(M.M).{'+str(self.cols-3)+'}(.A.).{'+str(self.cols-3)+'}(S.S)',
                 r'(S.S).{'+str(self.cols-3)+'}(.A.).{'+str(self.cols-3)+'}(M.M)']

        self.matches = 0

        for expr in exprs:
            self.check_a_mas(expr)

        return self.matches


if __name__ == '__main__':
    xf = XMASFinder('input_d04_test.txt')
    # paths =  XMASFinder(grid).count_paths()
    # print(paths)
    print(xf.find_masmas())
