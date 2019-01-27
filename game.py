import pygame as pg
import os
from grid import Grid
from pieces import Piece
from console import Console
from logger import Logger
from chat import ChatBox


class Game:
    """
    #    TODO:
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
        self.done = False

        # Initialize grid and pieces
        self.grid = Grid()
        self.pieces = Piece(self.grid.grid)

        # Player white: 'w' black: 'b'
        self.current_player = 'b'

        # setup grid, coordinates and the pieces
        self.grid.update_grid(self.size)
        self.board = self.grid.get_rect()
        self.pieces.positions(self.grid.coordinates(self.size))

        # Overlay
        self.black_pieces, self.white_pieces = self.grid.count_pieces_on_board()
        pg.font.init()
        self.font = pg.font.SysFont('Verdana', 24)
        self.overlay = None
        self.end_font = pg.font.SysFont('Comic Sans MS', 150)
        self.GAME_ENDED = self.end_font.render('GAME ENDED', True, self.blue)
        self.GAME_ENDED_CENTER = self.GAME_ENDED.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.white_pieces_on_board = self.font.render('white: {}'.format(self.white_pieces), True, self.blue)
        self.black_pieces_on_board = self.font.render('black: {}'.format(self.black_pieces), True, self.blue)
        self.end_game = False

        # Messaging
        self.chat_font = pg.font.SysFont('Verdana', 14, bold=True)
        self.chat_bg = pg.Rect
        self.chat_box = ChatBox(self.chat_font)

    def update_board(self):
        # Keep screen updated for new size
        self.grid.update_grid(self.size)
        self.pieces.positions(self.grid.coordinates(self.size))
        self.board = self.grid.get_rect()

    def start_game(self):
        return self.main()

    def highlight_legal_moves(self):
        row = 0
        column = 0

        for rect in self.board:
            if column > 7:
                column = 0
                row += 1

            if rect.collidepoint(pg.mouse.get_pos()):
                move = self.pieces.calc_valid_moves(self.current_player, self.grid.get_grid())

                if move[row][column] == self.current_player:
                    pg.draw.rect(self.screen, (0, 255, 200), rect)

            column += 1

    def check_legal_moves_left(self, move):
        count = 0
        for m in move:
            for legal in m:
                if legal == self.current_player:
                    count += 1
        if count == 0:
            self.end_game = True

    def bg_rect(self):
        width_1, height_1, pos_x_1, pos_y_1 = self.grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = self.grid.rect_objects[-1]

        pg.draw.rect(self.screen, (30, 30, 30), [width_1 + 4, height_1 + 4, (width_2 - width_1) + pos_x_2, (height_2 - height_1) + pos_y_2])

    def info_section(self):
        width_1, height_1, pos_x_1, pos_y_1 = self.grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = self.grid.rect_objects[-1]
        width_pos = self.screen.get_width() / 25

        pg.draw.rect(self.screen, (30, 30, 30),
                     (width_pos + 4, height_1 + 4, (width_2 - width_1) - (pos_x_2 * 2),
                      (height_2 - height_1 * 4)), 10)

        pg.draw.rect(self.screen, (61, 43, 49, 0.8), (width_pos,
                                                      height_1 + 4, (width_2 - width_1) - (pos_x_2 * 2),
                                                      (height_2 - height_1 * 4)))

        pg.draw.rect(self.screen, (76, 87, 89, 0.8),
                     (width_pos, height_1, (width_2 - width_1) - (pos_x_2 * 2),
                      (height_2 - height_1 * 4)), 10)

        pg.draw.rect(self.screen, (34, 35, 35),
                     (width_pos + 4, height_1 + 4, (width_2 - width_1) - (pos_x_2 * 2) - 8,
                      (height_2 - height_1 * 4 - 8)), 3)

    def chat_window(self):
        width_1, height_1, pos_x_1, pos_y_1 = self.grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = self.grid.rect_objects[-1]
        width_pos = self.screen.get_width() / 25

        pg.draw.rect(self.screen, (30, 30, 30),
                     (width_pos + 4, (height_2 - height_1 * 2 - pos_y_2 / 2 + 8), (width_2 - width_1) - (pos_x_2 * 2),
                      (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 4)) + pos_y_2), 10)

        self.chat_bg = pg.draw.rect(self.screen, (61, 43, 49, 0.8), (width_pos + 4, (height_2 - height_1 * 2 - pos_y_2 / 2 + 4),
                                                      (width_2 - width_1) - (pos_x_2 * 2),
                                                      (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 4)) + pos_y_2))

        pg.draw.rect(self.screen, (76, 87, 89, 0.8),
                     (width_pos, (height_2 - height_1 * 2 - pos_y_2 / 2 + 4), (width_2 - width_1) - (pos_x_2 * 2),
                      (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 4)) + pos_y_2), 10)

        pg.draw.rect(self.screen, (34, 35, 35),
                     (width_pos + 4, (height_2 - height_1 * 2 - pos_y_2 / 2 + 8),
                      (width_2 - width_1) - (pos_x_2 * 2) - 8,
                      (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 12)) + pos_y_2), 3)

    def main(self):

        # SECTION MAIN LOOP
        while not self.done:

            self.overlay = self.font.render(
                'Current player: white' if self.current_player == 'w' else 'Current player: black', True, self.blue)

            self.check_legal_moves_left(self.pieces.calc_valid_moves(self.current_player, self.grid.get_grid()))

            # dt = self.clock.tick(self.fps) / 1000
            self.screen.fill((255, 255, 255))
            self.size = self.screen.get_width(), self.screen.get_height()

            # SECTION EVENTS
            for event in pg.event.get():
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

                self.chat_box.handle_event(event, self.chat_bg, self.screen)

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
                            move = self.pieces.calc_valid_moves(self.current_player, self.grid.get_grid())

                            if move[row][column] == self.current_player:
                                self.log.console('legal move')

                                self.pieces.circles.append([self.white, (int(rect[0] + rect[2] / 2),
                                                                         int(rect[1] + rect[3] / 2)),
                                                                         int(rect[3] / 2.5)])

                                self.grid.add_piece(row, column, self.current_player)
                                self.log.console('added piece')
                                self.pieces.flip(self.current_player, row, column, self.grid.get_grid())
                                self.update_board()

                                if self.current_player == 'w':
                                    self.current_player = 'b'
                                else:
                                    self.current_player = 'w'
                            else:
                                self.log.console('illegal move')

                        column += 1

                # Video Resize update screen
                if event.type == pg.VIDEORESIZE:
                    self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                    self.size = self.screen.get_width(), self.screen.get_height()
                    self.GAME_ENDED_CENTER = self.GAME_ENDED.get_rect(
                        center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
                    self.update_board()

            # SECTION EVENTS END

            # Draw screen
            self.bg_rect()
            self.info_section()
            self.chat_window()
            self.grid.draw_grid(self.screen)
            self.pieces.draw_pieces(self.screen)
            self.chat_box.draw(self.screen, self.chat_bg)
            self.chat_box.update(self.screen, self.chat_bg)

            self.screen.blit(self.overlay, ((self.screen.get_width() / 15), self.screen.get_height() / 7))
            self.screen.blit(self.white_pieces_on_board, ((self.screen.get_width() / 15), self.screen.get_height() / 5))
            self.screen.blit(self.black_pieces_on_board, ((self.screen.get_width() / 15), self.screen.get_height() / 4))

            if self.end_game:
                self.screen.blit(self.GAME_ENDED, (self.screen.get_width() / 4, self.screen.get_height() / 4))

            # -> FIXME: Console is not finished.
            # if self.open_console:
            #    self.screen.blit(self.console.get_surface(), self.text_rect)

            # Update pieces on board
            self.black_pieces, self.white_pieces = self.grid.count_pieces_on_board()
            self.white_pieces_on_board = self.font.render('white: {}'.format(self.white_pieces), True, self.blue)
            self.black_pieces_on_board = self.font.render('black: {}'.format(self.black_pieces), True, self.blue)

            # Draw highlight
            self.highlight_legal_moves()

            # Update screen
            pg.display.update()
            self.clock.tick(self.fps)

        # SECTION MAIN LOOP END


if __name__ == '__main__':
    game = Game()
    game.start_game()
