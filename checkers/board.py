from collections import defaultdict
import pygame
from checkers.piece import Piece
from checkers.constants import *
import copy


class CaptureMovesDict:
    def __init__(self):
        self.data = defaultdict(list)

    def add(self, key, value_or_list):
        if isinstance(value_or_list, list):
            self.data[key].extend(value_or_list)
        else:
            self.data[key].append(value_or_list)

    def get(self, key):
        return self.data[key]

    def keys(self):
        return list(self.data.keys())

    def __add__(self, other):
        if not isinstance(other, CaptureMovesDict):
            raise ValueError("Can only add another MultiKeyDict instance")

        new_dict = CaptureMovesDict()

        # Add elements from the first dictionary
        for key, values in self.data.items():
            for value in values:
                new_dict.add(key, value)

        # Add elements from the second dictionary
        for key, values in other.data.items():
            for value in values:
                new_dict.add(key, value)

        return new_dict

    def __iadd__(self, other):
        if not isinstance(other, CaptureMovesDict):
            raise ValueError("Can only add another MultiKeyDict instance")

        # Add elements from the other dictionary
        for key, values in other.data.items():
            for value in values:
                self.add(key, value)

        return self

    def __len__(self):
        return sum(len(values) for values in self.data.values())

    def __str__(self):
        return f"CaptureMovesDict: {dict(self.data)}"


class Board:
    def __init__(self):
        self.board = []
        self.create_board()
        self.valid_moves = set()
        self.capture_moves = CaptureMovesDict()
        self.selected_square = None
        self.last_board = copy.deepcopy(self.board)

    def get_piece(self, row, col):
        return self.board[row][col]

    def select_piece(self, row, col):
        self.selected_square = (row, col)

    def unselect_piece(self):
        self.selected_square = None
        self.valid_moves.clear()

    def draw_squares(self, screen):
        screen.fill(BLACK)
        for row in range(NUM_ROWS):
            for col in range(row % 2, NUM_COLS, 2):
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )
        if self.selected_square is not None:
            row, col = self.selected_square
            pygame.draw.rect(screen, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        for row, col in self.valid_moves:
            pygame.draw.rect(screen, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    def create_custom_board(self):
        for row in range(NUM_ROWS):
            self.board.append([])
            for col in range(NUM_COLS):
                self.board[row].append(None)
        self.board[3][3] = Piece(3, 3, BLUE)
        self.board[5][3] = Piece(5, 3, BLUE)
        self.board[3][5] = Piece(3, 5, BLUE)
        self.board[5][5] = Piece(5, 5, BLUE)
        self.board[6][4] = Piece(6, 4, RED)
        self.board[6][4].king = True

    def create_board(self):
        for row in range(NUM_ROWS):
            self.board.append([])
            for col in range(NUM_COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLUE))
                    else:
                        self.board[row].append(None)  # None for nothing no piece on this square
                else:
                    self.board[row].append(None)

    def draw(self, screen):
        # draw board squares
        self.draw_squares(screen)
        # draw pieces
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(screen)

    def get_valid_moves(self, row, col):
        # this function called after piece has been successfully selected
        piece = self.board[row][col]
        color = piece.color

        final_capture_moves = CaptureMovesDict()
        visited = set()

        # check if current piece has capture move
        def get_capture_moves(row, col, captured_squares):

            is_last_move = True

            # capture_moves = CaptureMovesDict()
            for index, (dr, dc) in enumerate(DIRS):
                if not piece.king:
                    if color is RED and index >= 2:
                        continue
                    if color is BLUE and index <= 1:
                        continue
                new_row_1 = row + dr
                new_col_1 = col + dc
                new_row_2 = row + 2 * dr
                new_col_2 = col + 2 * dc
                if 0 <= new_row_1 < len(self.board) and 0 <= new_col_1 < len(self.board[0]) and 0 <= new_row_2 < len(self.board) and 0 <= new_col_2 < len(self.board[0]):
                    capture_piece = self.board[new_row_1][new_col_1]
                    if capture_piece is not None and capture_piece.color != color and self.board[new_row_2][new_col_2] is None:
                        if (new_row_1, new_col_1) not in captured_squares:
                            captured_squares.append((new_row_1, new_col_1))
                            get_capture_moves(new_row_2, new_col_2, captured_squares)
                            is_last_move = False
                            captured_squares.pop()

            if is_last_move:
                final_capture_moves.add((row, col), captured_squares)
            return

        # temperoary remove current piece from board
        self.board[row][col] = None
        get_capture_moves(row, col, [])
        self.board[row][col] = piece
        if len(final_capture_moves) > 0:
            self.capture_moves = final_capture_moves
            self.valid_moves = final_capture_moves.keys()
            return

        # check if other pieces has capture move
        def has_capture_moves():
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    if self.board[row][col] is not None and self.board[row][col].color == color:
                        for index, (dr, dc) in enumerate(DIRS):
                            if not self.board[row][col].king:
                                if color is RED and index >= 2 and piece:
                                    continue
                                if color is BLUE and index <= 1:
                                    continue
                            new_row_1 = row + dr
                            new_col_1 = col + dc
                            new_row_2 = row + 2 * dr
                            new_col_2 = col + 2 * dc
                            if 0 <= new_row_1 < len(self.board) and 0 <= new_col_1 < len(self.board[0]) and 0 <= new_row_2 < len(self.board) and 0 <= new_col_2 < len(self.board[0]):
                                capture_piece = self.board[new_row_1][new_col_1]
                                if capture_piece is not None and capture_piece.color != color and self.board[new_row_2][new_col_2] is None:
                                    return True
            return False

        valid_moves = set()
        if not has_capture_moves():
            for index, (dr, dc) in enumerate(DIRS):
                if not piece.king:
                    if color is RED and index >= 2:
                        continue
                    if color is BLUE and index <= 1:
                        continue
                new_row = row + dr
                new_col = col + dc
                if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]) and self.board[new_row][new_col] is None:
                    valid_moves.add((new_row, new_col))
        self.valid_moves = valid_moves

    def move(self, piece, row, col):
        self.last_board = copy.deepcopy(self.board)
        captured_squares = self.capture_moves.get((row, col))
        for r, c in captured_squares:
            self.board[r][c] = None

        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        self.valid_moves = set()
        self.capture_moves = CaptureMovesDict()
