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
    #    -> Multiplayer
    #        >> Host, server??
    #        >> Join/host menu
    #        >> networking log
    #        >> log to console
    #        >> 2 player mode
    #    -> Add AI
    #    ->
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
        self.grid.draw_grid(self.screen, self.size)
        self.board = self.grid.rect_objects
        coordinates = self.grid.coordinates(self.size)
        self.pieces.positions(coordinates)

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
                    for grid in self.board:
                        if grid.collidepoint(pg.mouse.get_pos()):
                            new_piece = [self.white, (int(grid[0] + grid[2] / 2),
                                                      int(grid[1] + grid[3] / 2)),
                                                      int(grid[3] / 2.5)]

                            if new_piece not in self.pieces.circles:
                                self.pieces.circles.append(new_piece)
                                self.log.console('added piece')
                            # TODO: Maybe add seperate lists for black pieces and white pieces ? ! ?

                            self.log.console('pieces on board: {}'.format(len(self.pieces.circles)))

                if event.type == pg.VIDEORESIZE:
                    # Keep screen updated for new size
                    # FIXME Screen doesn't update right while resizing
                    self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    self.grid.draw_grid(self.screen, self.size)
                    self.board = self.grid.get_rect()

            # SECTION EVENTS END

            # SECTION GRID
            for grid in self.board:
                pg.draw.rect(self.screen, (0, 255, 100), grid)

            # SECTION END GRID

            # SECTION PIECES

            # print(len(self.pieces.get_pieces()))
            for piece in self.pieces.get_pieces():
                pg.draw.circle(self.screen, piece[0], piece[1], 38)

            # SECTION END PIECES

            # -> FIXME
            if self.open_console:
                self.screen.blit(self.console.get_surface(), (0, 0))

            pg.display.update()
            self.clock.tick(self.fps)

        # SECTION MAIN LOOP END


if __name__ == '__main__':
    game = Game()
    game.start_game()
