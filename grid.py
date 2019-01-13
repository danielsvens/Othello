import pygame as pg


class Grid:

    def __init__(self):
        self.margin = 4
        self.grid = [[0 for _ in range(8)] for _ in range(8)]
        self.start_positions()

        self.rect_objects = list()

    def draw_grid(self, screen, position):

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
        # 1 White piece
        # 2 Black piece

        self.grid[3][3] = 1
        self.grid[3][4] = 2
        self.grid[4][3] = 2
        self.grid[4][4] = 1

    def get_rect(self):
        return self.rect_objects

    def add_piece(self, x, y, piece):
        self.grid[x][y] = piece
