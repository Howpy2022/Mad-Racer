import os
import sys
import math

from network import Network

import pygame

# Utils
def scale_image(img, new_width = None, new_height = None):
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
        center = img.get_rect(topleft = top_left).center)
    win.blit(rot_img, new_rect.topleft)



# Configuration
# initializes all imported pygame modules
pygame.init()
fps = 60
# creates an object to keep track of time
fpsClock = pygame.time.Clock()
width, height = 640, 480
# initializes a window or screen for display
screen = pygame.display.set_mode((width, height))
# creates a font object from the list of fonts from the computer system
font = pygame.font.SysFont('Arial', 40)

# global list of button objects
objects = []
start_objects = [] 

screen_mode = "start" # start, menu, settings, map_sketch, lobby, map_select, game, game_over

# loads a new in image from a file or a file-like object
background = scale_image(pygame.image.load("./grass2.jpg").convert(), 1280, 960)
background_location = [0, 0]
# gives coordinates for a rectangular object
background_rect =  pygame.Rect(0, 0, 1280, 960)



class Button():
    def __init__(self, x, y, width, height, buttonText = 'Button', onclickFunction = None, onePress = False, screen_mode = ""):
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

        # overall button surface (i.e. background); represents images
        self.buttonSurface = pygame.Surface((self.width, self.height))
        
        # overall button rectangle; gives rectangular coordinates for a rectangular object 
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # button text surface; draws a text on a new surface
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
       
        # whether button is pressed
        self.alreadyPressed = False

        self.screen_mode = screen_mode
        
        objects.append(self)

    def process(self):
        # TODO: add pos argument (for position of mouse or etc)
        # process button
        # checks the positioning of the mouse's pointer 
        mousePos = pygame.mouse.get_pos()

        # fills surface with specified color
        self.buttonSurface.fill(self.fillColors['normal'])
        # detects if the pointer is on top of the button
        if self.buttonRect.collidepoint(mousePos):
            # fills surface with specified color when on the button
            self.buttonSurface.fill(self.fillColors['hover'])

            # detects if the button is pressed by pushing the mouse down 
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                # fills surface with specified color when pressed
                self.buttonSurface.fill(self.fillColors['pressed'])
                
                # detects if the mouse button is pressed once
                if self.onePress:
                    # runs a predefined function when button is clicked --> (i.e. change to designated page)
                    self.onclickFunction()

                # in case if the mouse button has not been pressed
                elif not self.alreadyPressed:
                    # runs a predefined function when button is clicked --> (i.e. change to designated page)
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False
        # draws one image onto another
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        # draws one image onto another
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
        screen.fill((255, 51, 51))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # draw title text 
        titleText = font.render('Mad Racer', True, (255, 255, 255))
        screen.blit(titleText, (230, 220))
        
        for object in objects:
            if object.screen_mode == "start":
                object.process()

        pygame.display.flip()
        fpsClock.tick(60)
            

def menu_screen():
    # Handle menu screen
    if screen_mode == "menu":
        screen.fill((255, 51, 51))
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
        screen.fill((255, 51, 51))
        # gets events for the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # unitinitalizes all pygame modules
                pygame.quit()
                sys.exit()

        # draw settings text 
        settingsText = font.render('Settings', True, (255, 255, 255))
        screen.blit(settingsText, (250, 30))

        settingsText = font.render('Volume', True, (255, 255, 255))
        screen.blit(settingsText, (10, 110))

        settingsText = font.render('Username', True, (255, 255, 255))
        screen.blit(settingsText, (10, 210))

        settingsText = font.render('Screen Resolution', True, (255, 255, 255))
        screen.blit(settingsText, (10, 310))

        settingsText = font.render('Keymap', True, (255, 255, 255))
        screen.blit(settingsText, (10, 410))
        
        for object in objects:
            if object.screen_mode == "settings":
                object.process()
        # updates the full display Surface to the screen
        pygame.display.flip()
        # gives out the clock time in frames per second
        fpsClock.tick(60)


