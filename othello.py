import pygame
from button import Button
from board import Board
import webbrowser
import sys

RULES_URL = "https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english"

SCREEN_SIZE = (1000, 600)

GAME_STATES = {"LAUNCHING": 'launching',
               "PLAYING": 'playing',
               "ENDING": 'ending',
               "P1WON": "p1won",
               "P2WON": "p2won",
               "DRAW": "draw",
               "REVIEW": "review", }


class Othello:  # Class representing the functioning of the game of Othello
    def __init__(self, row_count, column_count):
        # Game parameters
        # Players
        self.players = {
            "white_player": {"key": 1, "color": (255, 255, 255), "AI": False},
            "black_player": {"key": 2, "color": (0, 0, 0), "AI": True},
        }
        # Game state
        self.current_player = self.players["black_player"]["key"]  # Black player always starts
        self.game_state = GAME_STATES["LAUNCHING"]
        self.ai_start = False
        self.difficulty = 1   # Default difficulty is easy (1 = easy, 2 = medium, 3 = hard)

        # Buttons
        self.buttons = {
            # Launching buttons
            "black_button" : Button(184, 245, 352, 286),
            "white_button" : Button(714, 248, 357, 820),
            # Playing buttons
            "reset_button" : Button(14, 456, 518, 196),
            "rules_button" : Button(790, 457, 516, 973),
            # Ending buttons
            "review_button" : Button(14, 528, 586, 196),
            # Difficulty button
            "easy_diff_button" : Button(14, 387, 445, 69),
            "medium_diff_button" : Button(77, 387, 445, 133),
            "hard_diff_button" : Button(140, 387, 445, 196),
        }

        # Creating board
        self.row_count = row_count
        self.column_count = column_count
        self.board = Board(self.row_count, self.column_count, (89, 139, 44), SCREEN_SIZE)

        # Initialisation of the game
        # Creation of the screen
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)
        pygame.display.set_caption('Abalone')
        # Launching of the game
        self.update_background(screen)
        self.launching_othello(screen)

    # ------------------------------------------------------------------------------------------------------------------
    # Gaming process methods

    # This method launches Othello and lets the user choose who starts
    def launching_othello(self, screen: pygame.Surface):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to start the game and choose his color
                    mouse_position = event.pos
                    if self.buttons["black_button"].is_clicked(mouse_position):  # User chooses black, he starts
                        self.players["white_player"]["AI"] = True
                        self.ai_start = False
                        self.players["black_player"]["AI"] = False
                        self.game_state = GAME_STATES["PLAYING"]
                        self.playing_othello(screen)  # Now start Othello
                    if self.buttons["white_button"].is_clicked(mouse_position):  # User chooses white, AI starts
                        self.players["white_player"]["AI"] = False
                        self.ai_start = True
                        self.players["black_player"]["AI"] = True
                        self.game_state = GAME_STATES["PLAYING"]
                        self.playing_othello(screen)  # Now start Othello


    # This method represents the main process of the Othello game
    def playing_othello(self, screen: pygame.Surface):
        self.init_game_background(screen)
        self.display_available_move(screen, self.players["white_player"]["key"])
        if self.ai_start:  # In case the user has chosen white, let's play with AI first
            self.board.is_there_valid_move(self.players["black_player"]["key"], self.players["white_player"]["key"])
            self.AI_turn(screen)


        while True:  # Global loop for the game's process
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos  # Click position
                    #print(mouse_position)
                    if self.buttons["rules_button"].is_clicked(mouse_position):  # Let's show the rules of the game
                        webbrowser.open(RULES_URL)  # Let's open the official website of Othello's rules
                    elif self.buttons["reset_button"].is_clicked(mouse_position):  # If user decides to reset the game
                        self.reset_game(screen)
                    elif self.buttons["easy_diff_button"].is_clicked(mouse_position):  # Difficulty changes to easy
                        self.difficulty = 1
                    elif self.buttons["medium_diff_button"].is_clicked(mouse_position):  # Difficulty changes to medium
                        self.difficulty = 2
                    elif self.buttons["hard_diff_button"].is_clicked(mouse_position):  # Difficulty changes to hard
                        self.difficulty = 3
                    elif self.board.is_clicked(mouse_position):  # Check If the click is inside the board
                        if self.play_user(mouse_position, screen):  # Play if the move is allowed
                            self.display_available_move(screen, self.current_player)
                            self.next_turn(screen)
                            self.show_score(screen)
                            self.is_game_ended(screen)
                            pygame.display.update()  # Updating screen display because AI has to play
                            self.AI_turn(screen)    # AI turn process
                            self.is_game_ended(screen)
                pygame.display.update()

    # This method is the main user turn process. We manage a verification process and the modification of the board
    def play_user(self, mouse_position: (float, float), screen: pygame.Surface):
        column_click, row_click = self.convert_click_to_position(mouse_position)  # We convert the click in a position
        if (row_click, column_click) in self.board.available_moves:  # If the move is available
            self.board.grid[row_click][column_click] = self.current_player
            self.board.update_grid(row_click, column_click, self.current_player)
            self.update_board_display(screen)
            return True  # Move done with success
        return False  # Move invalid

    # This method ends the game, calculates who won and brings to the ending page
    def ending_othello(self, screen: pygame.Surface):
        white_player_score = self.board.count_points(self.players["white_player"]["key"])
        black_player_score = self.board.count_points(self.players["black_player"]["key"])
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
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos
                    if self.buttons["reset_button"].is_clicked(mouse_position):  # Reset the game
                        self.reset_game(screen)
                    elif self.buttons["review_button"].is_clicked(mouse_position):  # Review the game
                        self.review_game(screen)

    # ------------------------------------------------------------------------------------------------------------------
    # AI implementation methods

    # This method manages the AI turn process
    def AI_turn(self, screen):
        pygame.time.wait(500)
        self.play_AI()  # AI playing process, using minimax algorithm
        self.display_available_move(screen, self.current_player)
        self.update_board_display(screen)
        self.next_turn(screen)
        self.show_score(screen)
        pygame.display.update()

    # This method is the main AI turn process. We manage the selection of the move and the modification of the board
    def play_AI(self):
        if self.current_player == self.players["white_player"]["key"]:
            other_player = self.players["black_player"]["key"]
        else:
            other_player = self.players["white_player"]["key"]
        best_move = [-1, -1]  # Default best move, allow us to know if the minimax algorithm doesn't work
        max_point = float('-inf')  # Represent the points of the best found move
        for move in self.board.available_moves:
            temp_board = self.board.copy_board(SCREEN_SIZE)  # We copy the board because we want to simulate moves
            temp_board.grid[move[0]][move[1]] = self.current_player  # Simulation of one of the available move
            flipped_coin = temp_board.update_grid(move[0], move[1], self.current_player)  # How many coin did it flipped
            temp_board.is_there_valid_move(other_player, self.current_player)  # Updating of the new available moves
            move_points = self.minimax(temp_board, other_player, False, flipped_coin, depth=self.difficulty)
            if move_points > max_point:
                max_point = move_points  # Then this move is currently the best that we found, we save it
                best_move = move
        if best_move != [-1, -1]:  # If we have found a move
            self.board.grid[best_move[0]][best_move[1]] = self.current_player  # Modification of the board
            self.board.update_grid(best_move[0], best_move[1], self.current_player)  # Updating of the board
            return True
        return False  # Not any move has been found

    # Implementation of the minimax algorithm for Othello game
    def minimax(self, board: Board, player: int, maximizing_player: int, turned_coin: int, depth: int):
        if player == self.players["white_player"]["key"]:  # Define the opponent key
            other_player = self.players["black_player"]["key"]
        else:
            other_player = self.players["white_player"]["key"]

        if depth == 0 or board.available_moves == []:  # If we have a leaf node or the maximum depth is reached
            total = self.evaluate_board(board, player, turned_coin)  # We evaluate the board with the heuristic method
            return total  # We return the heuristic evaluation of the board

        if maximizing_player:  # If we are with the maximizing player
            best_value = float('-inf')  # We want to find the best node in the possible moves of this board
            for move in board.available_moves:  # We process all the possible moves
                temp_board = board.copy_board(SCREEN_SIZE)  # We copy the board because we want to simulate the move
                temp_board.grid[move[0]][move[1]] = player  # Simulation of the move
                turned_coin = temp_board.update_grid(move[0], move[1], player)  # How many coin did it flipped
                temp_board.is_there_valid_move(other_player, player)  # Update of the new available moves
                value = self.minimax(temp_board, other_player, False, turned_coin, depth - 1)  # Minimax process
                best_value = max(best_value, value)  # Is the value of this node the best value that we found
        else:  # If we are with the minimizing player
            best_value = float('+inf')  # We want to find the worth node in the possible moves of this board
            for move in board.available_moves:  # We process all the possible moves
                temp_board = board.copy_board(SCREEN_SIZE)  # We copy the board because we want to simulate the move
                temp_board.grid[move[0]][move[1]] = player  # Simulation of the move
                turned_coin = temp_board.update_grid(move[0], move[1], player)  # How many coin did it flipped
                temp_board.is_there_valid_move(other_player, player)  # Update the new available moves
                value = self.minimax(temp_board, other_player, True, turned_coin, depth - 1)  # Minimax process
                best_value = min(best_value, value)  # Is the value of this node the worth value that we found
        return best_value  # We return the best/worth (maximizing/minimazing player) node for this move

    # ------------------------------------------------------------------------------------------------------------------
    # Control and interruption methods

    # This method tests if the game is ended
    def is_game_ended(self, screen):
        if not self.board.available_moves:  # If there are no available move anymore, game ends
            self.game_state = GAME_STATES["ENDING"]
            self.ending_othello(screen)

    # This method resets the game and brings back to the launching page
    def reset_game(self, screen: pygame.Surface):
        self.current_player = self.players["black_player"]["key"]  # White always starts
        self.game_state = GAME_STATES["LAUNCHING"]
        self.update_background(screen)
        self.board = Board(self.row_count, self.column_count, (89, 139, 44), SCREEN_SIZE)  # New board
        self.launching_othello(screen)

    # This method allows the user to review the previous game, and then to reset it
    def review_game(self, screen: pygame.Surface):
        winner = self.game_state
        self.game_state = GAME_STATES["REVIEW"]
        self.update_background(screen)
        self.display_user_color(screen)
        self.draw_grid(screen)
        self.update_board_display(screen)
        self.show_score(screen)
        if winner == 'p1won':  # Show who won
            pygame.draw.circle(screen, self.players["white_player"]["color"],
                               (105,
                                117),
                               self.board.radius * 1.25)
        elif 'p2won':  # Show who won
            pygame.draw.circle(screen, self.players["black_player"]["color"],
                               (105,
                                117),
                               self.board.radius * 1.25)
        pygame.display.update()

    # This method manage the end of a turn and switch the current player
    def next_turn(self, screen: pygame.Surface):
        if self.current_player == self.players["white_player"]["key"]:
            self.current_player = self.players["black_player"]["key"]
        else:
            self.current_player = self.players["white_player"]["key"]
        self.change_player_indicator(screen)  # We change the player indicator that it displays on the screen

    # ------------------------------------------------------------------------------------------------------------------
    # Display methods

    # This method is called at the beginning of the playing part of the game in order to create the displayed board
    def init_game_background(self, screen: pygame.Surface):
        self.update_background(screen)  # Updating the background
        self.display_user_color(screen)  # Show the user main color to remind it to him
        self.board.grid[3][3] = self.players["white_player"]["key"]  # Place the starting pieces
        self.board.grid[4][4] = self.players["white_player"]["key"]  # Place the starting pieces
        self.board.grid[4][3] = self.players["black_player"]["key"]  # Place the starting pieces
        self.board.grid[3][4] = self.players["black_player"]["key"]  # Place the starting pieces
        self.draw_grid(screen)  # Draw the grid on the screen
        # This section has the same goal as self.update_board_display. However, we don't have to analyse all the grid
        self.draw_circle(3, 3, screen, self.players["white_player"]["color"], self.board.radius)
        self.draw_circle(4, 4, screen, self.players["white_player"]["color"], self.board.radius)
        self.draw_circle(4, 3, screen, self.players["black_player"]["color"], self.board.radius)
        self.draw_circle(3, 4, screen, self.players["black_player"]["color"], self.board.radius)
        self.change_player_indicator(screen)  # Let's build the player display indicator
        pygame.display.update()

    # This method changes the player indicator circle that it display on the top right of the screen
    def change_player_indicator(self, screen: pygame.Surface):
        if self.current_player == self.players["white_player"]["key"]:  # If the current player is the white player
            pygame.draw.circle(screen, self.players["white_player"]["color"],
                               (105,
                                117),
                               self.board.radius * 1.25)
        else:  # If the current player is the black player
            pygame.draw.circle(screen, self.players["black_player"]["color"],
                               (105,
                                117),
                               self.board.radius * 1.25)

    # This method displays the user color on the right part of the board in order to remind it to him during the game
    def display_user_color(self, screen: pygame.Surface):
        if not self.players["white_player"]['AI']:  # If the player is the white player
            pygame.draw.circle(screen, self.players["white_player"]["color"],
                               (105,
                                210),
                               self.board.radius * 1.25)
        else:  # If the player is the black player
            pygame.draw.circle(screen, self.players["black_player"]["color"],
                               (105,
                                210),
                               self.board.radius * 1.25)

    # This method draws the green grid on the board with a sequence of green rectangle
    def draw_grid(self, screen: pygame.Surface):
        for column in range(self.column_count):
            for row in range(self.row_count):
                pygame.draw.rect(screen, self.board.color,
                                 (self.board.left_board_side + column * self.board.box_size * 1.03,
                                  self.board.top_board_side + self.board.box_size * row * 1.03,
                                  self.board.box_size,
                                  self.board.box_size))

    # This method shows all the available moves of the board with little grey circles
    def display_available_move(self, screen: pygame.Surface, last_player_key: int):
        # Generating other_coin_key
        if last_player_key == self.players["black_player"]["key"]:
            next_player_key = self.players["white_player"]["key"]
        else:
            next_player_key = self.players["black_player"]["key"]

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
        self.board.available_moves = []  # Then, we delete all the current available moves

    # This method update the board while creating circle of the good color
    def update_board_display(self, screen: pygame.Surface):
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.board.grid[row][col] == self.players["white_player"]["key"]:
                    self.draw_circle(col, row, screen, self.players["white_player"]["color"], self.board.radius)
                elif self.board.grid[row][col] == self.players["black_player"]["key"]:
                    self.draw_circle(col, row, screen, self.players["black_player"]["color"], self.board.radius)

    # This method shows the score of the game on the left part of the screen
    def show_score(self, screen):
        pygame.draw.rect(screen, (198, 184, 168), (48, 285, 50, 50))    # Use to erase last score display
        pygame.draw.rect(screen, (198, 184, 168), (125, 285, 50, 50))   # Use to erase last score display
        white_score = self.font.render(
            str(self.board.count_points(self.players["white_player"]["key"])),
            True,
            (255, 255, 255)
        )
        black_score = self.font.render(
            str(self.board.count_points(self.players["black_player"]["key"])),
            True,
            (0, 0, 0)
        )
        screen.blit(white_score, (50, 285))
        screen.blit(black_score, (125, 285))

    # This method updates game's background using the global state of the game
    def update_background(self, screen: pygame.Surface):
        fond = pygame.image.load(f'assets/{self.game_state}_background.png')
        fond = fond.convert()
        screen.blit(fond, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    # ------------------------------------------------------------------------------------------------------------------
    # Tool methods

    # This method is a shortcut to draw a circle at a specific (row, column) quickly
    def draw_circle(self, col: int, row: int, screen: pygame.Surface, color: (int, int, int), radius: int):
        pygame.draw.circle(screen, color,
                           (self.board.left_board_side + col * self.board.box_size * 1.03 + self.board.box_size // 2,
                            self.board.top_board_side + self.board.box_size * row * 1.03 + self.board.box_size // 2),
                           radius)

    # This method convert a click in a tuple integer that represent the position of the click in the grid
    def convert_click_to_position(self, mouse_position: (float, float)):
        column_click = (mouse_position[0] - self.board.left_board_side) / self.board.box_size / 1.03
        column_click = self.round_click_pos(column_click)
        row_click = (mouse_position[1] - self.board.top_board_side) / self.board.box_size / 1.03
        row_click = self.round_click_pos(row_click)
        return column_click, row_click

    def round_click_pos(self, x):  # This function convert a float into an integer by truncating at the unit
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

    # This method is a heuristic evaluation method that allow us to put a score for a specific grid
    def evaluate_board(self, board, player, turned_coin):
        total = 0
        for row in range(board.row_count):
            for col in range(board.column_count):
                if board.grid[row][col] == player:
                    total += board.grid[row][col] * board.square_weight[row][col]
        return total + 1.5 * turned_coin