import pygame
from checkers.constants import *
from checkers.board import Board


class Game:

    def __init__(self, screen):
        self.turn = RED
        self.board = Board()
        self.board.draw(screen)
        self.selected = None
        self.screen = screen

    def _get_row_col_from_coordinates(self, x, y):
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return row, col

    def select(self, x, y):
        row, col = self._get_row_col_from_coordinates(x, y)

        if not (0 <= row < len(self.board.board)) or not (0 <= col < len(self.board.board[0])):
            return
        piece = self.board.get_piece(row, col)

        if self.selected and (row, col) in self.board.valid_moves:
            # if selected and valid move then move
            self.board.move(self.selected, row, col)
            self.selected = None
            self.board.unselect_piece()
            self.change_turn()
        elif piece is not None and piece.color is self.turn:
            # if select valid piece then select
            self.selected = piece
            self.board.select_piece(row, col)
            self.board.get_valid_moves(row, col)

    def change_turn(self):
        if self.turn == RED:
            self.turn = BLUE
        else:
            self.turn = RED

    def update(self, screen):
        print("updating")
        self.board.draw(screen)
        pygame.display.update()

    def undo(self, screen):
        self.selected = None
        self.board.board = self.board.last_board
        self.change_turn()
        self.board.draw(screen)
