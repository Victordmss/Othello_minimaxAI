import numpy as np

DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1]]


class Board:
    def __init__(self, row_count, column_count, color):
        self.row_count = row_count
        self.column_count = column_count
        self.grid = np.zeros((self.row_count, self.column_count))
        self.color = color
        self.box_size = 50
        self.radius = int(self.box_size / 2 - 5)
        self.board_size = (self.row_count * self.box_size, self.column_count * self.box_size)
        self.available_moves = []
        self.left_board_side = 500 - (self.box_size * self.column_count) // 2
        self.top_board_side = 300 - (self.box_size * self.row_count) // 2
        self.bottom_board_side = 300 + (self.box_size * self.row_count) // 2
        self.right_board_side = 500 + (self.box_size * self.column_count) / 2

    def is_there_valid_move(self, row, col, next_player_key, last_player_key):
        if self.grid[row][col] == next_player_key:
            for x_direction, y_direction in DIRECTIONS:
                x = row + x_direction
                y = col + y_direction
                if not self.overflow(x, y) and self.grid[x][y] == last_player_key:
                    x += x_direction
                    y += y_direction
                    while not self.overflow(x, y) and self.grid[x][y] == last_player_key:
                        x += x_direction
                        y += y_direction
                    if not self.overflow(x, y) and self.grid[x][y] == 0:
                        self.available_moves.append((x, y))

    def overflow(self, x, y):
        return not (0 <= x <= self.column_count - 1 and 0 <= y <= self.row_count - 1)

    def is_clicked(self, mouse_position):
        return self.top_board_side <= mouse_position[1] <= self.bottom_board_side and \
            self.left_board_side <= mouse_position[0] <= self.right_board_side

    def update_grid(self, row_click, column_click, current_player):
        valid_move = False
        if current_player == 1:
            other_coin = 2
        else:
            other_coin = 1
        x = row_click
        y = column_click
        for x_direction, y_direction in DIRECTIONS:
            x = row_click + x_direction
            y = column_click + y_direction
            if not self.overflow(x, y) and self.grid[x][y] == other_coin:
                x += x_direction
                y += y_direction
                while not self.overflow(x, y) and self.grid[x][y] == other_coin:
                    x += x_direction
                    y += y_direction
                if not self.overflow(x, y) and self.grid[x][y] == current_player:
                    valid_move = True
                    while x != row_click or y != column_click:
                        x -= x_direction
                        y -= y_direction
                        self.grid[x][y] = current_player
        return valid_move

    def reset_board(self):
        self.grid = np.zeros((self.row_count, self.column_count))

