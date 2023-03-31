import numpy as np

# Global constant variable

DIRECTIONS = [  # Represents all the possible directions in a two-dimensional space
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0],
    [1, 1],
    [-1, -1],
    [-1, 1],
    [1, -1],
]

SQUARE_WEIGHTS = [  # Matrix representing the game grid weighted by the importance of the positions to win
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120],
]


# This class represents the game board, composed of the logical grid and the board display parameters.
class Board:
    def __init__(self, row_count, column_count, color, screen_size):
        # Logical board parameters
        self.row_count = row_count   # Number of rows of the board
        self.column_count = column_count    # Number of columns of the board
        self.grid = np.zeros((self.row_count, self.column_count))   # Logical grid of the board
        self.available_moves = []   # List of all the possible moves for the current player at each moment of the game
        self.square_weight = SQUARE_WEIGHTS

        # Display board parameters
        self.color = color   # Color of the board
        self.box_size = 50   # Size of each box of the board (they are squares, so we just need one value)
        self.radius = int(self.box_size / 2 - 5)    # Radius of the board pieces (no matter the color/player)
        self.board_size = (self.row_count * self.box_size, self.column_count * self.box_size)   # Size of the board
        # Screen is (1000*600)
        self.left_board_side = screen_size[0]//2 - (self.box_size * self.column_count) // 2   # Left board display side
        self.top_board_side = screen_size[1]//2 - (self.box_size * self.row_count) // 2   # Top board display side
        self.bottom_board_side = screen_size[1]//2 + (self.box_size * self.row_count) // 2   # Bottom board display side
        self.right_board_side = screen_size[0]//2 + (self.box_size * self.column_count) / 2   # Right board display side

    # ------------------------------------------------------------------------------------------------------------------
    # Security methods

    # This method just return a boolean value that indicates if the position is inside the grid or not
    def overflow(self, x: int, y: int):
        return not (0 <= x <= self.column_count - 1 and 0 <= y <= self.row_count - 1)

    # This method just return a boolean value that indicates if the click is inside the display board
    def is_clicked(self, mouse_position: (float, float)):
        return self.top_board_side <= mouse_position[1] <= self.bottom_board_side and \
            self.left_board_side <= mouse_position[0] <= self.right_board_side

    # This method allows to copy the board without memory reference
    def copy_board(self, screen_size):
        board = Board(self.row_count, self.column_count, (89, 139, 44), screen_size)
        board.grid = np.copy(self.grid)
        return board

    # ------------------------------------------------------------------------------------------------------------------
    # Processing grid methods

    # This method allows us to determine the moves that are available in the next turn
    # and to save them in the attribute of the class (available_move : array)
    def is_there_valid_move(self, next_player_key: int, last_player_key: int):
        self.available_moves = []   # Reset the available moves from the previous turn
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.grid[row][col] == next_player_key:  # if a box is filled by the next player
                    for x_direction, y_direction in DIRECTIONS:    # Let's test in all the directions
                        x = row + x_direction
                        y = col + y_direction
                        if not self.overflow(x, y) and self.grid[x][y] == last_player_key:
                            x += x_direction
                            y += y_direction
                            while not self.overflow(x, y) and self.grid[x][y] == last_player_key:
                                x += x_direction
                                y += y_direction
                            if not self.overflow(x, y) and self.grid[x][y] == 0 and (x, y) not in self.available_moves:
                                # If this position allows the next player to convert the opponent's pieces
                                # and the position is on the grid, then it is a valid move. We save it
                                self.available_moves.append((x, y))

    # This method allows us to count the points of a specific player whose key we have passed in parameter
    def count_points(self, piece_key: int):
        s = 0  # s represents the amount of piece of his color that the player has on the board
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.grid[row][col] == piece_key:
                    s += 1
        return s

    # ------------------------------------------------------------------------------------------------------------------
    # Grid editing methods

    # After each move, this method is called to update the grid by flipping the necessary pieces
    # This function also return the number of pieces that have been flipped
    def update_grid(self, row_click: int, column_click: int, player_key: int):
        s = 0   # Represent the number of pieces that will be flipped
        if player_key == 1:
            other_key = 2
        else:
            other_key = 1
        for x_direction, y_direction in DIRECTIONS:  # Let's test in all the directions
            x = row_click + x_direction
            y = column_click + y_direction
            if not self.overflow(x, y) and self.grid[x][y] == other_key:
                x += x_direction
                y += y_direction
                while not self.overflow(x, y) and self.grid[x][y] == other_key:
                    x += x_direction
                    y += y_direction
                if not self.overflow(x, y) and self.grid[x][y] == player_key:
                    # If we find another piece of the same color after passing through pieces of a different colour
                    # Then we do the same path in backwards while flipping the pieces we find
                    # until we come back to the starting position
                    while x != row_click or y != column_click:
                        x -= x_direction
                        y -= y_direction
                        s += 1
                        self.grid[x][y] = player_key
        return s    # We return the number of pieces that we flipped

    # This method resets the logical grid of the board
    def reset_board(self):
        self.grid = np.zeros((self.row_count, self.column_count))

