import pygame
from settings import *
from settings import LAYERS
from random import randint

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        # change hitbox

# Inheritance from generic
class Water(Generic):
    def __init__(self, pos, frames, groups):
        
        # Animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(pos = pos, 
                         surf = self.frames[self.frame_index], 
                         groups = groups, 
                         z = LAYERS['water'])
        
    def animate(self, dt):
        self.frame_index  += 3 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
    

class Seashell(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.height * 0.9)


class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)

        # Wood and apple drop
        self.apple_surf = pygame.image.load('../Sprite/item/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                Generic()

