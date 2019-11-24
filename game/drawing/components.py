import pygame

__all__ = ['Button']


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
