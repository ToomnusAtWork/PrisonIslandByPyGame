import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprite import Generic
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        # Inherited

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        map_data = load_pygame('./Maps/map.tmx')

        for x, y, surf in map_data.get_layer_by_name('Housefurniture').tiles():
            Generic((x * TILE_SIZE.y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        self.player = Player((640,360), self.all_sprites)

        # Instance of Generic
        Generic(pos = (0, 0), 
                surf = pygame.image.load('./Maps/Island.png').convert_alpha(), 
                groups = self.all_sprites,
                z = LAYERS['ground'])
        

    def run(self, dt):
        self.display_surface.fill('white')
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
    
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    
    
    def custom_draw(self, player):
        # Set player to be in middle
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2


        # 1.47.37 in vid
        # draw map opposite of moving
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

        

    
        
