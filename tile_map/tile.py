from pygame import Vector2


class Tile:

    def __init__(self, coords: Vector2, is_ground=False):
        self.image1 = None
        self.image2 = None
        self.coords = coords
        self.is_ground = is_ground
        self.g_cost = 0
        self.h_cost = 0
        self.previous = None
        self.neighbours = None
        self.heap_index = 0

    def x(self):
        return int(self.coords.x)

    def y(self):
        return int(self.coords.y)

    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        if self.f_cost() < other.f_cost():
            return True
        elif self.f_cost() == other.f_cost() and self.h_cost < other.h_cost:
            return True

        return False
