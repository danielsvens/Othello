import pygame as pg
import os
from grid import Grid
from pieces import Piece
from console import Console
from logger import Logger


class Game:
    """
    #    TODO:
    #    -> MouseOver on valid moves
    #    -> Create valid moves
    #    -> Add sound effects
    #    -> Add start game menu
    #    -> Add overlay / pieces gathered / UI
    #    -> Finish Console
    #    -> Add AI
    #    -> Multiplayer
    #        >> Host, server??
    #        >> Join/host menu
    #        >> log to console
    #        >> 2 player mode
    """

    def __init__(self):
        pg.init()

        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Initialize the screen
        self.screen = pg.display.set_mode((1280, 960), pg.RESIZABLE)
        self.size = self.screen.get_width(), self.screen.get_height()

        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))

        # Initialize the console
        self.console = Console(screen=self.screen)
        self.open_console = False
        self.log = Logger('console.log')

        self.clock = pg.time.Clock()

        # Sound Effects
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.mixer.init()

        # Sprites if we need any ???
        self.all_sprites = pg.sprite.Group()

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 100)
        self.blue = (0, 100, 255)

        self.fps = 60

        # Initialize grid and pieces
        self.grid = Grid()
        self.pieces = Piece(self.grid.grid)

        # setup grid, coordinates andthe pieces
        self.grid.update_grid(self.screen, self.size)
        self.board = self.grid.get_rect()
        self.pieces.positions(self.grid.coordinates(self.size))

    def intro(self):
        pass

    def start_game(self):
        return self.main()

    def main(self):

        done = False

        # SECTION MAIN LOOP
        while not done:

            # dt = self.clock.tick(self.fps) / 1000
            self.screen.fill((255, 255, 255))
            self.size = self.screen.get_width(), self.screen.get_height()

            events = pg.event.get()

            # SECTION EVENTS
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()

                    if event.key == pg.K_1:
                        if self.open_console:
                            self.open_console = False
                        else:
                            self.open_console = True

                if event.type == pg.MOUSEBUTTONDOWN:

                    # Get mapped row, column to each rectangle
                    row = 0
                    column = 0

                    for rect in self.board:
                        if column > 7:
                            column = 0
                            row += 1

                        # Grid collision
                        if rect.collidepoint(pg.mouse.get_pos()):

                            move = self.pieces.calc_valid_moves(self.grid.get_grid())
                            if move[row][column] == 'w':
                                print('legal move')

                                if self.grid.get_grid_coords(row, column) == '#':
                                    self.pieces.circles.append([self.white, (int(rect[0] + rect[2] / 2),
                                                                             int(rect[1] + rect[3] / 2)),
                                                                             int(rect[3] / 2.5)])

                                    self.grid.add_piece(row, column, 'w')
                                    self.log.console('added piece')
                                else:
                                    # TODO: Maybe add seperate lists for black pieces and white pieces ? ! ?
                                    self.log.console('pieces on board: {}'.format(len(self.pieces.circles)))
                            else:
                                print('illegal move')

                        column += 1

                if event.type == pg.VIDEORESIZE:

                    # Keep screen updated for new size
                    self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    self.size = self.screen.get_width(), self.screen.get_height()
                    self.grid.update_grid(self.screen, self.size)
                    self.pieces.positions(self.grid.coordinates(self.size))
                    self.board = self.grid.get_rect()

            # SECTION EVENTS END

            # SECTION GRID

            self.grid.draw_grid(self.screen)

            # SECTION END GRID

            # SECTION PIECES

            self.pieces.draw_pieces(self.screen)

            # SECTION END PIECES

            # -> FIXME: Console is not finished.
            if self.open_console:
                self.screen.blit(self.console.get_surface(), (0, 0))

            pg.display.update()
            self.clock.tick(self.fps)

        # SECTION MAIN LOOP END


if __name__ == '__main__':
    game = Game()
    game.start_game()
