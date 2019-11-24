import random

from game.entities import Food, Level
from game.direction import *
from game.drawing import *
from game.settings import Settings
import pygame
pygame.init()

settings = Settings()


class Game:
    clock = pygame.time.Clock()
    fps = 120

    _generate_food_location = None

    @staticmethod
    def _get_direction():
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key in TranslateDirection.direction:
                    return TranslateDirection.direction[i.key]

    def free_game_loop(self):
        level = Level('free', 1)
        tick = 0
        level_drawing = FreeGameDrawing(level)
        while not level.game_over_flag:
            self.clock.tick(self.fps)
            self.step_game(level, tick, level_drawing)
            tick += 1
        return level.score

    def level_game_loop(self, name, health, level_number, total_number_levels):
        level = Level(name, health)
        tick = 0
        level_drawing = LevelDrawing(level, level_number, total_number_levels)
        while not level.win_flag and not level.game_over_flag:
            self.clock.tick(self.fps)
            self.step_game(level, tick, level_drawing)
            tick += 1
        return level.health

    not_basic_food = [Food(*t) for t in settings.not_basic_food]

    def step_game(self, level: Level, tick, level_drawing):
        tick_move = self.fps // level.field.snake.speed
        if not tick_move or not tick % tick_move:
            level.step_snake(self._get_direction())
            if len(level.field.foods_location) <= 1:
                level.field.generate_food()
            level_drawing.draw()
            pygame.display.flip()

        if not (tick - 1) % (self.fps * 5):
            if self._generate_food_location in level.field.foods_location:
                level.field.foods_location.pop(self._generate_food_location)
            self._generate_food_location = \
                level.field.generate_food(random.choice(self.not_basic_food))
            level_drawing.draw()
            pygame.display.flip()

    def main_loop(self):
        windows = {
            'menu': Menu,
            'windows level game': WinWindow,
            'lose level game': GameOverWindow,
            'end of the free game': WinFreeGameWindow
        }

        pygame.display.set_caption('Snake Game')
        name_window = 'menu'
        current_window = windows[name_window]()

        while True:
            if type(current_window) is not windows[name_window]:
                current_window = windows[name_window]()
            current_window.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for button in current_window.buttons:
                        if button.is_pressed(pos):
                            name_window = button.href
                            break
                if name_window == 'level game':
                    levels = settings.levels

                    health = 3
                    for i in range(len(levels)):
                        health = self.level_game_loop(levels[i], health, i + 1, len(levels))
                        if not health:
                            name_window = 'lose level game'
                            break
                    else:
                        name_window = 'windows level game'
                elif name_window == 'free game':
                    score = self.free_game_loop()
                    name_window = 'end of the free game'
                    current_window = WinFreeGameWindow(score)

            pygame.display.flip()
