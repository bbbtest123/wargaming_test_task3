import argparse

import pygame
import random
import sys

from pygame.locals import *

from tile_map import pathfinding_a_star
from tile_map.map import Map
from tile_map.tile import Tile

parser = argparse.ArgumentParser(
    prog='Pathfinder',
    description='An A* pathfinding algorithm implementation')

parser.add_argument('-x')
parser.add_argument('-y')

args = parser.parse_args()

random.seed()

# Parsing args for X and Y
X = int(args.x) if args.x is not None and args.x.isnumeric() and 60 >= int(args.x) >= 2 else 20
Y = int(args.y) if args.y is not None and args.y.isnumeric() and 60 >= int(args.y) >= 2 else 20

# The size of image tiles
TILE_SIZE = 16

# Setting up screen
screen = pygame.display.set_mode((X * TILE_SIZE, Y * TILE_SIZE))
pygame.display.set_caption("Pathfinder")

# Setting up cloak
clock = pygame.time.Clock()

# The flag for ship animation (up or down)
ship_up_animation = True

# Initializing tile map
tile_map = Map(X, Y, 0.3)

# Initializing lists of tile images
dirt_internal_tiles_list = [pygame.image.load("tiles_pngs\\dirt_internal1.png"),
                            pygame.image.load("tiles_pngs\\dirt_internal2.png"),
                            pygame.image.load("tiles_pngs\\dirt_internal3.png"),
                            pygame.image.load("tiles_pngs\\dirt_internal4.png"),
                            pygame.image.load("tiles_pngs\\dirt_internal5.png"),
                            pygame.image.load("tiles_pngs\\dirt_internal6.png"),
                            pygame.image.load("tiles_pngs\\dirt_internal7.png")]

bush_tiles_list = [pygame.image.load("tiles_pngs\\bush1.png"),
                   pygame.image.load("tiles_pngs\\bush2.png"),
                   pygame.image.load("tiles_pngs\\bush3.png"),
                   pygame.image.load("tiles_pngs\\bush4.png"),
                   pygame.image.load("tiles_pngs\\bush5.png"),
                   pygame.image.load("tiles_pngs\\bush6.png"),
                   pygame.image.load("tiles_pngs\\bush7.png"),
                   pygame.image.load("tiles_pngs\\bush8.png"),
                   pygame.image.load("tiles_pngs\\log1.png"),
                   pygame.image.load("tiles_pngs\\log2.png"),
                   pygame.image.load("tiles_pngs\\log3.png")]

stuff_tiles_list = [pygame.image.load("tiles_pngs\\pool1.png"),
                    pygame.image.load("tiles_pngs\\rock1.png"),
                    pygame.image.load("tiles_pngs\\rock2.png"),
                    pygame.image.load("tiles_pngs\\rock3.png"),
                    pygame.image.load("tiles_pngs\\rock4.png")]

water_internal_tiles_list = [pygame.image.load("tiles_pngs\\water_internal1.png"),
                             pygame.image.load("tiles_pngs\\water_internal2.png"),
                             pygame.image.load("tiles_pngs\\water_internal3.png"),
                             pygame.image.load("tiles_pngs\\water_internal4.png")]

ship_tile_image = pygame.image.load("tiles_pngs\\ship.png")
goal_tile_image = pygame.image.load("tiles_pngs\\goal.png")
way_tile_image = pygame.image.load("tiles_pngs\\way.png")

# Initial tiles for the ship and the goal
ship_tile, goal_tile = random.sample(tile_map.water_tiles, 2)

# Tick count for animations
clock_tick_count = 0

# Animations per 1000 clock ticks
animation_rate = 1


# Setting images for tiles
def set_images():
    for i in range(X):
        for j in range(Y):
            if not tile_map.map[i][j].is_ground:
                rotation = random.randrange(2) * 180
                flip_vertical = random.randrange(2)
                flip_horizontal = 0
                tile = random.choice(water_internal_tiles_list)
                tile_content = None

            else:
                rotation = random.randrange(4) * 90
                flip_vertical = random.randrange(2)
                flip_horizontal = random.randrange(2)
                tile = random.choice(dirt_internal_tiles_list)
                tile_content = None

                if random.randrange(4) == 0:
                    content_type = random.randrange(2)

                    if content_type == 0:
                        rotation = 0
                        flip_vertical = random.randrange(2)
                        flip_horizontal = 0
                        tile_content = random.choice(bush_tiles_list)
                    else:
                        rotation = random.randrange(4) * 90
                        flip_vertical = random.randrange(2)
                        flip_horizontal = random.randrange(2)
                        tile_content = random.choice(stuff_tiles_list)
                    tile_content = pygame.transform.rotate(tile_content, rotation)
                    tile_content = pygame.transform.flip(tile_content, bool(flip_vertical), bool(flip_horizontal))

            tile = pygame.transform.rotate(tile, rotation)
            tile = pygame.transform.flip(tile, bool(flip_vertical), bool(flip_horizontal))
            tile_map.map[i][j].image1 = tile
            tile_map.map[i][j].image2 = tile_content


