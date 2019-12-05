import os

from tkinter import *
from tkinter import filedialog as fd

import pygame

from game.direction import Direction
from game.drawing.components import *
from game.entities import Food, Level
from game.settings import Settings
from game.events import PickWall, PickSnake, PickEraser, Save

settings = Settings()

__all__ = ['GameDrawing', 'FieldDrawing', 'FreeGameDrawing', 'LevelDrawing',
           'GameMakerDrawing']


def _load_image(name):
    return pygame.image.load(settings.picture(name))


def _draw_image(play_surface, image, x, y, rotate_angle=0):
    if rotate_angle:
        image = pygame.transform.rotate(image, rotate_angle)
    rect_image = image.get_rect(topleft=(x, y))
    play_surface.blit(image, rect_image)


class FieldDrawing:
    size_cell = settings.picture_size

    # region load_image

    wall = _load_image('wall')
    basic_food = _load_image('basic_apple')
    gold_apple = _load_image('gold_apple')
    wormy_apple = _load_image('wormy_apple')
    high_speed_apple = _load_image('high_speed_apple')
    snake_body = _load_image('snake_body')
    snake_head = _load_image('snake_head')
    snake_tail = _load_image('snake_tail')
    snake_turn = _load_image('snake_turn')

    # endregion

    _food_image = {Food(*food): _load_image(name)
                   for food, name
                   in settings.food_name_picture.items()}

    # Угол поворота [head, body, tail] змейки согласно его направлению
    dir_turn_angle_SBI = {
        Direction.RIGHT: -90,
        Direction.DOWN: 180,
        Direction.LEFT: 90,
        Direction.UP: 0
    }

    # Угол поворота [turn] змейки согласно его направлению
    _dir_turn_angle_STI = {
        (Direction.RIGHT, Direction.UP): 180,
        (Direction.DOWN, Direction.LEFT): 180,
        (Direction.UP, Direction.RIGHT): 0,
        (Direction.LEFT, Direction.DOWN): 0,
        (Direction.UP, Direction.LEFT): -90,
        (Direction.RIGHT, Direction.DOWN): -90,
        (Direction.LEFT, Direction.UP): 90,
        (Direction.DOWN, Direction.RIGHT): 90
    }

    def __init__(self, field, path_to_bg, surface):
        self.field = field
        if (field.height * self.size_cell != surface.get_height()
                or field.width * self.size_cell != surface.get_width()):
            raise ValueError('Размеры surface не соответствуют размерам поля')

        self.surface = surface
        self.bg = (pygame.image.load(path_to_bg)
                   if path_to_bg is not None and os.path.exists(path_to_bg)
                   else None)

    def _draw_snake(self):
        pointer = 0
        prev_sp = None
        for sp in self.field.snake:
            location = (sp.location.x * self.size_cell,
                        sp.location.y * self.size_cell)
            if pointer == 0:
                _draw_image(self.surface,
                            self.snake_head,
                            *location,
                            rotate_angle=self.dir_turn_angle_SBI[sp.direction])

            elif pointer == len(self.field.snake) - 1:
                _draw_image(self.surface,
                            self.snake_tail,
                            *location,
                            rotate_angle=self.dir_turn_angle_SBI[prev_sp.direction])

            else:
                if prev_sp.direction == sp.direction:
                    _draw_image(self.surface,
                                self.snake_body,
                                *location,
                                rotate_angle=self.dir_turn_angle_SBI[sp.direction])
                else:
                    _draw_image(self.surface,
                                self.snake_turn,
                                *location,
                                rotate_angle=self._dir_turn_angle_STI[sp.direction, prev_sp.direction])

            prev_sp = sp
            pointer += 1

    def _draw_food(self):
        for location, food in self.field.foods_location.items():
            _draw_image(
                self.surface,
                self._food_image[food],
                location.x * self.size_cell,
                location.y * self.size_cell)

    def _draw_walls(self):
        for location in self.field.walls:
            _draw_image(
                self.surface,
                self.wall,
                location.x * self.size_cell,
                location.y * self.size_cell)

    def _draw_bg(self):
        if self.bg is not None:
            self.surface.blit(self.bg, (0, 0))
        else:
            self.surface.fill(pygame.Color('white'))

    def draw(self):
        self._draw_bg()
        self._draw_snake()
        self._draw_walls()
        self._draw_food()


class GameDrawing:
    size_cell = settings.picture_size

    _heart = _load_image('heart')
    _toolbar_color = pygame.Color('0x002137')

    def __init__(self, level, delta_x=0, delta_y=0):
        """
        :param delta_x: смещение рисования поля по Ox относительно левого верхнего угла
        :param delta_y: смещение рисования поля по Oy относительно левого верхнего угла
        """

        self.level = level
        self.delta_x = delta_x
        self.delta_y = delta_y

        width_field = self.size_cell * level.field.width
        height_field = self.size_cell * level.field.height
        self.surface = pygame.display.set_mode((width_field + self.delta_x,
                                                height_field + self.delta_y))

        field_surface = self.surface.subsurface(
            pygame.Rect(self.delta_x, self.delta_y, width_field, height_field))

        self.field_drawer = \
            FieldDrawing(level.field,
                         settings.background_image(level.name) if level.name else None,
                         field_surface)

    def _draw_toolbar(self):
        pass

    def draw(self):
        self.field_drawer.draw()
        self._draw_toolbar()


