import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprite import Generic, Water, Tree, Interaction
from pytmx.util_pygame import load_pygame
from transition import Transition

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()

        # collision inherited pygame group sprite
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

    def setup(self):
        # map_data is basically tmx data 
        # map_data = load_pygame('./Data/map.tmx')

        # Water animation
        # water_frames = import_folder('./Sprite/water')
        # for x, y, surf in map_data.get_layer_by_name('Water').tiles():
        #     Water((x * TILE_SIZE, y * TILE_SIZE), waater_frames, self.all_sprites)

        # Fence placement 
        # for x, y, surf in map_data.get_layer_byname('Fence').tiles():
        #     Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Decoration placement
        # for obj in map_data.get_layer_by_name('Decoration').tiles():
            # Decorativeree(
            #     pos= (obj.x, obj.y), 
            #     surf= obj.image, 
            #     groups= [self.all_sprites, self.collision_sprites]
            #     )
        
        # Trees placement 
        # for obj in tmx_data.get_layer_by_name('Trees'):
        #     Tree(
        #         pos= (obj.x, obj.y), 
        #         surf= obj.image, 
        #         groups= [self.all_sprites, self.collision_sprites, self.tree_sprites],
        #         name= obj.name,
        #         player_add= self.player_add)

        # Rocks placement
        # for obj in tmx_data.get_layer_by_name('Rocks'):
        #     Rock(
        #         pos= (obj.x, obj.y),
        #         surf= obj.image,
        #     )

        # Collision in obj from tmx data in game 
        # for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
        #     Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # Player starting point
        # for obj in tmx_data.get_layer_by_name('Player'):
        #     if obj.name == 'Start':
        #         self.player = Player(
        #             pos= (obj.x, obj.y),
        #             group= self.all_sprites, 
        #             collision_sprites= self.collision_sprites,
        #             tree_sprites= self.tree_sprites,
        #             interaction = self.interaction_sprites)
                
        #     if obj.name == 'Boat':
        #         Interaction((obj.x, obj.y), 
        #                     (obj.width, obj.height), 
        #                     self.interaction_sprites, 
        #                     obj.name)

        self.player = Player((640,360), self.all_sprites, self.collision_sprites, self.tree_sprites)
        # we pass collision in player as parameter
        # but we pass collision in object as a container inside!

        # Instance of Generic
        Generic(pos = (0, 0), 
                surf = pygame.image.load('./Maps/NewIsland.png').convert_alpha(), 
                groups = self.all_sprites,
                z = LAYERS['ground'])
        
    def player_add(self, item):
        self.player.item_inventory[item] += 1 

    def reset(self):
        #  reset the world and create new apple and tree
        self.new = APPLE_POS

    def run(self, dt):
        self.display_surface.fill('#71ddee')
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

        # draw map opposite of moving
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
