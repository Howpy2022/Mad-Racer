import sys

import pygame


# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 40)

# global list of button objects
objects = []
start_objects = [] 

screen_mode = "start" # start, menu, settings, map_sketch, lobby, map_select, game, game_over


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, screen_mode=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        # overall button surface (i.e. background)
        self.buttonSurface = pygame.Surface((self.width, self.height))
        # overall button rectangle 
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # button text surface 
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        # whether button is pressed
        self.alreadyPressed = False

        self.screen_mode = screen_mode
        
        objects.append(self)

    def process(self):
        # TODO: add pos argument (for position of mouse or etc)
        # process button 
        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

def myFunction():
    print('Button Pressed')

def handleToSettings():
    global screen_mode
    screen_mode = "settings"

def handleToMenu():
    global screen_mode
    screen_mode = "menu"

def handleToStart():
    global screen_mode
    screen_mode = "start"            

def start_screen():
    # Handle start screen
    if screen_mode == "start":
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object in objects:
            if object.screen_mode == "start":
                object.process()

        pygame.display.flip()
        fpsClock.tick(60)
            

def menu_screen():
    # Handle menu screen
    if screen_mode == "menu":
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object in objects:
            if object.screen_mode == "menu":
                object.process()

        pygame.display.flip()
        fpsClock.tick(60)
    
def settings_screen():
    # Handle setting screen
    if screen_mode == "settings":
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object in objects:
            if object.screen_mode == "settings":
                object.process()

        pygame.display.flip()
        fpsClock.tick(60)


customButton = Button(30, 30, 400, 100, 'Play', handleToMenu, True, "start")
customButton = Button(30, 140, 400, 100, 'Settings', handleToSettings, True, "start")

customButton = Button(30, 30, 400, 100, 'Close', handleToStart, True, "menu")
customButton = Button(30, 140, 400, 100, 'Host', myFunction, True, "menu")
customButton = Button(30, 250, 400, 100, 'Join', myFunction, True, "menu")

customButton = Button(30, 30, 400, 100, 'Close', handleToStart, True, "settings")

# Game loop 
while True:
    # EVENTS 
	
	
    # DISPLAY 
            
    start_screen()
    menu_screen()
    settings_screen()
    
    

