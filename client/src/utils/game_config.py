import os 

import pygame 

from .images import Images 
# from .sounds import Sounds 
from .window import Window


class GameConfig:
    # Game config class
    
    def __init__(
        self, 
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int, 
        window: Window,
        images: Images,
    ):
        self.screen = screen 
        self.clock = clock 
        self.fps = fps 
        self.window = window 
        self.images = images 
        
    def process(self):
        # Process game config in 1 game tick
        self.clock.tick(self.fps)
    