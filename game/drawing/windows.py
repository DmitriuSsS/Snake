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
        rect = text_lose.get_rect()
        rect.centerx = self.surface.get_width() / 2
        rect.top = self._indent_from_edges
        self.surface.blit(text_lose, rect)

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
        rect_header = text_win.get_rect()
        rect_header.centerx = self.surface.get_width() / 2
        rect_header.top = self._indent_from_edges
        self.surface.blit(text_win, rect_header)

        text_score = self._font_text_score.render(self._text_score, True, self._text_color)
        rect_score = text_score.get_rect()
        rect_score.centerx = rect_header.centerx
        rect_score.top = rect_header.bottom + self._indent_between_components
        self.surface.blit(text_score, rect_score)

        for button in self.buttons:
            button.draw()

    @staticmethod
    def _redirect_to_menu():
        redirect = RedirectToMenu()
        pygame.event.post(redirect.event)


class GameMakerWindow:
    def __init__(self):
        self._size_window = (250, 280)

        self.surface = pygame.display.set_mode(self._size_window)

        # region настройка размеров кнопок, текста и блоков

        self._indent_from_edges = 10
        self._indent_between_components = 10

        borders = 2 * self._indent_from_edges
        height_work_area = self._size_window[1] - borders
        width_work_area = self._size_window[0] - borders

        self._size_cancel_go_buttons = (
            (width_work_area - self._indent_between_components) / 2,
            int(self._size_window[1] * 0.15)
        )
        top_for_cancel_go_buttons = self._size_window[1] - self._indent_from_edges - self._size_cancel_go_buttons[1]

        self._height_heading = int(self._size_window[1] * 0.15)

        self._size_block = (
            width_work_area,
            (height_work_area - self._height_heading - self._size_cancel_go_buttons[1]
             - self._indent_between_components) / 3
        )

        self._size_change_value_button = (
            (self._size_block[0] - 4 * self._indent_between_components) / 5,
            int((self._size_block[1] - 2 * self._indent_between_components) * 0.5)
        )

        self._text_heading = 'Set Game Properties'
        self._font_heading = pygame.font.SysFont(
            "Calibri",
            get_size_for_calibri(width_work_area, self._height_heading, self._text_heading)
        )

        self._border_for_value = {
            'score': [5, 100],
            'width': [10, 100],
            'height': [10, 100]
        }

        self._header_for_value = {
            'score':
                f'Score for win({self._border_for_value["score"][0]} <= s <= {self._border_for_value["score"][1]})',
            'width':
                f'Width({self._border_for_value["width"][0]} <= w <= {self._border_for_value["width"][1]})',
            'height':
                f'Height({self._border_for_value["height"][0]} <= h <= {self._border_for_value["height"][1]})'
        }

        # Так как у score самая большая строка
        self._font_heading_value = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                self._size_block[0],
                int(self._size_block[1] * 0.6),
                self._header_for_value['score']
            )
        )

        self._font_write_value = pygame.font.SysFont(
            'Calibri',
            get_size_for_calibri(
                int(width_work_area - 4 * (self._size_change_value_button[0] + self._indent_between_components)),
                int(0.35 * self._size_block[1]),
                '000'
            )
        )

        # endregion

        self.surface = pygame.display.set_mode(self._size_window)
        self.buttons = [
            Button(self.surface,
                   pygame.Rect(
                       self._indent_from_edges,
                       top_for_cancel_go_buttons,
                       *self._size_cancel_go_buttons
                   ),
                   'Cancel',
                   handler=self._cancel),
            Button(self.surface,
                   pygame.Rect(
                       self._size_window[0] - self._indent_from_edges - self._size_cancel_go_buttons[0],
                       top_for_cancel_go_buttons,
                       *self._size_cancel_go_buttons
                   ),
                   'GO',
                   handler=self._go)]

        self._y_for_block = {}
        self._properties_names = ['height', 'width', 'score']
        for i in range(len(self._properties_names)):
            _property = self._properties_names[i]
            self._y_for_block[_property] = self._height_heading + i * self._size_block[1]
            self._add_plus_minus_buttons(_property,
                                         self._y_for_block[_property] +
                                         self._size_block[1] -
                                         self._size_change_value_button[1] - self._indent_between_components / 2)

        self._bg_color = pygame.Color('white')
        self._text_color = pygame.Color('black')

        self._height = 10
        self._width = 10
        self._score_for_win = 5

    def draw(self):
        self.surface.fill(self._bg_color)
        render_text = self._font_heading.render(self._text_heading, True, self._text_color)
        rect = render_text.get_rect()
        rect.centerx = self.surface.get_width() / 2
        rect.centery = self._height_heading / 2
        self.surface.blit(render_text, rect)

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

        # region задание параметров rect для кнопок

        minus_10_rect = pygame.Rect(
            self._indent_from_edges, y,
            *self._size_change_value_button
        )

        minus_1_rect = pygame.Rect(
            minus_10_rect.right + self._indent_between_components, y,
            *self._size_change_value_button
        )

        plus_10_rect = pygame.Rect(
            self.surface.get_width() - self._size_change_value_button[0] - self._indent_from_edges, y,
            *self._size_change_value_button
        )

        plus_1_rect = pygame.Rect(
            plus_10_rect.left - self._size_change_value_button[0] - self._indent_between_components, y,
            *self._size_change_value_button
        )

        # endregion

        buttons = [
            Button(
                self.surface,
                minus_10_rect,
                text='-10',
                handler=self._change_arg(name_arg, -10, *self._border_for_value[name_arg]),
                width_circle=1
            ),
            Button(
                self.surface,
                minus_1_rect,
                text='--',
                handler=self._change_arg(name_arg, -1, *self._border_for_value[name_arg]),
                width_circle=1
            ),
            Button(
                self.surface,
                plus_1_rect,
                text='+',
                handler=self._change_arg(name_arg, 1, *self._border_for_value[name_arg]),
                width_circle=1
            ),
            Button(
                self.surface,
                plus_10_rect,
                text='+10',
                handler=self._change_arg(name_arg, 10, *self._border_for_value[name_arg]),
                width_circle=1
            )
        ]
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
        text = self._header_for_value[name_arg]

        y = self._y_for_block[name_arg]
        render_text = self._font_heading_value.render(text, True, self._text_color)
        rect = render_text.get_rect()
        rect.centerx = self.surface.get_width() / 2
        rect.top = y + self._indent_between_components
        self.surface.blit(render_text, rect)

        _values = {
            'score': self._score_for_win,
            'height': self._height,
            'width': self._width
        }

        value = str(_values[name_arg])
        render_text = self._font_write_value.render(value, True, self._text_color)
        rect = render_text.get_rect()
        rect.centerx = self.surface.get_width() / 2
        rect.centery = \
            y + self._size_block[1] - self._indent_between_components / 2 - self._size_change_value_button[1] / 2
        self.surface.blit(render_text, rect)
