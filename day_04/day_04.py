import numpy as np

class FindXMAS:
    def __init__(self, file_path):
        self.xmas = 'XMAS'
        self.data = self._read_file(file_path)
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.xmas_found = 0
        self.knockout_set = np.zeros((self.rows, self.cols))

    def _read_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = [[x for x in line.strip()] for line in file]

        return np.array(lines)

    def _check_xmas(self, r, c):

        check_letters = ['X','M', 'A', 'S']
        check_positions = {x:[] for x in check_letters}
        check_positions['X'] = [(r, c)]
        for index, letter in enumerate(check_letters[:-1]):
            for position in check_positions[letter]:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        check_row = position[0]+ i
                        check_col = position[1] + j
                        if check_row  >= 0 and check_row < self.rows and check_col  >= 0 and check_col < self.cols:
                            if self.data[check_row ][check_col ] == check_letters[index + 1]:
                                if check_letters[index+1] == 'S':
                                    self.xmas_found += 1

                                check_positions[check_letters[index+1]].append((check_row , check_col))
                                self.knockout_set[check_row, check_col] = 1
        print(check_positions)

    def find_xmas(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.data[r][c] == self.xmas[0]:
                    print(r,c)
                    self._check_xmas(r, c)



if __name__ == '__main__':
    fx = FindXMAS('input_d04_test.txt')
    fx.find_xmas()
    print(fx.xmas_found)
    print(fx.knockout_set)
