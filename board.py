import numpy as np

DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1]]
SQUARE_WEIGHTS = [
    [120, -20,  20,   5,   5,  20, -20, 120],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [20,  -5,  15,   3,   3,  15,  -5,  20],
    [5,  -5,   3,   3,   3,   3,  -5,   5],
    [5,  -5,   3,   3,   3,   3,  -5,   5],
    [20,  -5,  15,   3,   3,  15,  -5,  20],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [120, -20,  20,   5,   5,  20, -20, 120],
]

class Board:
    def __init__(self, row_count, column_count, color):
        # Board parameters
        self.row_count = row_count
        self.column_count = column_count
        self.grid = np.zeros((self.row_count, self.column_count))
        self.color = color
        self.available_moves = []
        self.square_weight = SQUARE_WEIGHTS

        # Geometrical parameters
        self.box_size = 50
        self.radius = int(self.box_size / 2 - 5)
        self.board_size = (self.row_count * self.box_size, self.column_count * self.box_size)
        self.left_board_side = 500 - (self.box_size * self.column_count) // 2
        self.top_board_side = 300 - (self.box_size * self.row_count) // 2
        self.bottom_board_side = 300 + (self.box_size * self.row_count) // 2
        self.right_board_side = 500 + (self.box_size * self.column_count) / 2

    def is_there_valid_move(self, next_player_key, last_player_key):
        self.available_moves = []
        for row in range(self.row_count):
            for col in range(self.column_count):
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
                            if not self.overflow(x, y) and self.grid[x][y] == 0 and (x, y) not in self.available_moves:
                                self.available_moves.append((x, y))

    def count_points(self, piece):
        s = 0
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.grid[row][col] == piece:
                    s += 1
        return s

    def overflow(self, x, y):
        return not (0 <= x <= self.column_count - 1 and 0 <= y <= self.row_count - 1)

    def is_clicked(self, mouse_position):
        return self.top_board_side <= mouse_position[1] <= self.bottom_board_side and \
            self.left_board_side <= mouse_position[0] <= self.right_board_side

    def update_grid(self, row_click, column_click, player_key):
        s = 0
        if player_key == 1:
            other_coin = 2
        else:
            other_coin = 1
        for x_direction, y_direction in DIRECTIONS:
            x = row_click + x_direction
            y = column_click + y_direction
            if not self.overflow(x, y) and self.grid[x][y] == other_coin:
                x += x_direction
                y += y_direction
                while not self.overflow(x, y) and self.grid[x][y] == other_coin:
                    x += x_direction
                    y += y_direction
                if not self.overflow(x, y) and self.grid[x][y] == player_key:
                    while x != row_click or y != column_click:
                        x -= x_direction
                        y -= y_direction
                        s += 1
                        self.grid[x][y] = player_key
        return s

    def reset_board(self):
        self.grid = np.zeros((self.row_count, self.column_count))

    def copy_board(self):
        board = Board(self.row_count, self.column_count, (89, 139, 44))
        board.grid = np.copy(self.grid)
        return board
