from typing import List, Tuple

import numpy as np


class XMASFinder:
    DIRECTIONS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
    TARGET = 'XMAS'
    VALID_MAS_PATTERNS = {
        ('M', 'M', 'S', 'S'),
        ('S', 'S', 'M', 'M'),
        ('S', 'M', 'S', 'M'),
        ('M', 'S', 'M', 'S')
    }

    def __init__(self, file_path: str):
        """Initialize XMASFinder with input file path."""
        self.grid = self.read_data(file_path)
        self.rows, self.cols = self.grid.shape
        self.mas_matches: List[Tuple[int, int]] = []

    @staticmethod
    def read_data(file_path: str) -> np.ndarray:
        """Read and parse input file into numpy array."""
        try:
            with open(file_path) as f:
                lines = [list(line.strip()) for line in f]
            return np.array(lines)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading input file: {str(e)}")

    def is_valid_pos(self, row: int, col: int) -> bool:
        """Check if position is within grid boundaries."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def check_direction(self, start_row: int, start_col: int, delta_row: int, delta_col: int) -> bool:
        """Check if XMAS pattern exists in given direction."""
        current_word = ''
        for idx in range(len(self.TARGET)):
            row = start_row + delta_row * idx
            col = start_col + delta_col * idx
            if not self.is_valid_pos(row, col):
                return False
            current_word += self.grid[row, col]
        return current_word == self.TARGET

    def count_paths(self) -> int:
        """Count total number of XMAS patterns in the grid."""
        count = 0
        x_positions = np.argwhere(self.grid == 'X')

        for row, col in x_positions:
            for delta_row, delta_col in self.DIRECTIONS:
                if self.check_direction(row, col, delta_row, delta_col):
                    count += 1
        return count

    def get_corners(self, r1: int, c1: int, r2: int, c2: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Get corner values for given rectangle coordinates."""
        return (
            self.grid[r1, c1],
            self.grid[r1, c2],
            self.grid[r2, c1],
            self.grid[r2, c2]
        )

    def find_mas(self) -> int:
        """Find all MAS patterns with 'A' in center."""
        self.mas_matches = []

        # Use numpy's advanced indexing to find all 'A' positions
        a_positions = np.argwhere(self.grid == 'A')

        for i, j in a_positions:
            # Skip positions too close to edges
            if i == 0 or i == self.rows - 1 or j == 0 or j == self.cols - 1:
                continue

            corners = self.get_corners(i - 1, j - 1, i + 1, j + 1)
            if corners in self.VALID_MAS_PATTERNS:
                self.mas_matches.append((i, j))

        return len(self.mas_matches)


def main():
    """Main execution function with basic error handling."""
    try:
        xf = XMASFinder('input_d04.txt')
        xmas_count = xf.count_paths()
        mas_count = xf.find_mas()
        print(f"Found {xmas_count} XMAS patterns")
        print(f"Found {mas_count} MAS patterns")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()