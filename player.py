import pygame
import spritesheet as ss

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Player Animations
        self.sprite_sheet = ss.SpriteSheet('./Sprite/characters/player.png', 'player.json')
        self.animation = self.sprite_sheet.sprites()

        self.status = 'down_idle'
        self.frame_index = 0

        # General attributes and animation
        self.image = self.animation[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2()
        self.speed = 10
        self.animation_status = self.animation.keys()


    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animation[self.status]):
            self.frame_index = 0

        self.image = self.animation[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()

        # Create direction
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
            self.status = 'up_idle'
    
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
                self.timers[''].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def get_status(self):

        # idle status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        # if self.timers['tool']

    # def update_timers(self):
        # for timer in self.timer_values():
        #     pass


    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        #vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y


    def update(self, dt):
        self.input()
        self.get_status()
        # self.update_timers()

        self.move(dt)
        self.animate(dt)