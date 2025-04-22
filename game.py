import pygame
import time
import math
from util import scale_image
from horse import Horse
from basicsprite import BasicSprite

pygame.init()

def draw_background(win, images):
    for img, pos in images:
        win.blit(img, pos)

# Load the images 
GRASS_IMG = scale_image(pygame.image.load("imgs/grass.png"), 0.8)
TRACK_IMG = scale_image(pygame.image.load("imgs/track.png"), 0.8)
# Static images
images = [(GRASS_IMG, (0, 0)), (TRACK_IMG, (0, 0))]

# Using the images, set up the window
WIDTH, HEIGHT = TRACK_IMG.get_width(), TRACK_IMG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Derby!")
clock = pygame.time.Clock()
FPS = 30
run = True
start = False


# Load the fence
FENCE = scale_image(pygame.image.load("imgs/fence.png"), 0.8)
FENCE_BORDER_MASK = pygame.mask.from_surface(FENCE)

# Load the finish line
FINISH = scale_image(pygame.image.load("imgs/flag.png"), 0.8)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (1350,700)



red_horse = Horse("Red", 10, 10, 10, 10, 10, (90, 110))
purple_horse = Horse("Purple", 10, 10, 10, 10, 10, (190, 210))
green_horse = Horse("Green", 10, 10, 10, 10, 10, (290, 310))


horse_group = pygame.sprite.Group()
horse_group.add(red_horse)
horse_group.add(purple_horse)
horse_group.add(green_horse)

fence_sprite = BasicSprite(FENCE, (0,0))
flag_sprite = BasicSprite(FINISH, FINISH_POSITION)

fence_group = pygame.sprite.Group()
fence_group.add(fence_sprite)

flag_group = pygame.sprite.Group()
flag_group.add(flag_sprite)



while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
    
    fence_group.update()
    horse_group.update()
    flag_group.update()

    wall_collide_dict = test_collisions = pygame.sprite.groupcollide(horse_group, fence_group, False, False, pygame.sprite.collide_mask)

    for horse in wall_collide_dict:
        print(horse.name + " collided with fence!")
        horse.bounce()


    draw_background(WIN, images)
    fence_group.draw(WIN)
    horse_group.draw(WIN)
    flag_group.draw(WIN)


    pygame.display.flip()
    clock.tick(FPS)
    # Handles the Quit






pygame.quit()