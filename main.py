import pygame
import time
import math
from MyPythonUtils.util import scale_image
from MyPythonUtils.horse import Horse
from MyPythonUtils.basicsprite import BasicSprite
import json

pygame.init()

# Open and read the JSON file
global map_data
with open('assets/maps.json', 'r') as file:
    global map_data
    map_data = json.load(file)

global horse_data
with open('assets/horses.json', 'r') as file:
    global horse_data
    horse_data = json.load(file)

horse_name_list = horse_data['horses']

map_dict = map_data['map-1']
map_directory = map_dict['directory']
map_fence_file = map_dict['fenceName']
map_track_file = map_dict['trackName']
flag_position = (map_dict['flagPositon']['x'], map_dict['flagPositon']['y'])
starting_position_list = []
for position in map_dict['startingPositions']:
    starting_position_list.append((position['x'], position['y']))


# Load the track background
TRACK_IMG = scale_image(pygame.image.load("imgs/" + map_directory + map_track_file), 1)

# Load the fence 
FENCE = scale_image(pygame.image.load("imgs/" + map_directory + map_fence_file), 1)
FENCE_BORDER_MASK = pygame.mask.from_surface(FENCE)

# Load the finish line
FINISH = scale_image(pygame.image.load("imgs/flag.png"), 0.8)
FINISH_MASK = pygame.mask.from_surface(FINISH)
# FINISH_POSITION = (1150,600)

# Using the images, set up the window
WIDTH, HEIGHT = TRACK_IMG.get_width(), TRACK_IMG.get_height()
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("The Derby!")
clock = pygame.time.Clock()
FPS = 30

# Set up all sprite groups for map, fence, and horses
fence_sprite = BasicSprite(FENCE, (0,0))
flag_sprite = BasicSprite(FINISH, flag_position)

fence_group = pygame.sprite.Group()
fence_group.add(fence_sprite)

flag_group = pygame.sprite.Group()
flag_group.add(flag_sprite)

# adds only horses for the amount of spots allowed on track
horse_group = pygame.sprite.Group()
for index in range(0, len(starting_position_list)):
    if index < len(horse_name_list):
        horse_group.add(Horse(horse_name_list[index], starting_position_list[index]))
    

run_game = True
race_is_ongoing = False
first_loop = True
race_has_been_finished = False

while run_game:

    # Draw everything before the race begins
    if first_loop:
        WIN.blit(TRACK_IMG, (0,0))
        fence_group.draw(WIN)
        horse_group.draw(WIN)
        flag_group.draw(WIN)
        pygame.display.flip()
        first_loop = False


    # key listener for quiting or starting the race
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run_game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not(race_has_been_finished):
            race_is_ongoing = True

    # Race Loop
    if race_is_ongoing:
        
        horse_group.update()

        wall_collide_dict = pygame.sprite.groupcollide(horse_group, fence_group, False, False, pygame.sprite.collide_mask)
        flag_collide_dict = pygame.sprite.groupcollide(horse_group, flag_group, False, False, pygame.sprite.collide_mask)

        # horse_collide_dict = pygame.sprite.groupcollide(horse_group, horse_group, False, False, pygame.sprite.collide_mask)
        
        # for horse in horse_collide_dict:
        #     horse.bounce()

        for horse in wall_collide_dict:
            horse.bounce()

        for horse in flag_collide_dict:
            race_is_ongoing = False
            race_has_been_finished = True
            horse.display_celebration(WIN, (WIDTH/2, HEIGHT/2))
            horse.display_name(WIN, (WIDTH/2, HEIGHT * 0.75))
            break # we only want the first horse in the dictionary, dont care if this brings on bugs

        if race_is_ongoing:
            WIN.blit(TRACK_IMG, (0,0))
            fence_group.draw(WIN)
            horse_group.draw(WIN)
            flag_group.draw(WIN)
            pygame.display.flip()
            clock.tick(FPS)
        else:
            pygame.display.flip()



# pygame.quit()