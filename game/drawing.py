import os

import pygame

from game.direction import Direction
from game.entities import Food
from game.entities import Level
from game.settings import Settings

settings = Settings()

__all__ = ['Button',
           'Menu', 'WinWindow', 'EndFreeGameWindow', 'GameOverWindow',
           'GameDrawing', 'FieldDrawing', 'FreeGameDrawing', 'LevelDrawing']


def _load_image(name):
    return pygame.image.load(settings.picture(name))


def _draw_image(play_surface, image, left, top, rotate_angle=0):
    if rotate_angle:
        image = pygame.transform.rotate(image, rotate_angle)
    rect_image = image.get_rect(topleft=(top, left))
    play_surface.blit(image, rect_image)


class Button:
    def __init__(self,
                 surface,
                 x, y,
                 width, height,
                 text, text_color=pygame.Color('black'),
                 button_color=pygame.Color('white'),
                 href=None,
                 name=None):
        self.parent_surface = surface
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.href = href
        self.name = text if name is None else name
        self._rect = pygame.Rect(x, y, width, height)

    def draw(self):
        self._draw_button()
        self._write_text()

    def _get_size_for_calibri(self):
        # формула специально для шрифта Calibri в pygame
        size_width = 8 * self.width // (5 * len(self.text)) - 1
        size_height = 2 * self.height // 3 - 1
        return max(min(size_height, size_width), 1)

    def _write_text(self):
        font_size = self._get_size_for_calibri()
        font = pygame.font.SysFont("Calibri", font_size)
        text = font.render(self.text, True, self.text_color)
        self.parent_surface.blit(text,
                                 (self.x + (self.width - text.get_width()) / 2,
                                  self.y + (self.height - text.get_height()) / 2))

    def _draw_button(self):
        width_circle = min(self.height, self.width) // 20
        color = self.button_color // pygame.Color(2, 2, 2, 255)
        color.a = self.button_color.a

        pygame.draw.rect(self.parent_surface, self.button_color,
                         (self.x, self.y, self.width, self.height))

        # обводка прямоугольника (кнопки)
        points = [(self.x, self.y),
                  (self.x, self.y + self.height),
                  (self.x + self.width, self.y + self.height),
                  (self.x + self.width, self.y)]
        for i in range(4):
            pygame.draw.line(self.parent_surface, color,
                             points[i], points[i - 3], width_circle)

    def is_pressed(self, mouse):
        return (self._rect.topleft[0] < mouse[0] < self._rect.bottomright[0]
                and self._rect.topleft[1] < mouse[1] < self._rect.bottomright[1])

# region windows


class Menu:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 20, 160, 50, 'Game with Levels', href='level game'),
                        Button(self.surface, 20, 90, 160, 50, 'Free game', href='free game')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        for button in self.buttons:
            button.draw()


class WinWindow:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK',
                               href='menu')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_win = pygame.font.SysFont("Calibri", 40)
        text_win = font_win.render('You WIN!', True, pygame.Color('black'))
        self.surface.blit(text_win, ((self.surface.get_width() - text_win.get_width()) / 2, 30))
        for button in self.buttons:
            button.draw()


class GameOverWindow:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK', href='menu')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_lose = pygame.font.SysFont("Calibri", 30)
        text_lose = font_lose.render('Game Over :(', True, pygame.Color('black'))
        self.surface.blit(text_lose, ((self.surface.get_width() - text_lose.get_width()) / 2, 30))
        for button in self.buttons:
            button.draw()


class EndFreeGameWindow:
    def __init__(self, score):
        self.score = score
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK', href='menu')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_win = pygame.font.SysFont("Calibri", 25)
        text_win = font_win.render('End of the Game', True, pygame.Color('black'))
        self.surface.blit(text_win, ((self.surface.get_width() - text_win.get_width()) / 2, 20))

        font_score = pygame.font.SysFont("Calibri", 20)
        text_score = font_score.render(f'Score: {self.score}', True, pygame.Color('black'))
        self.surface.blit(text_score, ((self.surface.get_width() - text_score.get_width()) / 2, 50))
        for button in self.buttons:
            button.draw()

# endregion


