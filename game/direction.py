from enum import Enum

import pygame

from game.service_entities.vector import Vector


__all__ = ['Direction', 'TranslateDirection']


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class TranslateDirection:
    dir_offset = {
        Direction.UP: Vector(0, -1),
        Direction.DOWN: Vector(0, 1),
        Direction.RIGHT: Vector(1, 0),
        Direction.LEFT: Vector(-1, 0)
    }

    opposite_dir = {
        Direction.RIGHT: Direction.LEFT,
        Direction.LEFT: Direction.RIGHT,
        Direction.DOWN: Direction.UP,
        Direction.UP: Direction.DOWN
    }

    word_dir = {
        'right': Direction.RIGHT,
        'left': Direction.LEFT,
        'up': Direction.UP,
        'down': Direction.DOWN
    }

    direction = {
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN
    }
