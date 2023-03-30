from sprite_object import *
from random import randint, random, choice


class Enemy(AnimatedSprite):
    def __init__(self, game, path='assets/sprites/enemy/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_distance = randint(3, 6)
        self.attack_damage = 10
        self.speed = 0.03
        self.accuracy = 0.15
        self.size = 10
        self.health = 100
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx

        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(
            self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        if next_pos not in self.game.object_handler.enemy_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.enemy_attack.play()

            if random() <= self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)

        if self.animation_trigger:
            self.pain = False

    def check_hit_in_enemy(self):
        if self.game.player.shot and self.ray_cast_value:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.enemy_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.enemy_death.play()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_enemy()
            self.check_hit_in_enemy()

            if self.pain:
                self.animate_pain()
            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.distance < self.attack_distance:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_enemy(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_distance_vertical, wall_distance_horizontal = 0, 0
        player_distance_vertical, player_distance_horizontal = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.theta
        texture_vertical, texture_horizontal = 1, 1

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

            if tile_horizontal == self.map_pos:
                player_distance_horizontal = depth_horizontal
                break

            if tile_horizontal in self.game.map.world_map:
                wall_distance_horizontal = depth_horizontal
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

            if tile_vertical == self.map_pos:
                player_distance_vertical = depth_verticle
                break

            if tile_vertical in self.game.map.world_map:
                wall_distance_vertical = depth_verticle
                break

            x_vertical += dx
            y_vertical += dy
            depth_verticle += delta_depth

        player_distance = max(player_distance_vertical,
                              player_distance_horizontal)
        wall_distance = max(wall_distance_vertical,
                            wall_distance_horizontal)

        if 0 < player_distance < wall_distance or not wall_distance:
            return True

        return False


class CacoDemonEnemy(Enemy):
    def __init__(self, game, path='assets/sprites/enemy/caco_demon/0.png', pos=(10.5, 6.5), scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_distance = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35


class CyberDemonEnemy(Enemy):
    def __init__(self, game, path='assets/sprites/enemy/cyber_demon/0.png', pos=(11.5, 6.0), scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_distance = 6.0
        self.health = 200
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25
