import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'assets/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.enemy_pain = pg.mixer.Sound(self.path + 'enemy_pain.wav')
        self.enemy_death = pg.mixer.Sound(self.path + 'enemy_death.wav')
        self.enemy_attack = pg.mixer.Sound(self.path + 'enemy_attack.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')

        self.shotgun.set_volume(0.3)
        self.enemy_pain.set_volume(0.2)
        self.enemy_death.set_volume(0.2)
        self.enemy_attack.set_volume(0.2)
        self.player_pain.set_volume(0.2)
        pg.mixer.music.set_volume(0.1)
