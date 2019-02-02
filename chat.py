import pygame as pg


class ChatBox:

    def __init__(self, font):
        self.text = ''
        self.font = font
        self.color = (0, 0, 0)
        self.active = False
        self.text_surface = self.font.render(self.text, True, self.color)
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
        return screen.blit(self.text_surface, (box.x + 10, box.y + box.h - 30))

    def update(self, screen, box):
        counter = 10

        for item in self.sent:
            text = self.font.render('user: {}'.format(item), True, self.color)
            screen.blit(text, (box.x + 10, box.y + counter))
            counter += 20
