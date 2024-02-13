import pygame
from settings import *

class Overlay:
    def __init__(self, player):

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        #set path for tool overlay in screen
        overlay_path = './Sprite/overlay/'
        self.tools_surf = {tool:pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}

    def display(self):

        # import tools for displaying
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_surf = pygame.transform.scale(tool_surf, (50, 50))
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

