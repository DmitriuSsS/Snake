import random

from game.entities import Food, Level, Field, Snake
from game.direction import *
from game.drawing.windows import *
from game.drawing.game_drawing import *
from game.events import *
from game.settings import Settings
import pygame
pygame.init()

settings = Settings()


class Game:
    clock = pygame.time.Clock()
    fps = 120

    @staticmethod
    def _get_direction():
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key in TranslateDirection.direction:
                    return TranslateDirection.direction[i.key]

    def game_maker_loop(self, width_field, height_field, score_for_win):
        # TODO: реализовать
        field = Field(Snake([]), set(), (width_field, height_field))
        level = Level(field=field, max_score=score_for_win)
        game_maker_drawer = GameMakerDrawing(level)
        while True:
            game_maker_drawer.draw()
            pygame.display.flip()

        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)

    def free_game_loop(self):
        level = Level('free', 1)
        level.max_score = len(level.field.not_walls_cells) - len(level.field.snake)
        game_drawing = FreeGameDrawing(level)
        self._game_loop(level, game_drawing)

        redirect = RedirectToEndFreeGameWindow(level.score)
        pygame.event.post(redirect.event)

    def level_game_loop(self, health):
        levels = settings.levels

        for i in range(len(levels)):
            level = Level(levels[i], health)
            level_drawing = LevelDrawing(level, i + 1, len(levels))
            health = self._game_loop(level, level_drawing)
            if not health:
                redirect = RedirectToGameOverWindow()
                break
        else:
            redirect = RedirectToWinWindow()

        pygame.event.post(redirect.event)

    def _game_loop(self, level, game_drawing):
        tick = 0
        while not level.win_flag and not level.game_over_flag:
            self.clock.tick(self.fps)
            self.step_game(level, tick, game_drawing)
            tick += 1
        return level.health

    not_basic_food = [Food(*t) for t in settings.not_basic_food]
    _generate_food_location = None

    def step_game(self, level: Level, tick, game_drawing: GameDrawing):
        tick_move = self.fps // level.field.snake.speed
        if not tick_move or not tick % tick_move:
            level.step_snake(self._get_direction())
            if len(level.field.foods_location) <= 1:
                level.field.generate_food()
            game_drawing.draw()
            pygame.display.flip()

        if not (tick - 1) % (self.fps * 5):
            if self._generate_food_location in level.field.foods_location:
                level.field.foods_location.pop(self._generate_food_location)
            self._generate_food_location = \
                level.field.generate_food(random.choice(self.not_basic_food))
            game_drawing.draw()
            pygame.display.flip()

    def main_loop(self):
        pygame.display.set_caption('Snake Game')
        pygame.display.set_icon(pygame.image.load(settings.picture('icon')))

        current_window = Menu()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONUP:
                    for button in current_window.buttons:
                        if button.is_pressed(e.pos):
                            button.handler()
                elif e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.USEREVENT:
                    if e.name == RedirectToFreeGame.name:
                        self.free_game_loop()
                    elif e.name == RedirectToLevelGame.name:
                        self.level_game_loop(3)
                    elif e.name == RedirectToGameMaker.name:
                        self.game_maker_loop(e.width, e.height, e.score)
                    elif e.name == RedirectToMenu.name:
                        current_window = Menu()
                    elif e.name == RedirectToGameOverWindow.name:
                        current_window = GameOverWindow()
                    elif e.name == RedirectToWinWindow.name:
                        current_window = WinWindow()
                    elif e.name == RedirectToEndFreeGameWindow.name:
                        current_window = EndFreeGameWindow(e.score)
                    elif e.name == RedirectToSetGameMakerProperty.name:
                        current_window = GameMakerWindow()

            current_window.draw()
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
