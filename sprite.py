import pygame
from settings import *
from settings import LAYERS
from random import randint, choice
from timer import Timer
class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        # change hitbox


class Interaction(Generic):
    def __init__(self, pos, surf, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

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
    

class Decorative(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.height * 0.9)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        
        # white surface particle
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((255, 255, 255))
        self.image = new_surf
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        # Tree attributes
        self.health = 5
        self.alive = True
        # need tree stump
        self.stump_surf = pygame.image.load(f'../graphic/treestump').convert_alpha()

        self.invul_timer = Timer(200)

        # Wood and apple drop
        self.apple_surf = pygame.image.load('../Sprite/item/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()

        self.player_add = player_add

    # def damage(self):
    #     # tree damaging
    #     self.health -= 1
    #     Particle(
    #         pos= x,
    #         surf= y,
    #         groups= self.groups()[0],
    #         z= LAYERS['fruits']
    #     )
    #     self.player_add('wood')

    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['fruits'], 300)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False


    def create_fruit(self):
        # create apple randomly on tree
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                Generic()

        # add wood drop and apple to tree

    def update(self, dt):
        if self.alive:
            self.check_death()
