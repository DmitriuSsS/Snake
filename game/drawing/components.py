import pygame
import time

from game.direction import Direction, TranslateDirection

__all__ = ['Button', 'TextArea']


class Button:
    def __init__(self,
                 parent_surface,
                 x, y,
                 width, height,
                 text, text_color=pygame.Color('black'),
                 button_color=pygame.Color('white'),
                 href=None,
                 name=None):
        self.parent_surface = parent_surface
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


class TextArea:
    def __init__(self,
                 parent_surface,
                 x, y,
                 width, height):
        self.parent_surface = parent_surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._rect = pygame.Rect(x, y, width, height)

        self._text = []
        self._cursor_position = 0
        self._font = 'Consolas'
        self._delta_x = 10
        self._active = False
        self._last_keydown = None
        self._tick_last_keydown = 0

        self._font_size, self._width_letter, self._height_letter = self._set_font_size()
        self._delta_y = (self.height - self._height_letter) / 2

    def _set_font_size(self):
        font_size = self.height * 4 // 5 - 1

        font = pygame.font.SysFont(self._font, font_size)
        text = font.render('Ag', True, pygame.Color('black'))
        return font_size, text.get_width() // 2, text.get_height()

    def _write_letter(self, letter: str):
        """
        Перестаёт добавлять буквы если получающийся текст по ширине больше окна
        """
        text_lt_width = (self.width < self._delta_x * 2 +
                         self._width_letter * (len(self._text) + 1))
        if letter != '' and text_lt_width:
            if self._cursor_position == len(self._text):
                self._text.append(letter)
            else:
                self._text.insert(self._cursor_position, letter)
            self._cursor_position += 1

    def _delete_letter(self, mode='delete'):
        if mode == 'delete':
            if self._cursor_position < len(self._text):
                self._text.pop(self._cursor_position)
        elif mode == 'backspace':
            if self._cursor_position > 0:
                self._cursor_position -= 1
                self._text.pop(self._cursor_position)
        else:
            raise ValueError('mode не опознан')

    def get_text(self):
        return ''.join(self._text)

    def _move_cursor(self, direction: Direction):
        if direction == Direction.RIGHT:
            if self._cursor_position < len(self._text):
                self._cursor_position += 1
        elif direction == Direction.LEFT:
            if self._cursor_position > 0:
                self._cursor_position -= 1

    def _write_text(self):
        font = pygame.font.SysFont(self._font, self._font_size)
        text = font.render(self.get_text(), True, pygame.Color('black'))
        self.parent_surface.blit(text,
                                 (self.x + self._delta_x,
                                  self.y + self._delta_y))

    def _draw_cursor(self):
        _time = time.time() % 1
        if self._active and _time >= 0.5:
            delta_y = self.height // 15
            x = self.x + self._delta_x + self._cursor_position * self._width_letter
            pygame.draw.line(self.parent_surface, pygame.Color('black'),
                             (x, self.y + delta_y),
                             (x, self.y + self.height - delta_y), 2)

    def _is_pressed(self, mouse):
        return (self._rect.topleft[0] < mouse[0] < self._rect.bottomright[0]
                and self._rect.topleft[1] < mouse[1] < self._rect.bottomright[1])

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._active = self._is_pressed(event.pos)
                if not self._active:
                    self._last_keydown = None
                    self._tick_last_keydown = 0
            elif self._active and event.type == pygame.KEYUP:
                if self._last_keydown is not None and event.key == self._last_keydown.key:
                    self._last_keydown = None
            elif self._active and event.type == pygame.KEYDOWN:
                self._tick_last_keydown = 0
                self._last_keydown = event

        if self._active and self._last_keydown is not None:
            self._tick_last_keydown += 1
            if 1 < self._tick_last_keydown < 500:
                return
            if self._last_keydown.key in TranslateDirection.dir_for_move_cursor:
                self._move_cursor(TranslateDirection.dir_for_move_cursor[self._last_keydown.key])

            elif self._last_keydown.key == pygame.K_RETURN:
                return True

            elif self._last_keydown.key == pygame.K_BACKSPACE:
                self._delete_letter(mode='backspace')

            elif self._last_keydown.key == pygame.K_DELETE:
                self._delete_letter(mode='delete')

            elif self._last_keydown.key == pygame.K_END:
                self._cursor_position = len(self._text)

            elif self._last_keydown.key == pygame.K_HOME:
                self._cursor_position = 0

            else:
                self._write_letter(self._last_keydown.unicode)

        pygame.time.wait(30)

    def draw(self):
        pygame.draw.rect(self.parent_surface, pygame.Color('white'), self._rect)
        self._write_text()
        self._draw_cursor()
