import pygame as pg


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

        for x in self.grid:
            counter_x += 1
            counter_y = -1
            for o in x:
                counter_y += 1
                if o == 1:
                    self.create_piece(self.WHITE, coordinates[str(counter_x)][counter_y])
                elif o == 2:
                    self.create_piece(self.BLACK, coordinates[str(counter_x)][counter_y])

    def get_pieces(self):
        return self.circles
