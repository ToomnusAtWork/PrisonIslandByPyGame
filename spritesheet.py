import pygame, io, json

# Sprite Sheet
SPRITESHEETMAP = 'SpriteSheetMap'
DIMS = 'Dimensions'
VALUES_MAP='Values_Map'
SPRITE_DETAILS = 'sprite_details'
ROW = 'row'
COUNT = 'count'
START = 'start'
class SpriteSheet(object):
    def __init__(self, filename, manual):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.spritesheetdata = manual
        except pygame.error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit
        
        self.file = filename
        self.dims = (0, 0)
        self.valuekeys = []
        self.valuemap  = {}
        self.anim = {}
        self.get_sprites_data()
        self.spritesheetimg = self.get_spritesheet_image()
        self.sprite = self.get_sprites()

    def get_spritesheet_image(self) -> pygame.Surface:
        return pygame.image.load(self.file).convert_alpha()
    
    def get_sprites_data(self):
        ssmap = io.FileIO(self.spritesheetdata, 'r+')
        ssmapdata = json.load(ssmap).get(SPRITESHEETMAP)
        self.dimensions(ssmapdata.get(DIMS))

        self.valuemap_lines(ssmapdata.get(VALUES_MAP))
        for x in self.valuemap_lines():
            self.anim[x] = self.valuemap_lines()[x].get(SPRITE_DETAILS)
    
    def get_sprites(self):
        ret = dict()
        for key in self.anim:
            ta = []
            spriteData = self.anim[key]
            row = spriteData.get("row")
            count = spriteData.get("count")
            start = spriteData.get("start")
            i = 0

            while i < count:
                tup = (
                    (start)+(self.dimensions()[0]*i),
                    (self.dimensions()[1]*row)
                )+self.dimensions()
                ta.append(self.spritesheetimg.subsurface(tup))
                i += 1
            ret[key] = ta
        return ret
        
    def sprites(self) -> dict:
        return self.sprite
    
    def dimensions(self,s=None) -> tuple:
        if s != None:
            self.dims = s
        return tuple(self.dims)
    
    def valuemap_lines(self,s=None) -> dict:
        if s != None:
            self.valuemap = s
        return self.valuemap


# class SpriteStripAnim(object):
#     def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
#         self.filename = filename
#         SpriteImgSet = SpriteSheet(filename)
#         self.images = SpriteImgSet.load_strip(rect, count, colorkey)
#         self.i = 0
#         self.loop = loop
#         self.frames = frames
#         self.f = frames

#     def iter(self):
#         self.i = 0
#         self.f = self.frames
#         return self
    
#     def next(self):
#         if self.i >= len(self.images):
#             if not self.loop:
#                 raise StopIteration
#             else:
#                 self.i = 0
#         image = self.images[self.i]
#         self.f -= 1
#         if self.f == 0:
#             self.i += 1
#             self.f = self.frames
#         return image
    
#     def __add__(self, ss):
#         self.images.extend(ss.images)
#         return self
        
# # Load the specific image from specific rectangle
#     def image_at(self, rectangle, colorkey = None):
#         rect = pygame.Rect(rectangle)
#         image = pygame.Surface(rect.size).convert()
#         image.blit(self.sheet, (0,0), rect)
        
#         if colorkey is not None:
#             # Check for topleft pixel color and use that color
#             if colorkey == -1:
#                 colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey, pygame.RLEACCEL)
#         return image
    
#     # Load whole bunch of images then return them as a list
#     def images_at(self, rects, colorkey = None):
#         return [self.image_at(rect, colorkey) for rect in rects]

#     # Load a whole strip of images then return them as a list
#     def load_strip(self, rect, image_count, colorkey = None):
#         tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3] )
#                 for x in range(image_count)]
#         return self.images_at(tups, colorkey)
