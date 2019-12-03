class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(other.x + self.x, other.y + self.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Vector(self.x * other, self.y * other)

    def __hash__(self):
        return hash(self.x) * 357 + hash(self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