class LevelDrawing(GameDrawing):
    def __init__(self, level: Level, level_number: int, count_levels: int):
        super().__init__(level, delta_y=self.size_cell * 2)

        self.level_number = level_number
        self.count_levels = count_levels

    def _draw_toolbar(self):
        pygame.draw.rect(
            self.surface,
            self._toolbar_color,
            pygame.Rect(0, 0, self.surface.get_width(), self.delta_y)
        )

        for i in range(self.level.health):
            _draw_image(self.surface, self._heart,
                        self.size_cell * (i + 1.5), (self.delta_y - self._heart.get_height()) / 2)

        # пишет счёт у данного уровня
        text = f'Score: {self.level.score}/{self.level.max_score}'
        s_font = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                int((self.surface.get_width() - self.size_cell * 5 - 20) * 0.4),
                int(self.delta_y * 0.65),
                text
            )
        )
        s_surf = s_font.render(text, True, pygame.Color('white'))
        s_rect = s_surf.get_rect()
        s_rect.topleft = ((self.surface.get_width() - s_rect.width) / 2,
                          (self.delta_y - s_rect.height) / 2)
        self.surface.blit(s_surf, s_rect)

        # пишет какой уровень по счёту сейчас и сколько в общем
        text = f'Level: {self.level_number}/{self.count_levels}'
        lvl_font = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                int((self.surface.get_width() - self.size_cell * 5 - 20) * 0.4),
                int(self.delta_y * 0.65),
                text
            )
        )
        lvl_surf = lvl_font.render(text, True, pygame.Color('white'))
        lvl_rect = lvl_surf.get_rect()
        lvl_rect.topleft = (self.surface.get_width() - 20 - lvl_rect.width,
                            (self.delta_y - s_rect.height) / 2)
        self.surface.blit(lvl_surf, lvl_rect)


class FreeGameDrawing(GameDrawing):
    def __init__(self, level: Level):
        super().__init__(level, delta_y=self.size_cell * 2)

    def _draw_toolbar(self):
        pygame.draw.rect(
            self.surface,
            self._toolbar_color,
            pygame.Rect(0, 0, self.surface.get_width(), self.delta_y)
        )

        score_text = f'Score: {self.level.score}'
        s_font = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                int(self.surface.get_width() * 0.8),
                int(self.delta_y * 0.65),
                score_text
            )
        )
        s_surf = s_font.render(score_text, True, pygame.Color('white'))
        s_rect = s_surf.get_rect()
        s_rect.topleft = ((self.surface.get_width() - s_rect.width) / 2,
                          (self.delta_y - s_rect.height) / 2)
        self.surface.blit(s_surf, s_rect)


# TODO:: дорефакторить

