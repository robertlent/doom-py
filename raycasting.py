import pygame as pg
import math
from settings import *


class Raycasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_horizontal, dy = (
                y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_horizontal = (y_map - oy) / sin_a
            x_horizontal = ox + depth_horizontal * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_horizontal = int(x_horizontal), int(y_horizontal)

                if tile_horizontal in self.game.map.world_map:
                    break

                x_horizontal += dx
                y_horizontal += dy
                depth_horizontal += delta_depth

            x_vertical, dx = (
                x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_verticle = (x_vertical - ox) / cos_a
            y_vertical = oy + depth_verticle * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vertical = int(x_vertical), int(y_vertical)

                if tile_vertical in self.game.map.world_map:
                    break

                x_vertical += dx
                y_vertical += dy
                depth_verticle += delta_depth

            if depth_verticle < depth_horizontal:
                depth = depth_verticle
            else:
                depth = depth_horizontal

            pg.draw.line(self.game.screen, "yellow", (100 * ox, 100 * oy),
                         (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
