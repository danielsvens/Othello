import pygame as pg
import textwrap


class ChatBox:

    def __init__(self, font):
        self.font = font
        self.color = (0, 0, 0)
        self.active = False
        self.text = ''
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_box_height = 0
        self.sent = []

    def handle_event(self, event, box):
        if event.type == pg.MOUSEBUTTONDOWN:
            if box.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.sent.append(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.text_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen, box):
        return screen.blit(self.text_surface, (box.x + 10, box.y + box.h - 26))

    def update(self, screen, box):
        spacing = 10
        text_buffer = []

        for txt in self.sent:
            text_buffer += textwrap.wrap(txt, box.w / 9 - 2)

        for item in text_buffer:
            text = self.font.render(f'User: {item}', True, self.color)
            screen.blit(text, (box.x + 10, box.y + spacing))
            spacing += 20

            if spacing >= box.h:
                self.sent.pop(0)
                spacing -= 20
