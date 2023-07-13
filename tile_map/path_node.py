from pygame import Vector2


class PathNode:

    def __init__(self, coords: Vector2):
        self.coords = coords
        self.g_cost = 0
        self.h_cost = 0
        self.previous = None
        self.neighbours = None

    def f_cost(self):
        return self.g_cost + self.h_cost

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
