import pygame
import time
import math
from util import scale_image
from horse import Horse

# Load the images 
GRASS = scale_image(pygame.image.load("imgs/grass.png"), 0.8)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.8)

# Load the fence
FENCE = scale_image(pygame.image.load("imgs/fence.png"), 0.8)
FENCE_BORDER_MASK = pygame.mask.from_surface(FENCE)

# Load the finish line
FINISH = scale_image(pygame.image.load("imgs/flag.png"), 0.8)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (1350,700)

# Using the images, set up the window
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Derby!")


clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (FENCE, (0, 0))]

red_horse = Horse("Red", 10, 10, 10, 10, 10, (90, 110))
purple_horse = Horse("Purple", 10, 10, 10, 10, 10, (190, 210))
green_horse = Horse("Green", 10, 10, 10, 10, 10, (290, 310))
horses = [purple_horse, red_horse, green_horse]


FPS = 60


def draw(win, images, horses):
    for img, pos in images:
        win.blit(img, pos)
    
    for horse in horses:
        horse.draw(win)

    pygame.display.update()



run = True
start = False

while run:

# Set up the clock and draw the sprites
    clock.tick(FPS)
    draw(WIN, images, horses)
    keys = pygame.key.get_pressed()

# Handles the Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
    

# Starts the Race!
    if keys[pygame.K_SPACE]:
        start = True


# Game loop
    if start:
        purple_horse.move_forward()
        

        if purple_horse.collide(FENCE_BORDER_MASK) != None:
            purple_horse.bounce()

        finish_poi_collide = purple_horse.collide(FINISH_MASK, *FINISH_POSITION)

        if finish_poi_collide != None:
            if finish_poi_collide[1] != 0:
                purple_horse.reset()
                print("You Won! Resetting Game...")



pygame.quit()