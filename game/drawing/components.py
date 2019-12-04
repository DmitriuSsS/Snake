import pygame

__all__ = ['Button', 'get_size_for_calibri']


def get_size_for_calibri(width: int, height: int, text: str) -> int:
    """
    Формула специально для шрифта Calibri в pygame
    :return: возвращает размер шрифта при котором он
    максимально занимает прямоугольник данной длины и высоты
    """
    size_width = 2 * width // len(text) - 1
    size_height = height - 1
    return int(max(min(size_height, size_width), 1))


class Button:
    def __init__(self,
                 parent_surface,
                 rect: pygame.Rect,
                 text='', text_color=pygame.Color('black'),
                 button_color=pygame.Color('white'), button_image=None,
                 handler=None,
                 name=None):
        self.parent_surface = parent_surface
        self.text = text
        self._text_color = text_color
        self._button_color = button_color
        self._image = button_image
        if (isinstance(self._image, pygame.Surface)
                and self._image.get_width() != rect.width
                and self._image.get_height() != rect.height):
            self._image = pygame.transform.scale(self._image, (rect.width, rect.height))
        self._handler = handler
        self.name = text if name is None else name
        self._rect = rect

    def draw(self):
        self._draw_button()
        if self.text:
            self._write_text()

    def handler(self):
        if self._handler is not None:
            self._handler()

    def _write_text(self):
        font_size = get_size_for_calibri(self._rect.width * 4 // 5, self._rect.height * 4 // 5, self.text)
        font = pygame.font.SysFont("Calibri", font_size)
        text = font.render(self.text, True, self._text_color)
        x, y = self._rect.x, self._rect.y
        button_width, button_height = self._rect.width, self._rect.height

        self.parent_surface.blit(text,
                                 (x + (button_width - text.get_width()) / 2,
                                  y + (button_height - text.get_height()) / 2))

    def _draw_button(self):
        width_circle = min(self._rect.height, self._rect.width) // 20
        color = self._button_color // pygame.Color(2, 2, 2, 255)
        color.a = self._button_color.a

        if not self._image:
            pygame.draw.rect(self.parent_surface, self._button_color, self._rect)
        else:
            rect_image = self._image.get_rect(topleft=self._rect.topleft)
            self.parent_surface.blit(self._image, rect_image)

        pygame.draw.rect(self.parent_surface, color, self._rect, width_circle)

    def is_pressed(self, mouse):
        return (self._rect.topleft[0] < mouse[0] < self._rect.bottomright[0]
                and self._rect.topleft[1] < mouse[1] < self._rect.bottomright[1])
