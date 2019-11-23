import os

import pygame

from game.direction import Direction
from game.entities import Food
from game.entities import Level
from game.settings import Settings


settings = Settings()


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


class WinFreeGameWindow:
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

    wall = _load_image('wall')
    basic_food = _load_image('basic_apple')
    gold_apple = _load_image('gold_apple')
    wormy_apple = _load_image('wormy_apple')
    high_speed_apple = _load_image('high_speed_apple')
    heart = _load_image('heart')
    snake_body = _load_image('snake_body')
    snake_head = _load_image('snake_head')
    snake_tail = _load_image('snake_tail')
    snake_turn = _load_image('snake_turn')
    toolbar = _load_image('toolbar')

    # endregion

    food_image = {Food(*food): _load_image(name)
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
    dir_turn_angle_STI = {
        (Direction.RIGHT, Direction.UP): 180,
        (Direction.DOWN, Direction.LEFT): 180,
        (Direction.UP, Direction.RIGHT): 0,
        (Direction.LEFT, Direction.DOWN): 0,
        (Direction.UP, Direction.LEFT): -90,
        (Direction.RIGHT, Direction.DOWN): -90,
        (Direction.LEFT, Direction.UP): 90,
        (Direction.DOWN, Direction.RIGHT): 90
    }

    def __init__(self, field, path_to_bg):
        self.field = field
        self.bg = (pygame.image.load(path_to_bg)
                   if os.path.exists(path_to_bg)
                   else None)

    def _draw_snake(self, surface):
        pointer = 0
        prev_sp = None
        for sp in self.field.snake:
            location = (sp.location.y * self.size_cell,
                        sp.location.x * self.size_cell)
            if pointer == 0:
                _draw_image(surface,
                            self.snake_head,
                            *location,
                            rotate_angle=self.dir_turn_angle_SBI[sp.direction])

            elif pointer == len(self.field.snake) - 1:
                _draw_image(surface,
                            self.snake_tail,
                            *location,
                            rotate_angle=self.dir_turn_angle_SBI[prev_sp.direction])

            else:
                if prev_sp.direction == sp.direction:
                    _draw_image(surface,
                                self.snake_body,
                                *location,
                                rotate_angle=self.dir_turn_angle_SBI[sp.direction])
                else:
                    _draw_image(surface,
                                self.snake_turn,
                                *location,
                                rotate_angle=self.dir_turn_angle_STI[sp.direction, prev_sp.direction])

            prev_sp = sp
            pointer += 1

    def _draw_food(self, surface):
        for location, food in self.field.foods_location.items():
            _draw_image(
                surface,
                self.food_image[food],
                location.y * self.size_cell,
                location.x * self.size_cell)

    def _draw_walls(self, surface):
        for location in self.field.walls:
            _draw_image(
                surface,
                self.wall,
                location.y * self.size_cell,
                location.x * self.size_cell)

    def _draw_bg(self, surface):
        if self.bg is not None:
            surface.blit(self.bg, (0, 0))
        else:
            surface.fill(pygame.Color('white'))

    def draw(self, surface):
        self._draw_bg(surface)
        self._draw_snake(surface)
        self._draw_walls(surface)
        self._draw_food(surface)


class LevelDrawing(FieldDrawing):
    def __init__(self, level: Level, level_number: int, count_levels: int):
        super().__init__(level.field, settings.background_image(level.name))
        self.delta_y = settings.height_toolbar
        self.surface = pygame.display.set_mode((self.size_cell * self.field.width,
                                                self.size_cell * self.field.height + self.delta_y))
        self.field_surface = self.surface.subsurface(
            pygame.Rect(0, self.delta_y, self.surface.get_width(), self.surface.get_height() - self.delta_y))

        self.level = level
        self.level_number = level_number
        self.count_levels = count_levels

    def _draw_toolbar(self):
        for i in range(self.field.width):
            _draw_image(self.surface, self.toolbar, 0, i * self.size_cell)
            _draw_image(self.surface, self.toolbar, self.size_cell, i * self.size_cell)

        for i in range(self.level.health):
            _draw_image(self.surface, self.heart,
                        self.delta_y / 2 - 8, self.size_cell + 24 * i)

        # пишет счёт у данного уровня
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(f'Score: {self.level.score}/{self.level.max_score}', True, pygame.Color('white'))
        s_rect = s_surf.get_rect()
        s_rect.topleft = (self.surface.get_width() - s_rect.width) / 2, (self.delta_y - s_rect.height) / 2
        self.surface.blit(s_surf, s_rect)

        # пишет какой уровень сейчас и сколько в общем
        lvl_font = pygame.font.SysFont('monaco', 24)
        lvl_surf = lvl_font.render(f'Level: {self.level_number}/{self.count_levels}',
                                   True, pygame.Color('white'))
        lvl_rect = lvl_surf.get_rect()
        lvl_rect.topleft = (self.field.width * self.size_cell - 20 - lvl_rect.width,
                            max((self.delta_y - s_rect.height) / 2, 8))
        self.surface.blit(lvl_surf, lvl_rect)

    def draw(self, field_surface=None):
        if field_surface is None:
            field_surface = self.field_surface
        super().draw(field_surface)
        self._draw_toolbar()


class FreeGameDrawing(FieldDrawing):
    def __init__(self, level: Level):
        super().__init__(level.field, settings.background_image(level.name))
        self.delta_y = settings.height_toolbar
        self.surface = pygame.display.set_mode((self.size_cell * self.field.width,
                                                self.size_cell * self.field.height + self.delta_y))
        self.field_surface = self.surface.subsurface(
            pygame.Rect(0, self.delta_y, self.surface.get_width(), self.surface.get_height() - self.delta_y))

        self.level = level

    def _draw_toolbar(self):
        for i in range(self.field.width):
            _draw_image(self.surface, self.toolbar, 0, i * self.size_cell)
            _draw_image(self.surface, self.toolbar, self.size_cell, i * self.size_cell)

        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(f'Score: {self.level.score}', True, pygame.Color('white'))
        s_rect = s_surf.get_rect()
        s_rect.topleft = (self.field.width * self.size_cell - s_rect.width) / 2, (self.delta_y - s_rect.height) / 2
        self.surface.blit(s_surf, s_rect)

    def draw(self, field_surface=None):
        if field_surface is None:
            field_surface = self.field_surface
        super().draw(field_surface)
        self._draw_toolbar()
