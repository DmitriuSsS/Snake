import pygame

__all__ = ['RedirectToMenu', 'RedirectToFreeGame', 'RedirectToLevelGame',
           'RedirectToGameOverWindow', 'RedirectToWinWindow',
           'RedirectToEndFreeGameWindow', 'RedirectToSetGameMakerProperty',
           'RedirectToGameMaker', 'PickEraser', 'PickSnake', 'PickWall',
           'Save']


class RedirectToMenu:
    name = 'Redirect to Menu'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class RedirectToFreeGame:
    name = 'Redirect to FreeGame'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class RedirectToLevelGame:
    name = 'Redirect to LevelGame'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class RedirectToWinWindow:
    name = 'Redirect to WinWindow'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class RedirectToGameOverWindow:
    name = 'Redirect to GameOverWindow'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class RedirectToEndFreeGameWindow:
    name = 'Redirect to EndFreeGameWindow'

    def __init__(self, score):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name, score=score)


class RedirectToSetGameMakerProperty:
    name = 'Redirect to SetGameMakerProperty'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class RedirectToGameMaker:
    name = 'Redirect to GameMaker'

    def __init__(self, width, height, score):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name,
                                        width=width, height=height, score=score)


class PickWall:
    name = 'Pick Wall'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class PickEraser:
    name = 'Pick Eraser'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)


class PickSnake:
    name = 'Pick Snake'

    def __init__(self, direction):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name,
                                        direction=direction)


class Save:
    name = 'Save'

    def __init__(self):
        self.event = pygame.event.Event(pygame.USEREVENT, name=self.name)
