import pygame
from game.drawing.components import *
from game.events import *

__all__ = ['Menu', 'WinWindow', 'GameOverWindow',
           'EndFreeGameWindow', 'GameMakerWindow']


class Menu:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 10, 160, 40, 'Game with Levels',
                               handler=self._redirect_to_level_game),
                        Button(self.surface, 20, 60, 160, 40, 'Free game',
                               handler=self._redirect_to_free_game),
                        Button(self.surface, 20, 110, 75, 40, 'GM',
                               handler=self._redirect_to_game_maker),
                        Button(self.surface, 105, 110, 75, 40, 'Exit',
                               handler=self._exit)]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        for button in self.buttons:
            button.draw()

    @staticmethod
    def _redirect_to_level_game():
        redirect = RedirectToLevelGame()
        pygame.event.post(redirect.event)

    @staticmethod
    def _redirect_to_free_game():
        redirect = RedirectToFreeGame()
        pygame.event.post(redirect.event)

    @staticmethod
    def _redirect_to_game_maker():
        redirect = RedirectToSetGameMakerProperty()
        pygame.event.post(redirect.event)

    @staticmethod
    def _exit():
        pygame.event.post(pygame.event.Event(pygame.QUIT))


class WinWindow:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK',
                               handler=self._redirect_to_menu)]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_win = pygame.font.SysFont("Calibri", 40)
        text_win = font_win.render('You WIN!', True, pygame.Color('black'))
        self.surface.blit(text_win, ((self.surface.get_width() - text_win.get_width()) / 2, 30))
        for button in self.buttons:
            button.draw()

    @staticmethod
    def _redirect_to_menu():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)


class GameOverWindow:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK',
                               handler=self._redirect_to_menu)]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_lose = pygame.font.SysFont("Calibri", 30)
        text_lose = font_lose.render('Game Over :(', True, pygame.Color('black'))
        self.surface.blit(text_lose, ((self.surface.get_width() - text_lose.get_width()) / 2, 30))
        for button in self.buttons:
            button.draw()

    @staticmethod
    def _redirect_to_menu():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)


class EndFreeGameWindow:
    def __init__(self, score):
        self.score = score
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK',
                               handler=self._redirect_to_menu)]

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

    @staticmethod
    def _redirect_to_menu():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)


class GameMakerWindow:
    def __init__(self):
        self._height_block = 60
        self._height_heading = 40
        self._height_button_plus = 20
        self.surface = pygame.display.set_mode((250, self._height_heading + 3 * self._height_block + 60))

        width_buttons_cancel_and_go = (self.surface.get_width() - 50) / 2
        y_for_buttons_cancel_and_go = self._height_heading + 3 * self._height_block + 10
        self.buttons = [Button(self.surface,
                               20, y_for_buttons_cancel_and_go,
                               width_buttons_cancel_and_go, 40,
                               'Cancel',
                               handler=self._cancel),
                        Button(self.surface,
                               30 + width_buttons_cancel_and_go, y_for_buttons_cancel_and_go,
                               width_buttons_cancel_and_go, 40,
                               'GO',
                               handler=self._go)]

        self._y_for_block = {}
        self._properties_names = ['height', 'width', 'score']
        for i in range(len(self._properties_names)):
            _property = self._properties_names[i]
            self._y_for_block[_property] = self._height_heading + i * self._height_block
            self._add_plus_minus_buttons(_property,
                                         self._y_for_block[_property] +
                                         self._height_block -
                                         self._height_button_plus - 5)

        self._height = 5
        self._width = 5
        self._score_for_win = 5

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font = pygame.font.SysFont("Calibri", 25)
        render_text = font.render('Set Game Properties', True, pygame.Color('black'))
        self.surface.blit(render_text, ((self.surface.get_width() - render_text.get_width()) / 2, 10))
        for _property in self._properties_names:
            self._draw_text(_property)
            pygame.draw.line(self.surface, pygame.Color('grey'),
                             (0, self._y_for_block[_property]),
                             (self.surface.get_width(), self._y_for_block[_property]))
        for button in self.buttons:
            button.draw()

    @staticmethod
    def _cancel():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)

    def _go(self):
        redirect = RedirectToGameMaker(self._width, self._height, self._score_for_win)
        pygame.event.post(redirect.event)

    def _add_plus_minus_buttons(self, name_arg, y):
        x = 10
        button_size = (30, self._height_button_plus)
        buttons = [Button(self.surface, x, y, *button_size, '-10',
                          handler=self._change_arg(name_arg, -10)),
                   Button(self.surface, x + button_size[0] + 5, y, *button_size, '--',
                          handler=self._change_arg(name_arg, -1)),
                   Button(self.surface, self.surface.get_width() - x - 2 * button_size[0] - 5, y,
                          *button_size, '+',
                          handler=self._change_arg(name_arg, 1)),
                   Button(self.surface, self.surface.get_width() - x - button_size[0], y,
                          *button_size, '+10',
                          handler=self._change_arg(name_arg, 10))]
        self.buttons += buttons

    def _change_arg(self, name_arg, value_change):
        """
        :param name_arg: [score, width, height]
        :return: func
        """
        left_border, right_border = 5, 100
        def _change():
            if name_arg == 'score':
                temp_score = self._score_for_win + value_change
                if left_border <= temp_score <= right_border:
                    self._score_for_win = temp_score
            elif name_arg == 'width':
                temp_width = self._width + value_change
                if left_border <= temp_width <= right_border:
                    self._width = temp_width
            elif name_arg == 'height':
                temp_height = self._height + value_change
                if left_border <= temp_height <= right_border:
                    self._height = temp_height

        return _change

    def _draw_text(self, name_arg):
        """
        :param name_arg: [score, width, height]
        """
        text = name_arg
        if name_arg == 'score':
            text += ' for win'
        text += f'(5 <= {name_arg[0]} <= 100)'

        y = self._y_for_block[name_arg]
        font = pygame.font.SysFont("Calibri", 17)
        render_text = font.render(text, True, pygame.Color('black'))
        self.surface.blit(render_text, ((self.surface.get_width() - render_text.get_width()) / 2, y + 10))

        _values = {
            'score': self._score_for_win,
            'height': self._height,
            'width': self._width
        }
        value = str(_values[name_arg])
        font = pygame.font.SysFont("Calibri", 17)
        render_text = font.render(value, True, pygame.Color('black'))
        self.surface.blit(render_text, ((self.surface.get_width() - render_text.get_width()) / 2,
                                        y + self._height_block - 5
                                        - (self._height_button_plus + render_text.get_height()) / 2))
