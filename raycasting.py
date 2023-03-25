import pygame as pg
import math
from settings import *


class Raycasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []

        for ray, values in enumerate(self.ray_casting_result):
            depth, projection_height, texture, offset = values

            if projection_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_column = pg.transform.scale(
                    wall_column, (SCALE, projection_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - projection_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projection_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE -
                    texture_height // 2, SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        texture_vertical, texture_horizontal = 1, 1

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_horizontal, dy = (
                y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_horizontal = (y_horizontal - oy) / sin_a
            x_horizontal = ox + depth_horizontal * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_horizontal = int(x_horizontal), int(y_horizontal)

                if tile_horizontal in self.game.map.world_map:
                    texture_horizontal = self.game.map.world_map[tile_horizontal]
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
                    texture_vertical = self.game.map.world_map[tile_vertical]
                    break

                x_vertical += dx
                y_vertical += dy
                depth_verticle += delta_depth

            if depth_verticle < depth_horizontal:
                depth, texture = depth_verticle, texture_vertical
                y_vertical %= 1
                offset = y_vertical if cos_a > 0 else (1 - y_vertical)
            else:
                depth, texture = depth_horizontal, texture_horizontal
                x_horizontal %= 1
                offset = (1 - x_horizontal) if sin_a > 0 else x_horizontal

            depth *= math.cos(self.game.player.angle - ray_angle)
            projection_height = SCREEN_DISTANCE / (depth + 0.0001)

            self.ray_casting_result.append(
                (depth,
                 projection_height,
                 texture,
                 offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