class FieldDrawing:
    size_cell = settings.picture_size

    # region load_image

    _wall = _load_image('wall')
    _basic_food = _load_image('basic_apple')
    _gold_apple = _load_image('gold_apple')
    _wormy_apple = _load_image('wormy_apple')
    _high_speed_apple = _load_image('high_speed_apple')
    _snake_body = _load_image('snake_body')
    _snake_head = _load_image('snake_head')
    _snake_tail = _load_image('snake_tail')
    _snake_turn = _load_image('snake_turn')

    # endregion

    _food_image = {Food(*food): _load_image(name)
                   for food, name
                   in settings.food_name_picture.items()}

    # Угол поворота [head, body, tail] змейки согласно его направлению
    _dir_turn_angle_SBI = {
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
                   if os.path.exists(path_to_bg)
                   else None)

    def _draw_snake(self):
        pointer = 0
        prev_sp = None
        for sp in self.field.snake:
            location = (sp.location.y * self.size_cell,
                        sp.location.x * self.size_cell)
            if pointer == 0:
                _draw_image(self.surface,
                            self._snake_head,
                            *location,
                            rotate_angle=self._dir_turn_angle_SBI[sp.direction])

            elif pointer == len(self.field.snake) - 1:
                _draw_image(self.surface,
                            self._snake_tail,
                            *location,
                            rotate_angle=self._dir_turn_angle_SBI[prev_sp.direction])

            else:
                if prev_sp.direction == sp.direction:
                    _draw_image(self.surface,
                                self._snake_body,
                                *location,
                                rotate_angle=self._dir_turn_angle_SBI[sp.direction])
                else:
                    _draw_image(self.surface,
                                self._snake_turn,
                                *location,
                                rotate_angle=self._dir_turn_angle_STI[sp.direction, prev_sp.direction])

            prev_sp = sp
            pointer += 1

    def _draw_food(self):
        for location, food in self.field.foods_location.items():
            _draw_image(
                self.surface,
                self._food_image[food],
                location.y * self.size_cell,
                location.x * self.size_cell)

    def _draw_walls(self):
        for location in self.field.walls:
            _draw_image(
                self.surface,
                self._wall,
                location.y * self.size_cell,
                location.x * self.size_cell)

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
    _toolbar = _load_image('toolbar')

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

        self.field_drawer = FieldDrawing(level.field,
                                         settings.background_image(level.name),
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
        for i in range(self.level.field.width):
            _draw_image(self.surface, self._toolbar, 0, i * self.size_cell)
            _draw_image(self.surface, self._toolbar, self.size_cell, i * self.size_cell)

        for i in range(self.level.health):
            _draw_image(self.surface, self._heart,
                        self.delta_y / 2 - 8, self.size_cell + 24 * i)

        # пишет счёт у данного уровня
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(f'Score: {self.level.score}/{self.level.max_score}', True, pygame.Color('white'))
        s_rect = s_surf.get_rect()
        s_rect.topleft = ((self.surface.get_width() - s_rect.width) / 2,
                          (self.delta_y - s_rect.height) / 2)
        self.surface.blit(s_surf, s_rect)

        # пишет какой уровень сейчас и сколько в общем
        lvl_font = pygame.font.SysFont('monaco', 24)
        lvl_surf = lvl_font.render(f'Level: {self.level_number}/{self.count_levels}', True, pygame.Color('white'))
        lvl_rect = lvl_surf.get_rect()
        lvl_rect.topleft = (self.surface.get_width() - 20 - lvl_rect.width,
                            (self.delta_y - s_rect.height) / 2)
        self.surface.blit(lvl_surf, lvl_rect)


class FreeGameDrawing(GameDrawing):
    def __init__(self, level: Level):
        super().__init__(level, delta_y=self.size_cell * 2)

    def _draw_toolbar(self):
        for i in range(self.level.field.width):
            _draw_image(self.surface, self._toolbar, 0, i * self.size_cell)
            _draw_image(self.surface, self._toolbar, self.size_cell, i * self.size_cell)

        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(f'Score: {self.level.score}', True, pygame.Color('white'))
        s_rect = s_surf.get_rect()
        s_rect.topleft = ((self.surface.get_width() - s_rect.width) / 2,
                          (self.delta_y - s_rect.height) / 2)
        self.surface.blit(s_surf, s_rect)
