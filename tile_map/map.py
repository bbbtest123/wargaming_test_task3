import random

from pygame import Vector2

from tile_map.tile import Tile


class Map:

    def __init__(self, width, height, ground_fraction):
        self.width = width
        self.height = height
        self.map = [[Tile(Vector2(x, y)) for y in range(self.height)] for x in range(self.width)]
        max_ground = int(self.width * self.height * ground_fraction)

        # Randomly placing ground tiles
        self.ground_tiles = set(random.sample([self.map[i][j] for i in range(self.width) for j in range(self.height)],
                                              max_ground))
        self.water_tiles = []

        for tile in self.ground_tiles:
            tile.is_ground = True

        # Setting water tiles list and calculating neighbouring tiles for each water tile
        for tile in [self.map[i][j] for i in range(self.width) for j in range(self.height)]:
            if not tile.is_ground:
                self.water_tiles.append(tile)
                self.add_walkable_neighbours(tile)

    # Removing data from a pathfinding attempt
    def clear_paths(self):
        for tile in self.water_tiles:
            tile.g_cost = 0
            tile.h_cost = 0
            tile.heap_index = 0
            tile.previous = None

    # Setting walkable neighbours for a tile
    def add_walkable_neighbours(self, tile: Tile):
        result = set()

        if tile.x() > 0 and not self.map[tile.x() - 1][tile.y()].is_ground:
            result.add(self.map[tile.x() - 1][tile.y()])
        if tile.y() > 0 and not self.map[tile.x()][tile.y() - 1].is_ground:
            result.add(self.map[tile.x()][tile.y() - 1])
        if tile.x() < self.width - 1 and not self.map[tile.x() + 1][tile.y()].is_ground:
            result.add(self.map[tile.x() + 1][tile.y()])
        if tile.y() < self.height - 1 and not self.map[tile.x()][tile.y() + 1].is_ground:
            result.add(self.map[tile.x()][tile.y() + 1])

        tile.neighbours = result
