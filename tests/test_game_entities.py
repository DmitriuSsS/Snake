import os
import unittest.mock
from copy import deepcopy

from parameterized import parameterized

from game.direction import Direction
from game.entities import *
from game.service_entities.vector import Vector


class TestFood(unittest.TestCase):
    def test_hash(self):
        food1 = Food(1, 1, 1)
        food2 = Food(2, 2, 2)

        self.assertEqual(hash(food1), hash(food1))
        self.assertNotEqual(hash(food1), hash(food2))

    def test_eq(self):
        food1 = Food(1, 1, 1)
        food2 = Food(1, 1, 1)
        food3 = Food(2, 2, 2)

        self.assertEqual(food1, food2)
        self.assertNotEqual(food1, food3)
        self.assertNotEqual(food1, 10)


class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake_parts = [SnakePart(Vector(3, 0), Direction.RIGHT),
                            SnakePart(Vector(2, 0), Direction.RIGHT)]
        self.snake = Snake(self.snake_parts)

    @staticmethod
    def equals_snake(snake: Snake, snake_parts: list):
        i = 0
        for part in snake:
            if (snake_parts[i].location != part.location
                    or snake_parts[i].direction != part.direction):
                return False
            i += 1
        return True

    def test_iter(self):
        self.assertTrue(self.equals_snake(self.snake, self.snake_parts))

    def test_len(self):
        self.assertEqual(len(self.snake_parts), len(self.snake))

    def test_get_head_and_tail(self):
        self.assertEqual(self.snake_parts[0], self.snake.head)
        self.assertEqual(self.snake_parts[-1], self.snake.tail)

    def test_eat_food(self):
        food = Food(2, 2, 2)
        old_speed = self.snake.speed
        old_length_change = self.snake.length_change
        self.snake.eat_food(food)

        self.assertEqual(old_speed * 2, self.snake.speed)
        self.assertEqual(old_length_change + 2, self.snake.length_change)

    def test_check_intersection(self):
        self.assertFalse(self.snake.check_intersection())

        self.assertTrue(self.snake.check_intersection(
            {self.snake_parts[0].location}))

        snake_parts = [SnakePart(Vector(0, 0), Direction.RIGHT),
                       SnakePart(Vector(0, 0), Direction.RIGHT)]
        snake = Snake(snake_parts)
        self.assertTrue(snake.check_intersection())

        self.assertTrue(snake.check_intersection({Vector(1, 1)}))

    @parameterized.expand([[Direction.RIGHT, Direction.RIGHT],
                           [Direction.LEFT, Direction.RIGHT],
                           [Direction.DOWN, Direction.DOWN],
                           [None, Direction.RIGHT]
                           ])
    def test_get_direction_for_step(self, proposed, expected):
        self.assertEqual(expected, self.snake._get_direction_for_step(proposed))

    @parameterized.expand([[None],
                           [Direction.RIGHT],
                           [Direction.LEFT]])
    def test_stepToHeadDirection_whenDirectionShouldNotChange(self, direction):
        self.snake.step(direction)
        expected_snake_parts = [SnakePart(Vector(4, 0), Direction.RIGHT),
                                SnakePart(Vector(3, 0), Direction.RIGHT)]
        self.assertTrue(self.equals_snake(self.snake, expected_snake_parts))

    def test_step_whenDirectionChange(self):
        self.snake.step(direction=Direction.UP)

        expected_snake_parts = [SnakePart(Vector(3, -1), Direction.UP),
                                SnakePart(Vector(3, 0), Direction.RIGHT)]

        self.assertTrue(self.equals_snake(self.snake, expected_snake_parts))

    def test_step_whenGoingOutOfTheField(self):
        self.snake.step(size_field=(4, 4))

        expect_snake_parts = [SnakePart(Vector(0, 0), Direction.RIGHT),
                              SnakePart(Vector(3, 0), Direction.RIGHT)]

        self.assertTrue(self.equals_snake(self.snake, expect_snake_parts))

    def test_step_whenSnakeShouldIncrease(self):
        self.snake.length_change = 1
        expect_snake_parts = ([SnakePart(Vector(4, 0), Direction.RIGHT)] +
                              self.snake_parts)

        self.snake.step()
        self.equals_snake(self.snake, expect_snake_parts)

    def test_step_whenSnakeShouldDecrease(self):
        self.snake.length_change = -1
        expect_snake_parts = [SnakePart(Vector(4, 0), Direction.RIGHT)]
        self.snake.step()
        self.equals_snake(self.snake, expect_snake_parts)


