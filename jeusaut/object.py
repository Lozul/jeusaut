class Object:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_colliding(self, other):
        if not isinstance(other, Object):
            return False

        return not (self.x + self.width <= other.x or other.x + other.width <= self.x or self.y + self.height <= other.y or other.y + other.height <= self.y)

    def update(self):
        pass

    def draw(self):
        pass