import random

from game.entities import Food, Level
from game.direction import *
from game.drawing.windows import *
from game.drawing.game_drawing import *
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
        level_drawing.draw()
        pygame.display.flip()
        while not level.game_over_flag:
            self.clock.tick(self.fps)
            self.step_game(level, tick, level_drawing)
            tick += 1

        window = EndFreeGameWindow(score=level.score)
        run = True
        while run:
            window.draw()
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    if window.buttons[0].is_pressed(e.pos):
                        run = False
                        break

        return Menu()

    def level_game_loop(self, health):
        levels = settings.levels

        for i in range(len(levels)):
            health = self._level_game_loop(levels[i], health, i + 1, len(levels))
            if not health:
                window = GameOverWindow()
                break
        else:
            window = WinWindow()

        run = True
        while run:
            window.draw()
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    if window.buttons[0].is_pressed(e.pos):
                        run = False
                        break

        return Menu()

    def _level_game_loop(self, name, health, level_number, total_number_levels):
        level = Level(name, health)
        tick = 0
        level_drawing = LevelDrawing(level, level_number, total_number_levels)
        level_drawing.draw()
        pygame.display.flip()
        while not level.win_flag and not level.game_over_flag:
            self.clock.tick(self.fps)
            self.step_game(level, tick, level_drawing)
            tick += 1
        return level.health

    not_basic_food = [Food(*t) for t in settings.not_basic_food]

    def step_game(self, level: Level, tick, level_drawing: GameDrawing):
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
        pygame.display.set_caption('Snake Game')
        pygame.display.set_icon(pygame.image.load(settings.picture('icon')))
        current_window = Menu()
        name_window = ''

        while True:
            current_window.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    for button in current_window.buttons:
                        if button.is_pressed(e.pos):
                            name_window = button.href
                            break
                if name_window != '':
                    if name_window == 'level game':
                        current_window = self.level_game_loop(3)
                    elif name_window == 'free game':
                        current_window = self.free_game_loop()

                    name_window = ''

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
