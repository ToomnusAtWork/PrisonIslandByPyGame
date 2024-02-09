import pygame

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit
    
    # Load the specific image from specific rectangle
    def image_at(self, rectangle, colorkey = None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        
        if colorkey is not None:
            # Check for topleft pixel color and use that color
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    # Load whole bunch of images then return them as a list
    def images_at(self, rects, colorkey = None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images then return them as a list
    def load_strip(self, rect, image_count, colorkey = None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3] )
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
    
class SpriteStripAnim(object):
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        self.filename = filename
        SpriteImgSet = SpriteSheet(filename)
        self.images = SpriteImgSet.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self
        
        # playerImgs = []
        # # playerImgSet
        # playerImgs = playerImgSet.images_at(playerImgSet.image_at((0, 0, 16, 16), 
        #     (17, 0, 16, 16), (33, 0, 16, 16), (39, 0, 16, 16)), colorkey=(255, 255, 255))
        # print(playerImgs)