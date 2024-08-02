import pygame
import spritesheet as ss
from settings import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites):
        super().__init__(group)

        # Player Animations
        self.sprite_sheet = ss.SpriteSheet('./Sprite/characters/Player.png', 'player.json')
        self.status = 'down_idle'
        self.frame_index = 0

        # Collision
        self.collisionSprite = collision_sprites
        self.animation = self.sprite_sheet.sprites()

        # General attributes and animation
        self.image = self.animation[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        # change hitbox 
        self.hitbox = self.rect.copy().inflate((-126, -70))
        
        # change hitbox
        self.z = LAYERS['main']

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Timers for tool
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool swap': Timer(200)
        }

        # Basic tools setup
        self.tools = ['sword', 'pickaxe', 'axe']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Inventory
        self.item_inventory = {
            'wood': 0
        }

        # Interaction
        self.treeSprites = tree_sprites
        # self.interaction = interaction

    def use_tool(self):
        if self.selected_tool == 'pickaxe':
            pass
        if self.selected_tool == 'axe':
            for tree in self.treeSprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        if self.selected_tool == 'sword':
            pass

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animation[self.status]):
            self.frame_index = 0
    
        self.image = self.animation[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
            # and not self.sleep

            # Create direction
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
        
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # Equipment usage
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # Change current equipment
            if keys[pygame.K_e] and not self.timers['tool swap'].active:
                self.timers['tool swap'].activate()
                self.tool_index += 1
                # Ternary in python
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            # Set and interaction button
            if keys[pygame.K_f]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Boat':
                        self.status = 'left_idle'

    def get_status(self):

        # idle status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collisionSprite.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    # check collide in horizontal axis
                    if direction == 'horizontal':
                        if self.direction.x > 0: # check if the collision side is on right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # check if the collision side is on left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    # check collide in vertical axis
                    if direction == 'vertical':
                        if self.direction.y > 0: # check if the down side is collide
                            self.hitbox.up = sprite.hitbox.down
                        if self.direction.y < 0: # check if the up side collide
                            self.hitbox.up = sprite.hitbox.up
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    

    def move(self, dt):
        # normalize vector speed in same speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)