# Updating water images for animation
def update_animation():
    for tile in tile_map.water_tiles:
        rotation = random.randrange(2) * 180
        flip_vertical = random.randrange(2)
        flip_horizontal = 0
        image = random.choice(water_internal_tiles_list)
        image = pygame.transform.rotate(image, rotation)
        image = pygame.transform.flip(image, bool(flip_vertical), bool(flip_horizontal))
        tile.image1 = image


# Drawing the map
def draw_map():
    for i in range(X):
        for j in range(Y):
            screen.blit(tile_map.map[i][j].image1, (i * TILE_SIZE, j * TILE_SIZE))
            if not tile_map.map[i][j].image2 is None:
                screen.blit(tile_map.map[i][j].image2, (i * TILE_SIZE, j * TILE_SIZE))
    screen.blit(ship_tile_image, (ship_tile.x() * TILE_SIZE, ship_tile.y() * TILE_SIZE - int(ship_up_animation)))
    screen.blit(goal_tile_image, (goal_tile.x() * TILE_SIZE, goal_tile.y() * TILE_SIZE))
    draw_path(path)


# Drawing a path from the ship to the goal
def draw_path(path: Tile):
    if path is None:
        return
    if path.previous is None:
        return

    screen.blit(way_tile_image, (path.x() * TILE_SIZE, path.y() * TILE_SIZE))
    draw_path(path.previous)


# Checking if the mouse cursor on specific tile
def is_mouse_on_tile(pos, tile):
    return (tile.x() + 1) * TILE_SIZE >= pos[0] >= tile.x() * TILE_SIZE \
        and (tile.y() + 1) * TILE_SIZE >= pos[1] >= tile.y() * TILE_SIZE


# Getting a tile under the mouse cursor
def get_tile(pos):
    x = int(pos[0] / TILE_SIZE)
    y = int(pos[1] / TILE_SIZE)
    if int(pos[0] / TILE_SIZE) < 0:
        x = 0
    elif int(pos[0] / TILE_SIZE) > X - 1:
        x = X - 1

    if int(pos[1] / TILE_SIZE) < 0:
        y = 0
    elif int(pos[1] / TILE_SIZE) > Y - 1:
        y = Y - 1

    return tile_map.map[x][y]


gameOn = True

path = None
set_images()
draw_map()

dragging_ship = False
dragging_goal = False

while gameOn:
    # Updating tiles for animation
    clock_tick_count += 1
    if clock_tick_count >= 1000 / animation_rate:
        update_animation()
        ship_up_animation = not ship_up_animation
        clock_tick_count = 0

    # Calculating a path
    if path is None:
        path = pathfinding_a_star.find_path(ship_tile, goal_tile)

    # Drawing the map
    draw_map()
    for event in pygame.event.get():
        # Dragging the ship or the goal on mouse button down
        if event.type == MOUSEBUTTONDOWN:
            if is_mouse_on_tile(pygame.mouse.get_pos(), ship_tile) and \
                    dragging_ship is False and dragging_goal is False:
                dragging_ship = True

            elif is_mouse_on_tile(pygame.mouse.get_pos(), goal_tile) and \
                    dragging_ship is False and dragging_goal is False:
                dragging_goal = True
        # Finishing dragging the ship or the goal on mouse button up
        elif event.type == MOUSEBUTTONUP:
            dragging_ship = False
            dragging_goal = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gameOn = False

        elif event.type == QUIT:
            gameOn = False

    # Updating positions for the ship and the goal
    if dragging_ship and not get_tile(pygame.mouse.get_pos()) is ship_tile \
            and not get_tile(pygame.mouse.get_pos()).is_ground:
        tile_map.clear_paths()
        path = None
        ship_tile = get_tile(pygame.mouse.get_pos())

    if dragging_goal and not get_tile(pygame.mouse.get_pos()) is goal_tile \
            and not get_tile(pygame.mouse.get_pos()).is_ground:
        tile_map.clear_paths()
        path = None
        goal_tile = get_tile(pygame.mouse.get_pos())

    pygame.display.flip()
