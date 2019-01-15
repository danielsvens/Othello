import pygame as pg


class Grid:

    def __init__(self):
        self.margin = 4
        self.grid = [['#' for _ in range(8)] for _ in range(8)]
        self.start_positions()

        self.rect_objects = list()

    def update_grid(self, screen, position):

        objects = list()

        pos_x, pos_y = position
        width, height = position

        for row in range(8):
            for column in range(8):
                rect = pg.draw.rect(screen, (0, 255, 100), [(self.margin + width / 16) * column + pos_x / 4,
                                                            (self.margin + height / 10) * row + pos_y / 10,
                                                            width / 16, height / 10])

                objects.append(rect)

        self.rect_objects = objects

    def coordinates(self, position):

        pos_x, pos_y = position
        width, height = position
        coordinates = {}

        for row in range(8):
            for column in range(8):
                coordinates.update({str(row): list()})

        for row in range(8):
            for column in range(8):
                coordinates[str(row)].append([(self.margin + width / 16) * column + pos_x / 4,
                                             (self.margin + height / 10) * row + pos_y / 10,
                                             width / 16, height / 10])

        return coordinates

    def start_positions(self):
        # 'w' White piece
        # 'b' Black piece

        self.grid[3][3] = 'w'
        self.grid[3][4] = 'b'
        self.grid[4][3] = 'b'
        self.grid[4][4] = 'w'

    def get_rect(self):
        return self.rect_objects

    def add_piece(self, x, y, piece):
        self.grid[x][y] = piece

    def draw_grid(self, screen):
        for grid in self.rect_objects:
            pg.draw.rect(screen, (0, 255, 100), grid)

    def get_grid_coords(self, x, y):
        return self.grid[x][y]

    def get_grid(self):
        return self.grid

    def count_pieces_on_board(self):
        black, white = 0, 0

        for row in self.grid:
            for column in row:
                if column == 'w':
                    white += 1
                elif column == 'b':
                    black += 1

        return black, white



