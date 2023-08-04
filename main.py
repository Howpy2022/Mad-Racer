import sys
import math 

import pygame

# Utils 
def scale_image(img, new_width=None, new_height=None):
    # Scales the pygame img to (new_width, new_height)
    # At least one of new_width, new_height must be given
    # If only one is given, the other is scaled to maintain aspect ratio
    assert (new_width is not None or new_height is not None)
    
    if new_width is not None and new_height is None:
        width, height = img.get_size()
        ratio = new_width / width
        new_height = int(height * ratio)
    elif new_height is not None and new_width is None:
        width, height = img.get_size()
        ratio = new_height / height
        new_width = int(width * ratio)
    
    size = round(new_width), round(new_height)
    return pygame.transform.scale(img, size)


def draw_image(win, img, top_left, angle):
    # Draws the image with top_left positioning and angle rotation about the center 
    rot_img = pygame.transform.rotate(img, angle)
    new_rect = rot_img.get_rect(
        center=img.get_rect(topleft=top_left).center)
    win.blit(rot_img, new_rect.topleft)



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


background = scale_image(pygame.image.load("./grass2.jpg"), 1280, 960)
background_location = [0, 0]
background_rect =  pygame.Rect(0, 0, 1280, 960)



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
    
def handleToGame():
    print("Button Pressed")
    
    global screen_mode
    screen_mode = "game"            

def start_screen():
    # Handle start screen
    if screen_mode == "start":
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # draw title text 
        titleText = font.render('Mad Racer', True, (255, 255, 255))
        screen.blit(titleText, (30, 30))
        
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

        # draw settings text 
        settingsText = font.render('Settings', True, (255, 255, 255))
        screen.blit(settingsText, (30, 30))
        
        for object in objects:
            if object.screen_mode == "settings":
                object.process()

        pygame.display.flip()
        fpsClock.tick(60)


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        draw_image(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        # TODO: decelerate instead?
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

# CAR_WIDTH = 20
# CAR_HEIGHT = 50
# RED_CAR = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
# RED_CAR.fill((255, 0, 0))

RED_CAR = scale_image(pygame.image.load("./red-car.png"), new_width=20)

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    # START_POS = (180, 200)
    START_POS = (width // 2, height // 2)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()
    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        background_location[0] += horizontal
        background_location[1] += vertical
        # self.y -= vertical
        # self.x -= horizontal
        
    def process(self, win=None):
        # Handle display
        if win is None:
                self.draw(screen)
        else:
            self.draw(win)
            
        # Handle movement
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            self.move_forward()
        if keys[pygame.K_s]:
            moved = True
            self.move_backward()

        if not moved:
            self.reduce_speed()
            
            


def game_screen():
    # Handle racing game screen
    if screen_mode == "game":
        
        screen.fill((20, 20, 20))
        background_rect = pygame.Rect(background_location[0], background_location[1], 1280, 960)
        # background_rect =  pygame.Rect(0, 0, 1280, 960)

        screen.blit(background, background_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player_car.process()

        pygame.display.flip()
        fpsClock.tick(60)
        
        
        

customButton = Button(30, 100, 400, 100, 'Play', handleToMenu, False, "start")
customButton = Button(30, 210, 400, 100, 'Settings', handleToSettings, False, "start")

customButton = Button(30, 30, 400, 100, 'Close', handleToStart, False, "menu")
customButton = Button(30, 140, 400, 100, 'Host', handleToGame, False, "menu")
customButton = Button(30, 250, 400, 100, 'Join', myFunction, False, "menu")

customButton = Button(30, 100, 400, 100, 'Close', handleToStart, False, "settings")

player_car = PlayerCar(8, 8)

# Game loop 
while True:
    # EVENTS 
	
	
    # DISPLAY 
            
    start_screen()
    menu_screen()
    settings_screen()
    game_screen()
    

