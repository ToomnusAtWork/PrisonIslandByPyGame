import pygame
import spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # General attributes
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2()
        self.speed = 10

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 
                        'right': [], 'left': [],
                        'up_idle': [], 'down_idle': [],
                        'right_idle': [], 'left_idle': [],
                        'up_sword': [], 'down_sword': [], 
                        'right_sword': [], 'left_sword': []}
        # img in up down
        

    def animate(self, dt):
        pass

    def input(self):
        keys = pygame.key.get_pressed()

        # Create direction
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = 1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = -1
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

        # idle movement
        if self.direction.magnitude() == 0:
            pass
            # self.status = self.status.split('_')[0] + '_idle'
        
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