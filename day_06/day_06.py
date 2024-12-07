import numpy as np


class BumpMap:
    def __init__(self, file_path):
        self.map = self.load_map(file_path)
        self.visited = np.zeros(self.map.shape)
        self.current_position = np.where(self.map == "^")
        self.current_direction = "^"
        self.visited[self.current_position] = 1
        self.rows, self.cols = self.map.shape
        self.is_off_board = False

    def load_map(self, file_path):
        with open(file_path, "r") as f:
            return np.array([[x for x in line.strip()] for line in f])

    def off_board(self, position):
        return (
            position[0] < 0
            or position[0] >= self.rows
            or position[1] < 0
            or position[1] >= self.cols
        )

    def move(self):
        unobstructed = False
        while not unobstructed:
            proposed_position = self.get_proposed_position(self.current_direction)
            if self.off_board(proposed_position):
                self.is_off_board = True
                return

            if self.map[proposed_position] != '#':
                # print(f"Moving from {self.current_position} to {proposed_position}")
                # print(f"Current direction: {self.current_direction}")
                self.map[self.current_position] = 'X'
                self.current_position = proposed_position
                self.visited[self.current_position] = 1
                self.map[self.current_position] = self.current_direction
                # print(
                #     # self.visited,
                #     # '\n',
                #     self.map)
                unobstructed = True
            else:
                self.current_direction = self.rotate(self.current_direction)

    def get_proposed_position(self, direction):
        if direction == "^":
            proposed_position = (
                self.current_position[0] - 1,
                self.current_position[1],
            )
        elif direction == "v":
            proposed_position = (
                self.current_position[0] + 1,
                self.current_position[1],
            )
        elif direction == "<":
            proposed_position = (
                self.current_position[0],
                self.current_position[1] - 1,
            )
        else: # direction == ">":
            proposed_position = (
                self.current_position[0],
                self.current_position[1] + 1,
            )

        return proposed_position

    def rotate(self, direction):
        if direction == "^":
            return ">"
        elif direction == "v":
            return "<"
        elif direction == "<":
            return "^"
        elif direction == ">":
            return "v"
        else:
            raise ValueError("Invalid direction")

    def walk_about(self):
        while not self.is_off_board:
            self.move()


if __name__ == "__main__":
    bump_map = BumpMap("input_d06.txt")
    bump_map.walk_about()
    print(bump_map.visited.sum())
