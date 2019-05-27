import pygame as pg
from player_piece import PlayerPiece


class Piece:

    def __init__(self, grid):
        self.grid = grid
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.circles = list()

    def create_piece(self, color, position):

        # [pos_x, pos_y, width_x, height_y]
        circle = [color, (int(position[0] + position[2] / 2), int(position[1] + position[3] / 2)),
                                                int(position[3] / 2.5)]

        self.circles.append(circle)

    def positions(self, coordinates):
        counter_x = -1

        self.circles = list()

        for x in self.grid:
            counter_x += 1
            counter_y = -1
            for o in x:
                counter_y += 1
                if o == PlayerPiece.WHITE:
                    self.create_piece(self.WHITE, coordinates[str(counter_x)][counter_y])
                elif o == PlayerPiece.BLACK:
                    self.create_piece(self.BLACK, coordinates[str(counter_x)][counter_y])

    def get_pieces(self):
        return self.circles

    def draw_pieces(self, screen):
        for piece in self.circles:
            pg.draw.circle(screen, piece[0], piece[1], piece[2])

    def calc_valid_moves(self, player, board):
        valid = [[PlayerPiece.EMPTY for _ in range(8)] for _ in range(8)]

        for row in range(8):
            for column in range(8):
                if board[row][column] == PlayerPiece.EMPTY:
                    nw = self.valid_move(player, -1, -1, row, column, board)
                    nn = self.valid_move(player, -1, 0, row, column, board)
                    ne = self.valid_move(player, -1, 1, row, column, board)

                    ww = self.valid_move(player, 0, -1, row, column, board)
                    ee = self.valid_move(player, 0, 1, row, column, board)

                    sw = self.valid_move(player, 1, -1, row, column, board)
                    ss = self.valid_move(player, 1, 0, row, column, board)
                    se = self.valid_move(player, 1, 1, row, column, board)

                    if nw or nn or ne or ww or ee or sw or ss or se:
                        valid[row][column] = player

        return valid

    def valid_move(self, player, x, y, row, column, board):
        if player == PlayerPiece.WHITE:
            other = PlayerPiece.BLACK
        else:
            other = PlayerPiece.WHITE

        if row + x < 0 or row + x > 7:
            return False

        if column + y < 0 or column + y > 7:
            return False

        if board[row + x][column + y] != other:
            return False

        if row + (x * 2) < 0 or row + (x * 2) > 7:
            return False

        if column + (y * 2) < 0 or column + (y * 2) > 7:
            return False

        return self.match(player, x, y, row + (x * 2), column + (y * 2), board)

    def match(self, player, x, y, row, column, board):
        if board[row][column] == player:
            return True

        if row + x < 0 or row + x > 7:
            return False

        if column + y < 0 or column + y > 7:
            return False

        return self.match(player, x, y, row + x, column + y, board)

    def flip(self, player, row, column, board):
        self.flip_pieces(player, -1, -1, row, column, board)
        self.flip_pieces(player, -1, 0, row, column, board)
        self.flip_pieces(player, -1, 1, row, column, board)

        self.flip_pieces(player, 0, -1, row, column, board)
        self.flip_pieces(player, 0, 1, row, column, board)

        self.flip_pieces(player, 1, -1, row, column, board)
        self.flip_pieces(player, 1, 0, row, column, board)
        self.flip_pieces(player, 1, 1, row, column, board)

    def flip_pieces(self, player, x, y, row, column, board):

        if row + x < 0 or row + x > 7:
            return False

        if column + y < 0 or column + y > 7:
            return False

        if board[row + x][column + y] == PlayerPiece.EMPTY:
            return False

        if board[row + x][column + y] == player:
            return True
        else:
            if self.flip_pieces(player, x, y, row + x, column + y, board):
                board[row + x][column + y] = player
                return True
            else:
                return False
