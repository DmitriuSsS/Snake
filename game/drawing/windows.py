import pygame
from game.drawing.components import *

__all__ = ['Menu', 'WinWindow', 'GameOverWindow', 'EndFreeGameWindow']


class Menu:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 20, 160, 50, 'Game with Levels', href='level game'),
                        Button(self.surface, 20, 90, 160, 50, 'Free game', href='free game')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        for button in self.buttons:
            button.draw()


class WinWindow:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK',
                               href='menu')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_win = pygame.font.SysFont("Calibri", 40)
        text_win = font_win.render('You WIN!', True, pygame.Color('black'))
        self.surface.blit(text_win, ((self.surface.get_width() - text_win.get_width()) / 2, 30))
        for button in self.buttons:
            button.draw()


class GameOverWindow:
    def __init__(self):
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK', href='menu')]

    def draw(self):
        self.surface.fill(pygame.Color('white'))
        font_lose = pygame.font.SysFont("Calibri", 30)
        text_lose = font_lose.render('Game Over :(', True, pygame.Color('black'))
        self.surface.blit(text_lose, ((self.surface.get_width() - text_lose.get_width()) / 2, 30))
        for button in self.buttons:
            button.draw()


class EndFreeGameWindow:
    def __init__(self, score):
        self.score = score
        self.surface = pygame.display.set_mode((200, 160))
        self.buttons = [Button(self.surface, 20, 100, 160, 40, 'OK', href='menu')]

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
