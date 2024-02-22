import pygame
from settings import *
from support import import_folder
from sprite import Generic

class Drop(Generic):
    def __init__(self, surf, pos, moving, group, z):
        self.surf = surf

class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder()
        self.rain_floor = import_folder()
        self.floor_w, self.floor_h = pygame.image.load('../Sprite/water/').get_size()

    def create_floor(self):
        pass

    def create_drop(self):
        pass

    def update(self):
        self.create_floor()
        self.create_drop()