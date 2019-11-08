import pygame as pg
import os
import time


class Console:

    LOG_FILE = 'console.log'

    def __init__(self, screen, font):
        if os.path.isfile(self.LOG_FILE):
            self.log = os.path.abspath(self.LOG_FILE)
        self.screen = screen

        self.font = font
        self.text_buffer = []
        self.surface = pg.Surface((self.screen.get_width(), self.screen.get_height() / 3))
        self.surface.set_alpha(250)
        self.surface.fill((60, 67, 79))

        self.buffer = []

    @property
    def get_surface(self):
        return self.surface

    def tail_log(self):
        for line in self._tail(open(self.log)):
            self.buffer.append(self.font.render(line, True, (0, 0, 0)))

    def update(self, box):
        spacing = 10

        for line in self.buffer:
            self.surface.blit(line, (box.x + 10, box.y + spacing))
            spacing += 20

            if spacing >= 80:
                self.buffer.pop(0)
                spacing -= 20

            print(self.buffer)

    @staticmethod
    def _tail(f):
        f.seek(0, 2)
        while True:
            line = f.readline()

            if not line:
                time.sleep(0.1)
                continue

            yield line
