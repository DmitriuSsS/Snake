import os

import pygame

from game.direction import Direction
from game.entities import Food
from game.entities import Level
from game.settings import Settings

settings = Settings()

__all__ = ['GameDrawing', 'FieldDrawing', 'FreeGameDrawing', 'LevelDrawing']


def _load_image(name):
    return pygame.image.load(settings.picture(name))


def _draw_image(play_surface, image, left, top, rotate_angle=0):
    if rotate_angle:
        image = pygame.transform.rotate(image, rotate_angle)
    rect_image = image.get_rect(topleft=(top, left))
    play_surface.blit(image, rect_image)


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
