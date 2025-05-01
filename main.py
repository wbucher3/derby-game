import pygame
import time
import math
import json
from MyPythonUtils.horse import Horse
from MyPythonUtils.basicsprite import BasicSprite
from MyPythonUtils.datafetch import retrieve_map_dict
from MyPythonUtils.datafetch import retrieve_horse_list

####################################################
##### Fetch all data 
####################################################

horse_name_list = retrieve_horse_list()
map_dict = retrieve_map_dict('map-5')

map_directory = map_dict['directory']
map_fence_file = map_dict['fenceName']
map_track_file = map_dict['trackName']
flag_position = (map_dict['flagPositon']['x'], map_dict['flagPositon']['y'])
starting_position_list = []
for position in map_dict['startingPositions']:
    starting_position_list.append((position['x'], position['y']))

####################################################
##### Initialize Pygame 
#################################################### 

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("The Derby!")
clock = pygame.time.Clock()
FPS = 30

####################################################
##### Create Sprite Groups
#################################################### 

track_group = pygame.sprite.GroupSingle(BasicSprite(pygame.image.load("imgs/" + map_directory + map_track_file), (0,0)))

fence_group = pygame.sprite.Group()
fence_group.add(BasicSprite(pygame.image.load("imgs/" + map_directory + map_fence_file), (0,0)))

flag_group = pygame.sprite.Group()
flag_group.add(BasicSprite(pygame.image.load("imgs/carrots.png"), flag_position))

horse_group = pygame.sprite.Group()
horse_individual_list = []
for index in range(0, len(starting_position_list)):
    if index < len(horse_name_list):
        current = Horse(horse_name_list[index], starting_position_list[index])
        horse_group.add(current)
        horse_individual_list.append(pygame.sprite.GroupSingle(current))


####################################################
##### Game Loop
####################################################  

run_game = True
race_is_ongoing = False
first_loop = True
race_has_been_finished = False

while run_game:

    # Draw all sprites before the race begins
    if first_loop:
        track_group.draw(screen)
        fence_group.draw(screen)
        horse_group.draw(screen)
        flag_group.draw(screen)
        pygame.display.flip()
        first_loop = False


    # keyboard listener for quiting or starting the race
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run_game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not(race_has_been_finished):
            race_is_ongoing = True

    # Race Loop
    if race_is_ongoing:
        
        # change the horse position based on angle and velocity
        horse_group.update()

        # detect wall or flag collisions
        wall_collide_dict = pygame.sprite.groupcollide(horse_group, fence_group, False, False, pygame.sprite.collide_mask)
        flag_collide_dict = pygame.sprite.groupcollide(horse_group, flag_group, False, False, pygame.sprite.collide_mask)

        # detect horse collisions -- this is kind of messy, probs a better way
        for horse1 in horse_individual_list:
            for horse2 in horse_individual_list: 
                if horse1.sprite.name == horse2.sprite.name:
                    continue
                temp_dict = pygame.sprite.groupcollide(horse1, horse2, False, False, pygame.sprite.collide_mask)
                for horse in temp_dict:
                    horse.bounce()

        # handle any collisions with walls
        for horse in wall_collide_dict:
            horse.bounce()

        # handle flag collisions -- win condition
        for horse in flag_collide_dict:
            race_is_ongoing = False
            race_has_been_finished = True
            horse.display_celebration(screen, (WIDTH/2, HEIGHT/2))
            horse.display_name(screen, (WIDTH/2, HEIGHT * 0.75))
            break # we only want the first horse in the dictionary, dont care if this brings on bugs

        # draw the screen after all the logic is complete
        if race_is_ongoing:
            track_group.draw(screen)
            fence_group.draw(screen)
            horse_group.draw(screen)
            flag_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
        else:
            pygame.display.flip()
