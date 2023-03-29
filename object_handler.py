from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.static_sprite_path = 'assets/sprites/static_sprites/'
        self.animated_sprite_path = 'assets/sprites/animated_sprites/'
        self.npc_sprite_path = 'assets/sprites/npc/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}
        self.enemy_count = 5
        self.enemy_types = [NPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_enemies()

        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(
            game, path=self.animated_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(
            game, path=self.animated_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(
            game, path=self.animated_sprite_path + 'red_light/0.png', pos=(19.5, 7.5)))

    def spawn_enemies(self):
        for i in range(self.enemy_count):
            enemies = choices(self.enemy_types, self.weights)[0]
            pos = x, y = randrange(
                self.game.map.columns), randrange(self.game.map.rows)

            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(
                    self.game.map.columns), randrange(self.game.map.rows)

            self.add_npc(enemies(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.game_win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        self.npc_positions = {
            npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
