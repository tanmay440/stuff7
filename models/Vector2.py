class Vector2:
    """
    Represents a 2D vector.
    """
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)

        if isinstance(other, Vector2):
            return Vector2(self.y - other.y, self.x - other.x)

        return NotImplemented

    def __truediv__(self, scalar:float):
        return Vector2(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)

    def get_rotation_angle(self):
        import math
        return math.degrees(math.atan2(self.y, self.x))