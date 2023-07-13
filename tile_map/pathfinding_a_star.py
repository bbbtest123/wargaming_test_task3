from pygame import Vector2

from tile_map.heap import Heap
from tile_map.tile import Tile


# Calculating heuristic distance
def heuristic(current: Tile, goal: Tile):
    return Vector2(current.coords.x - goal.coords.x, 0).length() + Vector2(0, current.coords.y - goal.coords.y).length()


# Finding a path
def find_path(start: Tile, goal: Tile):
    open_set = Heap()
    closed_set = set()

    open_set.add(start)

    while open_set.last_index > 0:
        current = open_set.pop()

        closed_set.add(current)

        if current == goal:
            return current

        for neighbour in current.neighbours:
            if neighbour not in closed_set and (neighbour not in open_set or neighbour.g_cost > current.g_cost + 1):
                neighbour.g_cost = current.g_cost + 1
                neighbour.h_cost = heuristic(neighbour, goal)
                neighbour.previous = current

                if neighbour not in open_set:
                    open_set.add(neighbour)
                else:
                    open_set.update(neighbour)

    return None
