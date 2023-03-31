import pygame
from button import Button
from board import Board
import webbrowser

RULES_URL = "https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english"

SCREEN_SIZE = (1000, 600)

GAME_STATES = {"LAUNCHING": 'launching',
               "PLAYING": 'playing',
               "ENDING": 'ending',
               "P1WON": "p1won",
               "P2WON": "p2won",
               "DRAW": "draw",
               "REVIEW": "review", }


def round_click_pos(x):  # This function convert a float into an integer by truncating at the unit
    if x < 1:
        x = 0
    elif x < 2:
        x = 1
    elif x < 3:
        x = 2
    elif x < 4:
        x = 3
    elif x < 5:
        x = 4
    elif x < 6:
        x = 5
    elif x < 7:
        x = 6
    else:
        x = 7
    return x


class Othello:  # Class representing the functioning of the game of Othello
    def __init__(self, row_count, column_count):
        # Game parameters
        # Players
        self.white_player = {"key": 1, "color": (255, 255, 255), "AI": False}
        self.black_player = {"key": 2, "color": (0, 0, 0), "AI": True}
        # Game state
        self.current_player = self.white_player["key"]  # White player always starts
        self.game_state = GAME_STATES["LAUNCHING"]
        self.ai_start = False

        # Buttons
        # Launching buttons
        self.black_button = Button(184, 245, 352, 286)
        self.white_button = Button(714, 248, 357, 820)
        # Playing buttons
        self.reset_button = Button(13, 456, 518, 198)
        self.rules_button = Button(790, 457, 516, 973)
        # Ending buttons
        self.review_button = Button(13, 528, 586, 198)

        # Creating board
        self.row_count = row_count
        self.column_count = column_count
        self.board = Board(self.row_count, self.column_count, (89, 139, 44), SCREEN_SIZE)

        # Initialisation of the game
        # Creation of the screen
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Abalone')
        # Launching of the game
        self.update_background(screen)
        self.launching_othello(screen)

    # This method updates game's background using the global state of the game
    def update_background(self, screen: pygame.Surface):
        fond = pygame.image.load(f'assets/{self.game_state}_background.png')
        fond = fond.convert()
        screen.blit(fond, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    # This method launches Othello and lets the user choose who starts
    def launching_othello(self, screen: pygame.Surface):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to start the game and choose his color
                    mouse_position = event.pos
                    if self.black_button.is_clicked(mouse_position):  # User chooses black, so AI is white and starts
                        self.white_player['AI'] = True
                        self.ai_start = True
                        self.black_player['AI'] = False
                    if self.white_button.is_clicked(mouse_position):  # User chooses white, so he starts
                        self.white_player['AI'] = False
                        self.ai_start = False
                        self.black_player['AI'] = True
                    self.game_state = GAME_STATES["PLAYING"]
                    self.playing_othello(screen)  # Now start Othello

    # This method represents the main process of the Othello game
    def playing_othello(self, screen: pygame.Surface):
        self.init_game_background(screen)
        self.display_available_move(screen, self.black_player["key"])

        if self.ai_start:  # In case the user has chosen black, let's play with AI first
            self.board.is_there_valid_move(self.white_player["key"], self.black_player["key"])
            self.play_AI()
            self.update_board_display(screen)
            self.display_available_move(screen, self.current_player)
            self.next_turn(screen)
            pygame.time.wait(500)
            pygame.display.update()

        while True:  # Global loop for the game's process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos  # Click position
                    if self.rules_button.is_clicked(mouse_position):  # If user decides to see the rules of the game
                        webbrowser.open(RULES_URL)   # Let's open the official website of Othello's rules
                    if self.reset_button.is_clicked(mouse_position):  # If user decides to reset the game
                        self.reset_game(screen)
                    if self.board.is_clicked(mouse_position):  # Check If the click is inside the board
                        if self.play_user(mouse_position, screen):  # Play if the move is allowed
                            self.display_available_move(screen, self.current_player)
                            self.next_turn(screen)
                            if not self.board.available_moves:  # If there are no available move anymore, game ends
                                self.game_state = GAME_STATES["ENDING"]
                                self.ending_othello(screen)
                            pygame.display.update()  # Updating screen display because AI has to play
                            pygame.time.wait(500)
                            if self.play_AI():  # AI playing process, using minimax algorithm
                                self.display_available_move(screen, self.current_player)
                                self.update_board_display(screen)
                                self.next_turn(screen)
                            else:
                                print("BUG SYSTEME")
                            if not self.board.available_moves:  # If there are no available move anymore, game ends
                                self.game_state = GAME_STATES["ENDING"]
                                self.ending_othello(screen)
                pygame.display.update()

    # This method resets the game and brings back to the launching page
    def reset_game(self, screen: pygame.Surface):
        self.current_player = self.white_player["key"]  # White always starts
        self.game_state = GAME_STATES["LAUNCHING"]
        self.update_background(screen)
        self.board = Board(self.row_count, self.column_count, (89, 139, 44), SCREEN_SIZE)  # New board
        self.launching_othello(screen)

    # This method ends the game, calculates who won and brings to the ending page
    def ending_othello(self, screen: pygame.Surface):
        white_player_score = self.board.count_points(self.white_player["key"])
        black_player_score = self.board.count_points(self.black_player["key"])
        if white_player_score > black_player_score:  # Calculate if white player won
            self.game_state = GAME_STATES["P1WON"]
        elif white_player_score < black_player_score:  # Calculate if black player won
            self.game_state = GAME_STATES["P2WON"]
        else:  # Calculate if nobody won because of a draw
            self.game_state = GAME_STATES["DRAW"]
        self.update_background(screen)  # Updating to the good ending page depending on the result of the game
        while True:  # Ending game process, allowing the user to review or to reset the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos
                    if self.reset_button.is_clicked(mouse_position):  # If reset button is clicked, reset the game
                        self.reset_game(screen)
                    elif self.review_button.is_clicked(mouse_position):  # If review button is clicked, review the game
                        self.review_game(screen)

    # This method allows the user to review the previous game, and then to reset it
    def review_game(self, screen: pygame.Surface):
        winner = self.game_state
        self.game_state = GAME_STATES["REVIEW"]
        self.update_background(screen)
        self.display_user_color(screen)
        self.draw_grid(screen)
        self.update_board_display(screen)
        if winner == 'p1won':  # Show who won
            pygame.draw.circle(screen, self.white_player["color"],
                               (105,
                                150),
                               self.board.radius * 2)
        elif 'p2won':  # Show who won
            pygame.draw.circle(screen, self.black_player["color"],
                               (105,
                                150),
                               self.board.radius * 2)
        pygame.display.update()

    # This method shows all the available moves of the board with little grey circles
    def display_available_move(self, screen: pygame.Surface, last_player_key: int):
        # Generating other_coin_key
        if last_player_key == 1:
            next_player_key = 2
        else:
            next_player_key = 1

        # Deleting older display
        self.reset_available_moves(screen)

        # Testing all the bord
        self.board.is_there_valid_move(next_player_key, last_player_key)

        # Drawing available moves
        for (row, col) in self.board.available_moves:
            self.draw_circle(col, row, screen, (200, 200, 200), self.board.radius // 2)

    # This method deletes all the little circles of available moves that we created before
    def reset_available_moves(self, screen: pygame.Surface):
        for row, col in self.board.available_moves:
            if self.board.grid[row][col] == 0:
                self.draw_circle(col, row, screen, self.board.color, self.board.radius)
        self.board.available_moves = []    # Then, we delete all the current available moves

    # This method update the board while creating circle of the good color
    def update_board_display(self, screen: pygame.Surface):
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.board.grid[row][col] == 1:
                    self.draw_circle(col, row, screen, self.white_player["color"], self.board.radius)
                elif self.board.grid[row][col] == 2:
                    self.draw_circle(col, row, screen, self.black_player["color"], self.board.radius)

    def draw_circle(self, col: int, row: int, screen: pygame.Surface, color: (int, int, int), radius: int):
        pygame.draw.circle(screen, color,
                           (self.board.left_board_side + col * self.board.box_size * 1.03 + self.board.box_size // 2,
                            self.board.top_board_side + self.board.box_size * row * 1.03 + self.board.box_size // 2),
                           radius)

    def play_AI(self):
        if self.current_player == 1:
            other_player = self.black_player["key"]
        else:
            other_player = self.white_player["key"]
        best_move = [-1, -1]
        max_point = float('-inf')
        for move in self.board.available_moves:
            temp_board = self.board.copy_board(SCREEN_SIZE)
            print(move)
            temp_board.grid[move[0]][move[1]] = self.current_player
            turned_coin = temp_board.update_grid(move[0], move[1], self.current_player)
            temp_board.is_there_valid_move(other_player, self.current_player)
            move_points = self.minimax(temp_board, other_player, 0, False, turned_coin)
            if move_points > max_point:
                max_point = move_points
                best_move = move
        if best_move != [-1, -1]:
            print("move chosed : ", best_move, max_point)
            self.board.grid[best_move[0]][best_move[1]] = self.current_player
            self.board.update_grid(best_move[0], best_move[1], self.current_player)
            return True
        return False

    def minimax(self, board: Board, player: int, depth: int, maximizing_player: int, turned_coin: int):
        if player == 1:
            other_player = self.black_player["key"]
        else:
            other_player = self.white_player["key"]

        if depth == 0 or board.available_moves == []:
            total = 0
            for row in range(board.row_count):
                for col in range(board.column_count):
                    if board.grid[row][col] == player:
                        total += board.grid[row][col] * board.square_weight[row][col]
            return total + 2 * turned_coin

        if maximizing_player:
            best_value = float('-inf')
            for move in board.available_moves:
                temp_board = board.copy_board()
                temp_board.grid[move[0]][move[1]] = player
                turned_coin = temp_board.update_grid(move[0], move[1], player)
                temp_board.is_there_valid_move(other_player, player)
                value = self.minimax(temp_board, other_player, depth - 1, False, turned_coin)
                best_value = max(best_value, value)
        else:
            best_value = float('inf')
            for move in board.available_moves:
                temp_board = board.copy_board()
                temp_board.grid[move[0]][move[1]] = player
                turned_coin = temp_board.update_grid(move[0], move[1], player)
                temp_board.is_there_valid_move(other_player, player)
                value = self.minimax(temp_board, other_player, depth - 1, True, turned_coin)
                print(value)
                best_value = min(best_value, value)
        return best_value

    def play_user(self, mouse_position: (float, float), screen: pygame.Surface):
        column_click = (mouse_position[0] - self.board.left_board_side) / self.board.box_size / 1.03
        column_click = round_click_pos(column_click)
        row_click = (mouse_position[1] - self.board.top_board_side) / self.board.box_size / 1.03
        row_click = round_click_pos(row_click)
        if (row_click, column_click) in self.board.available_moves:
            self.board.grid[row_click][column_click] = self.current_player
            self.board.update_grid(row_click, column_click, self.current_player)
            self.update_board_display(screen)
            return True
        return False

    def next_turn(self, screen: pygame.Surface):
        if self.current_player == 1:
            self.current_player = self.black_player["key"]
        else:
            self.current_player = self.white_player["key"]
        self.change_player_indicator(screen)

    def change_player_indicator(self, screen: pygame.Surface):
        if self.current_player == 1:
            pygame.draw.circle(screen, self.white_player["color"],
                               (105,
                                150),
                               self.board.radius * 2)
        else:
            pygame.draw.circle(screen, self.black_player["color"],
                               (105,
                                150),
                               self.board.radius * 2)

    def init_game_background(self, screen: pygame.Surface):
        self.update_background(screen)
        self.display_user_color(screen)
        self.board.grid[3][3] = 1
        self.board.grid[4][4] = 1
        self.board.grid[4][3] = 2
        self.board.grid[3][4] = 2
        self.draw_grid(screen)
        self.draw_circle(3, 3, screen, self.white_player["color"], self.board.radius)
        self.draw_circle(4, 4, screen, self.white_player["color"], self.board.radius)
        self.draw_circle(4, 3, screen, self.black_player["color"], self.board.radius)
        self.draw_circle(3, 4, screen, self.black_player["color"], self.board.radius)
        self.change_player_indicator(screen)
        pygame.display.update()

    def display_user_color(self, screen: pygame.Surface):
        if not self.white_player['AI']:
            pygame.draw.circle(screen, self.white_player["color"],
                               (105,
                                330),
                               self.board.radius * 2)
        else:
            pygame.draw.circle(screen, self.black_player["color"],
                               (105,
                                330),
                               self.board.radius * 2)

    def draw_grid(self, screen: pygame.Surface):
        for column in range(self.column_count):
            for row in range(self.row_count):
                pygame.draw.rect(screen, self.board.color,
                                 (self.board.left_board_side + column * self.board.box_size * 1.03,
                                  self.board.top_board_side + self.board.box_size * row * 1.03,
                                  self.board.box_size,
                                  self.board.box_size))
