import sys 

import pygame 
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import *

from .utils import GameConfig, Images, Window


class GameClient:
    # Game client class
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mad Racer")
        window = Window(800, 600)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()
        
        self.config = GameConfig(
            screen = screen,
            clock=pygame.time.Clock(),
            fps=60,
            window=window, 
            images=images,
        )
        
    def start(self):
        # Handle game start
        pass 
    
    def menu(self):
        # Handle game menu
        pass

    def play(self):
        # Handle game play
        pass

    def 
        
        