import random
from copy import deepcopy, copy
from typing import List

from game.direction import *
from game.service_entities.queue import Queue
from game.service_entities.vector import Vector
from game.settings import Settings

__all__ = ['Food', 'SnakePart', 'Snake', 'Field', 'Level']

settings = Settings()


class Food:
    def __init__(self, speed_change=1.0, length_change=1, score=1):
        self.speed_change = speed_change
        self.length_change = length_change
        self.score = score

    def __hash__(self):
        return self.score * 357 ^ int(self.length_change * 7 + self.speed_change)

    def __eq__(self, other):
        if not isinstance(other, Food):
            return False
        return (self.score == other.score
                and self.speed_change == other.speed_change
                and self.length_change == other.length_change)


class SnakePart:
    def __init__(self, location: Vector, direction: Direction):
        self.direction = direction
        self.location = location


class Snake:
    def __init__(self, body: list, speed: float = 14.0):
        """
        :param body: list[SnakePart], перечисленный в порядке head -> tail
        """

        self.speed = speed
        self.length_change = 0

        self.body = Queue()
        for snake_part in body[::-1]:
            self.body.enqueue(snake_part)

    def _get_direction_for_step(self, proposed_direction: Direction = None) -> Direction:
        if proposed_direction is None:
            return self.head.direction
        if proposed_direction == TranslateDirection.opposite_dir[self.head.direction]:
            return self.head.direction
        return proposed_direction

    def step(self, direction: Direction = None, size_field: tuple = None):
        direction = self._get_direction_for_step(direction)
        new_head_location = self.head.location + TranslateDirection.dir_offset[direction]
        if size_field is not None:
            new_head_location.x %= size_field[0]
            new_head_location.y %= size_field[1]
        self.body.enqueue(SnakePart(new_head_location, direction))
        if self.length_change > 0:
            self.length_change -= 1
            return
        if self.length_change < 0:
            self.length_change += 1
            self.body.dequeue()
        self.body.dequeue()

    def check_intersection(self, points: set = None) -> bool:
        if points is None:
            points = set()
        count = len(points)
        _points = copy(points)
        for part in self:
            count += 1
            _points.add(part.location)

        return count != len(_points)

    def eat_food(self, food: Food):
        self.speed *= food.speed_change
        self.length_change += food.length_change

    @property
    def head(self) -> SnakePart:
        return self.body.tail

    @property
    def tail(self) -> SnakePart:
        return self.body.head

    def __iter__(self):
        """Итератор для змейки пробегающий от головы до хвоста"""
        snake = []
        for part in self.body:
            snake.append(part)
        return iter(snake[::-1])

    def __len__(self):
        return len(self.body)

    def __contains__(self, item):
        if type(item) is Vector:
            for part in self:
                if part.location == item:
                    return True
        if type(type) is SnakePart:
            for part in self:
                if item == part:
                    return True
        return False


class Field:
    def __init__(self, snake: Snake, walls: set, size_field: tuple):
        self.foods_location = {}
        self.snake = snake
        self.walls = walls
        self.width, self.height = size_field

        self.not_walls_cells = set()
        for x in range(self.width):
            for y in range(self.height):
                point = Vector(x, y)
                if point not in walls:
                    self.not_walls_cells.add(point)

    def is_crash(self):
        return self.snake.check_intersection(self.walls)

    def generate_food(self, food: Food = Food()):
        loc = set([e.location for e in self.snake.body]).union(self.foods_location.keys())
        empty_cells = self.not_walls_cells - loc
        location = random.choice(list(empty_cells))
        self.foods_location[location] = food

        return location

    def eat_food(self, location: Vector = None) -> float:
        """
        :return: score
        """
        if location is None:
            location = self.snake.head.location
        self.snake.eat_food(self.foods_location[location])
        food = self.foods_location.pop(location)
        return food.score


class Level:
    @staticmethod
    def anti_parse_map(field: Field, max_score: int) -> List[str]:
        """
        :return: строки карты
        """
        result = []

        for i in range(field.height):
            line = []
            for j in range(field.width):
                line.append('#' if Vector(j, i) in field.walls else ' ')
            result.append(''.join(line))

        result.append(TranslateDirection.dir_word[field.snake.head.direction])
        for part in field.snake:
            result.append(f'{part.location.x} {part.location.y}')

        result.append(str(max_score))
        return result

    @staticmethod
    def parse_map(map_path: str) -> (Field, int):
        walls = set()
        with open(map_path, 'r', encoding='utf-8') as mfd:
            lines = mfd.read().split('\n')
            width_field = 0
            height_field = len(lines) - 5
            for i in range(height_field):
                for j in range(len(lines[i])):
                    if len(lines[i]) > width_field:
                        width_field = len(lines[i])
                    if lines[i][j] == settings.wall_symbol:
                        walls.add(Vector(j, i))

            snake_dir = TranslateDirection.word_dir[lines[-5]]
            snake = []
            for i in range(-4, -1):
                location = tuple(map(int, lines[i].split(' ')))
                snake_part = SnakePart(Vector(*location), snake_dir)
                snake.append(snake_part)
            max_score = int(lines[-1])

        field = Field(Snake(snake), walls, (width_field, height_field))
        return field, max_score

    def __init__(self, level_name: str = None, health: int = 3,
                 field: Field = None, max_score: int = 5):
        if level_name is None and field is None:
            raise Exception('Имя уровня и поле оба были None')
        self.win_flag = False
        self.game_over_flag = False
        self.health = health
        self.name = ''
        if level_name:
            (self.field, self.max_score) = self.parse_map(settings.map_file(level_name))
            self.name = level_name
        else:
            self.field, self.max_score = field, max_score
        self.old_snake = deepcopy(self.field.snake)
        self.score = 0

    def reset(self):
        self.score = 0
        self.field.snake = deepcopy(self.old_snake)

    def lose(self):
        self.health -= 1
        if not self.health:
            self.game_over_flag = True
        else:
            self.reset()

    def eat_food(self):
        self.score += self.field.eat_food()

    def step_snake(self, direction: Direction = None):
        self.field.snake.step(direction, (self.field.width, self.field.height))
        if self.field.is_crash() or len(self.field.snake) <= 1:
            self.lose()
        if self.field.snake.head.location in self.field.foods_location:
            if self.field.foods_location[self.field.snake.head.location] == Food():
                self.field.generate_food()
            self.eat_food()
        if self.score >= self.max_score:
            self.win_flag = True
