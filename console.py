import pygame as pg
from pygame import freetype
import os
from logger import Logger


class Console:

    def __init__(
            self,
            font_size=16,
            font='',
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            input_string='',
            screen=None
            ):

        """
        :param font_size: Font size in pixels
        :param font: Font-file
        :param text_color: rgb(0, 0, 0)
        :param cursor_color: rgb(0, 0, 0)
        :param input_string: Input to be displayed
        :return
        """

        self.font_size = font_size
        self.text_color = text_color
        self.cursor_color = cursor_color
        self.input_string = input_string
        self.screen = screen
        self.antialias = 250
        self.log = Logger('console.log')
        self.repeat_keys_initial_ms = 400
        self.repeat_keys_interval_ms = 35

        pg.freetype.init()

        if not os.path.isfile(font):
            self.font_object = pg.freetype.SysFont("monospaced", font_size)
        else:
            try:
                self.font_object = pg.freetype.Font(font, font_size)
            except EOFError:
                self.log.console('File not found')
                self.font_object = pg.freetype.SysFont("monospaced", font_size)

        self.console = pg.Surface((self.screen.get_width(), self.screen.get_height() / 3))
        self.console.set_alpha(250)
        self.console.fill((60, 67, 79))

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = self.repeat_keys_initial_ms
        self.keyrepeat_interval_ms = self.repeat_keys_interval_ms

        self.cursor_surface = pg.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(input_string)
        self.cursor_visible = True
        self.cursor_switch_ms = 500
        self.cursor_ms_counter = 0

        self.clock = pg.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pg.K_BACKSPACE:
                    self.input_string = (
                            self.input_string[:max(self.cursor_position - 1, 0)]
                            + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pg.K_DELETE:
                    self.input_string = (
                            self.input_string[:self.cursor_position]
                            + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pg.K_RETURN:
                    return True

                elif event.key == pg.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pg.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pg.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pg.K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                            self.input_string[:self.cursor_position]
                            + event.unicode
                            + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pg.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (self.keyrepeat_intial_interval_ms - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pg.event.post(pg.event.Event(event_key, event_unicode))

        # Re-render text surface:
        self.font_object.render_to(self.console, (int(self.font_size / 20 + 1), self.font_size), self.input_string, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size + self.cursor_surface.get_width()
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
                self.console.blit(self.cursor_surface, (cursor_y_pos, 15))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.console

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0
