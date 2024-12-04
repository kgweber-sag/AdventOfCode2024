import numpy as np

class FindXMAS:
    def __init__(self, file_path):
        self.xmas = 'XMAS'
        self.data = self._read_file(file_path)
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.xmas_found = 0

    def _read_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = [[x for x in line.strip()] for line in file]

        return np.array(lines)

    def _check_xmas(self, r, c):

        check_letters =[x for x in self.xmas]

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                check_row = r + i
                check_col = c + j
                if 0 <= check_row < self.rows and 0 <= check_col < self.cols:
                    if self.data[check_row ][check_col ] == check_letters[1]:
                        # we know our direction change is the i, j vector
                        for index, letter in enumerate(check_letters[2:]):
                            row_delta = i*(index+2)
                            col_delta = j*(index+2)
                            if 0 <= (r + row_delta) < self.rows and 0 <= (c + col_delta) < self.cols:
                                if self.data[r + row_delta][c + col_delta] == letter:
                                    if index+3 == len(self.xmas):
                                        self.xmas_found += 1
                                    else:
                                        continue
                                else:
                                    break


    def find_xmas(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.data[r][c] == self.xmas[0]:
                    self._check_xmas(r, c)



if __name__ == '__main__':
    fx = FindXMAS('input_d04.txt')
    fx.find_xmas()
    print(fx.xmas_found)
