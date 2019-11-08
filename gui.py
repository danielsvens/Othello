import pygame as pg


class Gui:

    # Extremely unreadable code =D but it works!

    @staticmethod
    def bg_rect(grid, screen):
        width_1, height_1, pos_x_1, pos_y_1 = grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = grid.rect_objects[-1]

        pg.draw.rect(screen, (30, 30, 30),
                     [width_1 + 4, height_1 + 4,
                     (width_2 - width_1) + pos_x_2,
                     (height_2 - height_1) + pos_y_2])

    @staticmethod
    def info_section(grid, screen):
        width_1, height_1, pos_x_1, pos_y_1 = grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = grid.rect_objects[-1]
        width_pos = screen.get_width() / 25

        pg.draw.rect(screen, (30, 30, 30),
                     (width_pos + 4, height_1 + 4,
                     (width_2 - width_1) - (pos_x_2 * 2),
                     (height_2 - height_1 * 4)), 10)

        pg.draw.rect(screen, (61, 43, 49, 0.8),
                     (width_pos,
                     height_1 + 4,
                     (width_2 - width_1) - (pos_x_2 * 2),
                     (height_2 - height_1 * 4)))

        pg.draw.rect(screen, (76, 87, 89, 0.8),
                     (width_pos, height_1,
                     (width_2 - width_1) - (pos_x_2 * 2),
                     (height_2 - height_1 * 4)), 10)

        pg.draw.rect(screen, (34, 35, 35),
                     (width_pos + 4, height_1 + 4,
                     (width_2 - width_1) - (pos_x_2 * 2) - 8,
                     (height_2 - height_1 * 4 - 8)), 3)

    @staticmethod
    def chat_bg(grid, screen):
        width_1, height_1, pos_x_1, pos_y_1 = grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = grid.rect_objects[-1]
        width_pos = screen.get_width() / 25

        pg.draw.rect(screen, (30, 30, 30),
                     (width_pos + 4,
                     (height_2 - height_1 * 2 - pos_y_2 / 2 + 8),
                     (width_2 - width_1) - (pos_x_2 * 2),
                     (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 4)) + pos_y_2), 10)

        pg.draw.rect(screen, (61, 43, 49, 0.8),
                     (width_pos + 4, (height_2 - height_1 * 2 - pos_y_2 / 2 + 4),
                     (width_2 - width_1) - (pos_x_2 * 2),
                     (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 4)) + pos_y_2))

        pg.draw.rect(screen, (76, 87, 89, 0.8),
                     (width_pos,
                     (height_2 - height_1 * 2 - pos_y_2 / 2 + 4),
                     (width_2 - width_1) - (pos_x_2 * 2),
                     (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 4)) + pos_y_2), 10)

        pg.draw.rect(screen, (34, 35, 35),
                     (width_pos + 4,
                     (height_2 - height_1 * 2 - pos_y_2 / 2 + 8),
                     (width_2 - width_1) - (pos_x_2 * 2) - 8,
                     (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 12)) + pos_y_2), 3)

        x = width_pos + 4
        w = (width_2 - width_1) - (pos_x_2 * 2) - 8
        y = (height_2 - height_1 * 2 - pos_y_2 / 2 + 8) + \
            (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 12)) + pos_y_2 - 35

        pg.draw.line(screen, (34, 35, 35), (x, y), (x + w, y), 3)

        return pg.draw.rect(screen, (34, 35, 35),
                            (width_pos + 4,
                            (height_2 - height_1 * 2 - pos_y_2 / 2 + 8),
                            (width_2 - width_1) - (pos_x_2 * 2) - 8,
                            (height_2 - (height_2 - height_1 * 2 - pos_y_2 / 2 + 12)) + pos_y_2 - 35), 1)

    @staticmethod
    def input_box(grid, screen, color):
        width_1, height_1, pos_x_1, pos_y_1 = grid.rect_objects[0]
        width_2, height_2, pos_x_2, pos_y_2 = grid.rect_objects[-1]
        width_pos = screen.get_width() / 25

        return pg.draw.rect(screen, color,
                            (width_pos + 4,
                            (height_2 - height_1 / 3 + pos_y_2 - 6),
                            (width_2 - width_1) - (pos_x_2 * 2) - 8,
                            (height_2 - (height_2 - height_1 / 2 + 14))), 3)