class Maps(pygame.sprite.Sprite):
    def __init__(self, tile_map, y, x, rot):
        map_files = []
        map_tile = ['X.png', 'I.png', 'L.png', 'T.png', '0.png', 'null.png']

        crossing = 0
        straight = 1
        turn = 2
        split = 3
        deadend = 4
        null = 5

        map_1 = [
                    [2, 1, 3, 1, 1, 3, 1, 1, 1, 4],
                    [1, 5, 1, 5, 4, 0, 1, 2, 5, 4],
                    [1, 4, 3, 1, 3, 3, 1, 3, 2, 1],
                    [3, 1, 3, 1, 3, 5, 4, 5, 1, 1],
                    [3, 2, 1, 5, 1, 5, 3, 1, 0, 3],
                    [1, 2, 0, 1, 0, 3, 0, 4, 1, 1],
                    [1, 5, 1, 4, 2, 1, 1, 2, 3, 1],
                    [1, 2, 0, 1, 3, 3, 0, 0, 2, 1],
                    [1, 1, 4, 2, 2, 5, 1, 2, 1, 3],
                    [2, 3, 1, 3, 1, 1, 3, 1, 1, 2]
        ]

        pygame.sprite.Sprite.__init__(self)
        self.image = map_files[tile_map]
        self.rect = self.image.get_rect()

        if rot != 0:
            self.image = pygame.transform.rotate(self.image, r * 90)
        
        self.x = x
        self.y = y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left = False, right = False):
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
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x = 0, y = 0):
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

RED_CAR = scale_image(pygame.image.load("./red-car.png").convert_alpha(), new_width = 20)
GREY_CAR = scale_image(pygame.image.load("./grey-car.png").convert_alpha(), new_width = 20)

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
        
    def process(self, win = None, draw=False):
        # Handle display
        if draw:
            if win is None:
                    self.draw(screen)
            else:
                self.draw(win)
            
        # Handle movement
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            self.rotate(left = True)
        if keys[pygame.K_d]:
            self.rotate(right = True)
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
        
        player_car.process(draw=True)
        
        # send network stuff
        # calculate player car x, y relative to background (absolute position)
        player_x = player_car.x - background_location[0]
        player_y = player_car.y - background_location[1]
        player2_x, player2_y, player2_angle = parse_data(send_data(player_x, player_y, player_car.angle))
        
        # set player car 2 x, y relative to current background (absolute position -> relative)
        player_car2.x = player2_x + background_location[0]
        player_car2.y = player2_y + background_location[1]
        player_car2.angle = player2_angle
        
        # player_car.draw(screen)
        player_car2.draw(screen)
        
        pygame.display.flip()
        fpsClock.tick(60)
        
        
        

customButton = Button(250, 420, 150, 50, 'Play', handleToMenu, False, "start")
customButton = Button(480, 30, 150, 50, 'Settings', handleToSettings, False, "start")

customButton = Button(480, 30, 150, 50, 'Close', handleToStart, False, "menu")
customButton = Button(250, 140, 150, 50, 'Host', handleToGame, False, "menu")
customButton = Button(250, 250, 150, 50, 'Join', myFunction, False, "menu")

customButton = Button(480, 30, 150, 50, 'Close', handleToStart, False, "settings")
customButton = Button(320, 110, 150, 50, 'On', handleToStart, False, "settings")
customButton = Button(480, 110, 150, 50, 'Off', handleToStart, False, "settings")

player_car = PlayerCar(8, 8)
player_car2 = PlayerCar(8, 8)
player_car2.img = GREY_CAR

network = Network()

def send_data(x, y, angle):
    global network 
    
    data = f"{network.id}:{x},{y},{angle}"
    reply = network.send(data)
    
    return reply 

def parse_data(data):
    try:
        d = data.split(":")[1].split(",")
        return float(d[0]), float(d[1]), float(d[2])
    except:    
        return 0,0,0
    

# Game loop 
while True:
    # EVENTS 
	
	
    # DISPLAY 
            
    start_screen()
    menu_screen()
    settings_screen()
    game_screen()
    