class GameMakerDrawing(GameDrawing):
    def __init__(self, level: Level):
        self._width_toolbar = 110
        super().__init__(level, delta_x=self._width_toolbar)

        self.mode = 'grid'  # mode = grid or preview
        self._active_button = None
        self.direction_snake = Direction.RIGHT

        size_buttons = (45, 25)
        self._height_header = 25
        self._size_buttons_components = (self.size_cell, self.size_cell)
        x = self.delta_x - 20 - self._size_buttons_components[0]

        # создаю изображение змейки для кнопки
        snake_image = pygame.Surface((self.size_cell * 3, self.size_cell))
        _draw_image(snake_image, self.field_drawer.snake_tail, 0, 0,
                    self.field_drawer.dir_turn_angle_SBI[self.direction_snake])
        _draw_image(snake_image, self.field_drawer.snake_body, self.size_cell, 0,
                    self.field_drawer.dir_turn_angle_SBI[self.direction_snake])
        _draw_image(snake_image, self.field_drawer.snake_head, 2 * self.size_cell, 0,
                    self.field_drawer.dir_turn_angle_SBI[self.direction_snake])
        snake_image.set_colorkey(pygame.Color('black'))

        self.buttons_components = [Button(self.surface,
                                          pygame.Rect(x, self._height_header,
                                                      *self._size_buttons_components),
                                          button_image=self.field_drawer.wall,
                                          name='wall',
                                          handler=self._handle_pick_wall),
                                   Button(self.surface,
                                          pygame.Rect(x, self._height_header + 5 + self._size_buttons_components[1],
                                                      *self._size_buttons_components),
                                          button_color=pygame.Color('white'),
                                          name='eraser',
                                          handler=self._handle_pick_eraser),
                                   Button(self.surface,
                                          pygame.Rect(x - 14,
                                                      self._height_header + 10 + 2 * self._size_buttons_components[1],
                                                      snake_image.get_width(), snake_image.get_height()),
                                          button_image=snake_image,
                                          name='snake',
                                          handler=self._handle_pick_snake),
                                   Button(self.surface,
                                          pygame.Rect(5,
                                                      self._height_header + 15 + 3 * self._size_buttons_components[1],
                                                      self.delta_x - 10, 17),
                                          text='Back Ground',
                                          handler=self._handle_pick_bg),
                                   Button(self.surface,
                                          pygame.Rect(5,
                                                      self._height_header + 35 + 3 * self._size_buttons_components[1],
                                                      self.delta_x - 10, 17),
                                          text='Skip Back Ground',
                                          handler=self._skip_bg)]

        self.buttons_redirect = [Button(self.surface,
                                        pygame.Rect(size_buttons[0] + 15,
                                                    self.surface.get_height() - 5 - size_buttons[1],
                                                    *size_buttons),
                                        text='Save',
                                        handler=self._save_level)]

        self.button_change_mode = Button(self.surface,
                                         pygame.Rect(5, self.surface.get_height() - 5 - size_buttons[1],
                                                     *size_buttons),
                                         name='mode',
                                         text='Preview',
                                         handler=self._handle_change_mode)

        self.buttons = self.buttons_components + self.buttons_redirect + [self.button_change_mode]

    def _handle_pick_wall(self):
        pick = PickWall()
        pygame.event.post(pick.event)
        for button in self.buttons_components:
            if button.name == 'wall':
                self._active_button = button
                break

    def _handle_pick_eraser(self):
        pick = PickEraser()
        pygame.event.post(pick.event)
        for button in self.buttons_components:
            if button.name == 'eraser':
                self._active_button = button
                break

    def _handle_pick_snake(self):
        pick = PickSnake(self.direction_snake)
        pygame.event.post(pick.event)
        for button in self.buttons_components:
            if button.name == 'snake':
                self._active_button = button
                break

    def _handle_change_mode(self):
        if self.mode == 'grid':
            self.mode = 'preview'
            self.button_change_mode.text = 'Grid'
        else:
            self.mode = 'grid'
            self.button_change_mode.text = 'Preview'

    def _handle_pick_bg(self):
        root = Tk()
        root.withdraw()
        root.update()
        file_name = fd.askopenfilename(filetypes=[("image files", "*.png")])
        root.destroy()
        if file_name:
            self.field_drawer.bg = pygame.image.load(file_name)
            if (self.field_drawer.bg.get_width() != self.field_drawer.surface.get_width()
                    or self.field_drawer.bg.get_height() != self.field_drawer.surface.get_height()):
                self.field_drawer.bg = pygame.transform.scale(self.field_drawer.bg,
                                                              (self.field_drawer.surface.get_width(),
                                                               self.field_drawer.surface.get_height()))

    def _skip_bg(self):
        self.field_drawer.bg = None

    def _save_level(self):
        if len(self.level.field.snake) == 3:
            field = self.level.field
            score_for_win = self.level.max_score

            _map = Level.anti_parse_map(field, score_for_win)
            count_levels = len(os.listdir(settings.levels_dir)) - 1
            level_name = f'level_{count_levels}'
            os.mkdir(os.path.join(settings.levels_dir, level_name))
            with open(settings.map_file(level_name), 'w+') as file:
                for i in range(len(_map) - 1):
                    file.write(_map[i] + '\n')
                file.write(_map[-1])

            bg = self.field_drawer.bg
            if bg is not None:
                pygame.image.save(bg, settings.background_image(level_name))

            settings.add_level(level_name)

            redirect = Save()
            pygame.event.post(redirect.event)

    def _draw_toolbar(self):
        pygame.draw.rect(self.surface, pygame.Color('0x000080'),
                         pygame.Rect(0, 0, self.delta_x, self.surface.get_height()))

        font = pygame.font.SysFont("Calibri", 17)
        header = font.render('Components', True, pygame.Color('white'))
        self.surface.blit(header, ((self.delta_x - header.get_width()) / 2, 5))

        font = pygame.font.SysFont("Calibri", 17)
        wall = font.render('Wall -', True, pygame.Color('white'))
        self.surface.blit(wall, (5, self._height_header))

        eraser = font.render('Eraser -', True, pygame.Color('white'))
        self.surface.blit(eraser, (5, self._height_header + 5 + self._size_buttons_components[1]))

        snake = font.render('Snake -', True, pygame.Color('white'))
        self.surface.blit(snake, (5, self._height_header + 10 + 2 * self._size_buttons_components[1]))

        if self._active_button is not None:
            button = self._active_button
            pygame.draw.rect(self.surface, pygame.Color('0x75bbfd'), button.rect, 3)

        for button in self.buttons:
            button.draw()

    def draw(self):
        super().draw()

        if self.mode == 'grid':
            # TODO: разобраться с alpha
            color_circle = pygame.Color('black')
            color_circle.a = 128
            for i in range(self.level.field.width):
                x = self.delta_x + (i + 1) * self.size_cell
                pygame.draw.line(
                    self.surface, color_circle,
                    (x, 0),
                    (x, self.surface.get_height()),
                )

            for i in range(self.level.field.height):
                y = (i + 1) * self.size_cell
                pygame.draw.line(self.surface, color_circle,
                                 (self.delta_x, y),
                                 (self.surface.get_width(), y))
