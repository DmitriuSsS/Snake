import pygame
from game.drawing.components import *
from game.events import *

__all__ = ['Menu', 'GameOverWindow', 'EndFreeGameWindow', 'GameMakerWindow']


class Menu:
    def __init__(self):
        self._size_window = (200, 160)

        # region настройка расположения и размеров кнопок
        delta_x = 20
        distance_between_buttons = 10
        height_buttons = (self._size_window[1] - 4 * distance_between_buttons) // 3

        self._rect_button_level_game = pygame.Rect(
            delta_x,
            distance_between_buttons,
            self._size_window[0] - 2 * delta_x,
            height_buttons
        )

        self._rect_button_free_game = self._rect_button_level_game.copy()
        self._rect_button_free_game.y = (self._rect_button_level_game.bottom +
                                         distance_between_buttons)

        width_button_game_maker = (self._size_window[0] - 2 * delta_x - distance_between_buttons) // 2
        self._rect_button_game_maker = pygame.Rect(
            delta_x,
            self._rect_button_free_game.bottom + distance_between_buttons,
            width_button_game_maker,
            height_buttons
        )

        self._rect_button_exit = self._rect_button_game_maker.copy()
        self._rect_button_exit.x = self._rect_button_game_maker.right + distance_between_buttons

        # endregion

        self.surface = pygame.display.set_mode(self._size_window)
        self.buttons = [
            Button(self.surface, self._rect_button_level_game,
                   text='Game with Levels',
                   handler=self._redirect_to_level_game),
            Button(self.surface, self._rect_button_free_game,
                   text='Free game',
                   handler=self._redirect_to_free_game),
            Button(self.surface, self._rect_button_game_maker,
                   text='GM',
                   handler=self._redirect_to_game_maker),
            Button(self.surface, self._rect_button_exit,
                   text='Exit',
                   handler=self._exit)
        ]

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


class GameOverWindow:
    def __init__(self, message):
        self._size_window = (200, 160)

        # region настройка размеров и положения кнопок и текста

        self._indent_from_edges = 20
        self._rect_button_redirect_to_menu = pygame.Rect(
            self._indent_from_edges,
            self._size_window[1] * 3 // 4 - self._indent_from_edges,
            self._size_window[0] - 2 * self._indent_from_edges,
            self._size_window[1] // 4
        )

        height_text = self._rect_button_redirect_to_menu.top - 2 * self._indent_from_edges
        self._text = message
        self._font = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                self._size_window[0] - 2 * self._indent_from_edges,
                height_text,
                self._text
            )
        )

        # endregion

        self._bg_color = pygame.Color('white')
        self._text_color = pygame.Color('black')

        self.surface = pygame.display.set_mode(self._size_window)
        self.buttons = [Button(self.surface, self._rect_button_redirect_to_menu, 'OK',
                               handler=self._redirect_to_menu)]

    def draw(self):
        self.surface.fill(self._bg_color)
        text_lose = self._font.render(self._text, True, self._text_color)
        self.surface.blit(text_lose, ((self.surface.get_width() - text_lose.get_width()) / 2, self._indent_from_edges))
        for button in self.buttons:
            button.draw()

    @staticmethod
    def _redirect_to_menu():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)


class EndFreeGameWindow:
    def __init__(self, score):
        self._size_window = (200, 160)

        # region настройка размеров и положения кнопок и текста

        self._indent_from_edges = 20
        self._indent_between_components = 10

        self._rect_button_redirect_to_menu = pygame.Rect(
            self._indent_from_edges,
            self._size_window[1] * 3 // 4 - self._indent_from_edges,
            self._size_window[0] - 2 * self._indent_from_edges,
            self._size_window[1] // 4
        )

        self._text_header = 'End of the Game'
        self._text_score = f'Score: {score}'
        height_text = self._rect_button_redirect_to_menu.top - self._indent_from_edges - self._indent_between_components
        title_space = 0.65
        height_header = int(title_space * height_text)
        height_text_score = int((1 - title_space) * height_text)

        self._font_header = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                self._size_window[0] - 2 * self._indent_from_edges,
                height_header,
                self._text_header
            )
        )

        self._font_text_score = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                int((self._size_window[0] - 2 * self._indent_from_edges) * 0.6),
                height_text_score,
                self._text_score
            )
        )

        # endregion

        self._bg_color = pygame.Color('white')
        self._text_color = pygame.Color('black')

        self.surface = pygame.display.set_mode(self._size_window)
        self.buttons = [Button(self.surface, self._rect_button_redirect_to_menu,
                               text='OK',
                               handler=self._redirect_to_menu)]

    def draw(self):
        self.surface.fill(self._bg_color)
        text_win = self._font_header.render(self._text_header, True, self._text_color)
        self.surface.blit(text_win, ((self.surface.get_width() - text_win.get_width()) / 2, self._indent_from_edges))

        text_score = self._font_text_score.render(self._text_score, True, self._text_color)
        self.surface.blit(text_score, (
            (self.surface.get_width() - text_score.get_width()) / 2,
            self._indent_from_edges + text_win.get_rect().height + self._indent_between_components)
        )
        for button in self.buttons:
            button.draw()

    @staticmethod
    def _redirect_to_menu():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)


# TODO: дорефакторить

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

        self._height = 10
        self._width = 10
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
        border = [10, 100]
        if name_arg == 'score':
            border[0] = 5
        buttons = [Button(self.surface, x, y, *button_size, '-10',
                          handler=self._change_arg(name_arg, -10, *border)),
                   Button(self.surface, x + button_size[0] + 5, y, *button_size, '--',
                          handler=self._change_arg(name_arg, -1, *border)),
                   Button(self.surface, self.surface.get_width() - x - 2 * button_size[0] - 5, y,
                          *button_size, '+',
                          handler=self._change_arg(name_arg, 1, *border)),
                   Button(self.surface, self.surface.get_width() - x - button_size[0], y,
                          *button_size, '+10',
                          handler=self._change_arg(name_arg, 10, *border))]
        self.buttons += buttons

    def _change_arg(self, name_arg, value_change, left_border, right_border):
        """
        :param name_arg: [score, width, height]
        :return: func
        """

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
            text += ' for win(5 <= s <= 100)'
        else:
            text += f'(10 <= {name_arg[0]} <= 100)'

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