class TestField(unittest.TestCase):
    def setUp(self):
        snake_parts = [SnakePart(Vector(3, 0), Direction.RIGHT),
                       SnakePart(Vector(2, 0), Direction.RIGHT)]
        snake = Snake(snake_parts)
        walls = {Vector(3, 1), Vector(2, 1), Vector(1, 1)}
        size = (4, 4)

        self.field = Field(snake, walls, size)

    def test_is_crash(self):
        self.assertFalse(self.field.is_crash())

        self.field.snake = Snake([SnakePart(list(self.field.walls)[0], Direction.RIGHT)])
        self.assertTrue(self.field.is_crash())

    @unittest.mock.patch('game.entities.Snake.eat_food')
    def test_eat_food(self, mock):
        location = Vector(3, 0)
        food = Food()
        self.field.foods_location[location] = food
        self.assertEqual(food.score, self.field.eat_food(location))

        self.field.foods_location[location] = food
        self.assertEqual(food.score, self.field.eat_food())

        self.assertEqual(2, mock.call_count)

    def test_generate_food(self):
        food = Food(1, 2, 3)
        self.field.generate_food(food)

        location, actual_food = [item for item in self.field.foods_location.items()][0]

        self.assertEqual(food, actual_food)
        self.assertTrue(0 <= location.x < self.field.width)
        self.assertTrue(0 <= location.y <= self.field.height)
        self.assertFalse(location in self.field.walls)
        self.assertFalse(location in [part for part in self.field.snake])


class TestLevel(unittest.TestCase):
    def setUp(self):
        walls = {Vector(i, 2) for i in range(3)}
        snake = Snake([SnakePart(Vector(2, 1), Direction.RIGHT),
                       SnakePart(Vector(1, 1), Direction.RIGHT),
                       SnakePart(Vector(0, 1), Direction.RIGHT)])
        self.field = Field(snake, walls, (3, 3))
        with unittest.mock.patch.object(Level, 'parse_map') as mock_get_value:
            mock_get_value.return_value = deepcopy(self.field), 5
            self.level = Level('level', 3)

    @staticmethod
    def equal_field(field1: Field, field2: Field):
        snake1 = [part for part in field1.snake]
        snake2 = [part for part in field2.snake]
        if len(snake1) != len(snake2):
            return False
        for i in range(len(snake1)):
            if (snake1[i].direction != snake2[i].direction
                    or snake1[i].location != snake2[i].location):
                return False
        if field1.walls != field2.walls:
            return False
        return (field1.width, field1.height) == (field2.width, field2.height)

    def test_parse_map(self):
        score = 5

        actual_field, actual_max_score = Level.parse_map(
            os.path.join('tests', 'data', 'maps_for_test', 'map3x3.txt'))

        self.assertTrue(self.equal_field(self.field, actual_field))
        self.assertEqual(score, actual_max_score)

    def test_reset(self):
        self.level.step_snake()
        self.level.reset()

        self.assertFalse(self.field == self.level.field)
        self.equal_field(self.field, self.level.field)

    @unittest.mock.patch('game.entities.Level.reset')
    def test_call_reset(self, mock):
        self.level.lose()
        self.assertTrue(mock.called)
        self.assertFalse(self.level.game_over_flag)

    def test_game_over(self):
        self.level.health = 1
        self.level.lose()

        self.assertTrue(self.level.game_over_flag)

    def test_eat_food(self):
        old_score = self.level.score
        food = Food(score=10)
        self.level.field.foods_location[self.field.snake.head.location] = food
        self.level.eat_food()

        self.assertEqual(old_score + 10, self.level.score)

    def test_step_snake_when_win(self):
        self.level.score = self.level.max_score
        self.level.step_snake()

        self.assertTrue(self.level.win_flag)

    @unittest.mock.patch('game.entities.Level.lose')
    def test_step_snake_when_snake_break(self, mock):
        self.level.field.walls.add(Vector(0, 1))
        self.level.step_snake()

        self.assertTrue(mock.called)

    @unittest.mock.patch('game.entities.Field.generate_food')
    def test_step_when_snake_eat_basic_food(self, mock):
        self.level.field.foods_location[Vector(0, 1)] = Food()
        self.level.step_snake()

        self.assertTrue(mock.called)

    @unittest.mock.patch('game.entities.Field.generate_food')
    def test_step_when_snake_eat_not_basic_food(self, mock):
        self.level.field.foods_location[Vector(0, 1)] = Food(2, 2, 2)
        self.level.step_snake()

        self.assertFalse(mock.called)
