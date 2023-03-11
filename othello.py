import numpy as np
import pygame
from button import Button
from board import Board

GAME_STATES = {"LAUNCHING": 'launching',
               "PLAYING": 'playing',
               "ENDING": 'ending',
               "P1WON": "p1won",
               "P2WON": "p2won",
               "DRAW": "draw",
               "REVIEW": "review", }


def round_click_pos(click):
    if click < 1:
        click = 0
    elif click < 2:
        click = 1
    elif click < 3:
        click = 2
    elif click < 4:
        click = 3
    elif click < 5:
        click = 4
    elif click < 6:
        click = 5
    elif click < 7:
        click = 6
    else:
        click = 7
    return click


class Othello:
    def __init__(self, row_count, column_count):
        # Game parameters
        self.player_1 = {"key": 1, "color": (255, 255, 255), "AI": False}
        self.player_2 = {"key": 2, "color": (0, 0, 0), "AI": True}
        self.current_player = self.player_1["key"]
        self.game_state = GAME_STATES["LAUNCHING"]

        # Buttons
        # Launching buttons
        self.black_button = Button(184, 245, 352, 286)
        self.white_button = Button(714, 248, 357, 820)
        # Playing buttons
        self.reset_button = Button(13, 456, 518, 198)
        # Ending buttons
        self.review_button = Button(13, 528, 586, 198)

        # Creating board
        self.row_count = row_count
        self.column_count = column_count
        self.board = Board(self.row_count, self.column_count, (89, 139, 44))

        # Initialisation of the game
        pygame.init()
        screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Abalone')
        self.launching_othello(screen)

    def launching_othello(self, screen):
        self.update_background(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos
                    if self.black_button.is_clicked(mouse_position):
                        self.player_1['AI'] = True
                        self.player_2['AI'] = False
                        self.game_state = GAME_STATES["PLAYING"]
                        self.playing_othello(screen)
                    if self.white_button.is_clicked(mouse_position):
                        self.player_1['AI'] = False
                        self.player_2['AI'] = True
                        self.game_state = GAME_STATES["PLAYING"]
                        self.playing_othello(screen)

    def update_background(self, screen):
        fond = pygame.image.load(f'assets/{self.game_state}_background.png')
        fond = fond.convert()
        screen.blit(fond, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def playing_othello(self, screen):
        self.init_game_background(screen)
        self.display_available_move(screen, self.current_player)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos
                    # Check If the click is inside the board
                    if self.reset_button.is_clicked(mouse_position):
                        self.reset_game(screen)
                    if self.board.is_clicked(mouse_position):
                        self.play_once(mouse_position, screen)  # Playing process
                        self.display_available_move(screen, self.current_player)
                        if not self.board.available_moves:
                            self.game_state = GAME_STATES["ENDING"]
                            self.ending_othello(screen)
                    """if self.current_player == 1 and not self.player_1["AI"]:
                        mouse_position = event.pos
                        # Check If the click is inside the board
                        if self.is_valid_click(mouse_position):
                            self.play_once(mouse_position, screen)  # Playing process
                            self.display_available_move(screen, self.current_player)
                            if not self.board.available_moves:
                                self.game_state = GAME_STATES["ENDING"]
                                self.ending_othello(screen)
                    else:
                        print("WAIT, NOW IT IS AI TURN")"""
                pygame.display.update()

    def reset_game(self, screen):
        self.game_state = GAME_STATES["LAUNCHING"]
        self.board = Board(self.row_count, self.column_count, (89, 139, 44))
        self.launching_othello(screen)

    def ending_othello(self, screen):
        p1_sum = 0
        p2_sum = 0
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.board.grid[row][col] == 1:
                    p1_sum += 1
                elif self.board.grid[row][col] == 2:
                    p2_sum += 1
        if p1_sum > p2_sum:
            self.game_state = GAME_STATES["P1WON"]
        elif p1_sum < p2_sum:
            self.game_state = GAME_STATES["P2WON"]
        else:
            self.game_state = GAME_STATES["DRAW"]
        self.update_background(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Click are used to play and place your coin
                    mouse_position = event.pos
                    if self.reset_button.is_clicked(mouse_position):
                        self.reset_game(screen)
                    elif self.review_button.is_clicked(mouse_position):
                        self.review_game(screen)

    def review_game(self, screen):
        winner = self.game_state
        self.game_state = GAME_STATES["REVIEW"]
        self.update_background(screen)
        self.display_user_color(screen)
        self.draw_grid(screen)
        self.update_color_board(screen)
        if winner == 'p1won':
            pygame.draw.circle(screen, self.player_1["color"],
                               (105,
                                150),
                               self.board.radius * 2)
        elif 'p2won':
            pygame.draw.circle(screen, self.player_2["color"],
                               (105,
                                150),
                               self.board.radius * 2)
        pygame.display.update()

    def display_available_move(self, screen, next_player_key):
        # Generating other_coin_key
        if next_player_key == 1:
            last_player_key = 2
        else:
            last_player_key = 1

        # Deleting older display
        self.reset_available_moves(screen)

        # Testing all the bord
        for row in range(self.row_count):
            for col in range(self.column_count):
                self.board.is_there_valid_move(row, col, next_player_key, last_player_key)

        # Drawing available moves
        for (row, col) in self.board.available_moves:
            pygame.draw.circle(screen, (200, 200, 200),
                               (
                               self.board.left_board_side + col * self.board.box_size * 1.03 + self.board.box_size // 2,
                               self.board.top_board_side + self.board.box_size * row * 1.03 + self.board.box_size // 2),
                               self.board.radius // 2)

    def reset_available_moves(self, screen):
        for row, col in self.board.available_moves:
            if self.board.grid[row][col] == 0:
                self.draw_circle(col, row, screen, self.board.color)
        self.board.available_moves = []

    def update_color_board(self, screen):
        for row in range(self.row_count):
            for col in range(self.column_count):
                if self.board.grid[row][col] == 1:
                    self.draw_circle(col, row, screen, self.player_1["color"])
                elif self.board.grid[row][col] == 2:
                    self.draw_circle(col, row, screen, self.player_2["color"])

    def draw_circle(self, col, row, screen, color):
        pygame.draw.circle(screen, color,
                           (self.board.left_board_side + col * self.board.box_size * 1.03 + self.board.box_size // 2,
                            self.board.top_board_side + self.board.box_size * row * 1.03 + self.board.box_size // 2),
                           self.board.radius)

    def play_once(self, mouse_position, screen):
        column_click = (mouse_position[0] - self.board.left_board_side) / self.board.box_size / 1.03
        column_click = round_click_pos(column_click)
        row_click = (mouse_position[1] - self.board.top_board_side) / self.board.box_size / 1.03
        row_click = round_click_pos(row_click)
        if self.board.grid[row_click][column_click] == 0:
            self.board.grid[row_click][column_click] = self.current_player
            if self.board.update_grid(row_click, column_click, self.current_player):
                self.update_color_board(screen)
                if self.current_player == 1:
                    self.current_player = self.player_2["key"]
                else:
                    self.current_player = self.player_1["key"]
                self.change_player_indicator(screen)
            else:
                self.board.grid[row_click][column_click] = 0

    def change_player_indicator(self, screen):
        if self.current_player == 1:
            pygame.draw.circle(screen, self.player_1["color"],
                               (105,
                                150),
                               self.board.radius * 2)
        else:
            pygame.draw.circle(screen, self.player_2["color"],
                               (105,
                                150),
                               self.board.radius * 2)

    def init_game_background(self, screen):
        self.update_background(screen)
        self.display_user_color(screen)
        self.board.grid[3][3] = 1
        self.board.grid[4][4] = 1
        self.board.grid[4][3] = 2
        self.board.grid[3][4] = 2
        self.draw_grid(screen)
        self.draw_circle(3, 3, screen, self.player_1["color"])
        self.draw_circle(4, 4, screen, self.player_1["color"])
        self.draw_circle(4, 3, screen, self.player_2["color"])
        self.draw_circle(3, 4, screen, self.player_2["color"])
        self.change_player_indicator(screen)
        pygame.display.update()

    def display_user_color(self, screen):
        if not self.player_1['AI']:
            pygame.draw.circle(screen, self.player_1["color"],
                               (105,
                                330),
                               self.board.radius * 2)
        else:
            pygame.draw.circle(screen, self.player_2["color"],
                               (105,
                                330),
                               self.board.radius * 2)

    def draw_grid(self, screen):
        for column in range(self.column_count):
            for row in range(self.row_count):
                pygame.draw.rect(screen, self.board.color,
                                 (self.board.left_board_side + column * self.board.box_size * 1.03,
                                  self.board.top_board_side + self.board.box_size * row * 1.03,
                                  self.board.box_size,
                                  self.board.box_size))
