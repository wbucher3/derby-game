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
map_dict = retrieve_map_dict('map-2')

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

fence_group = pygame.sprite.GroupSingle(BasicSprite(pygame.image.load("imgs/" + map_directory + map_fence_file), (0,0)))

flag_group = pygame.sprite.Group()
flag_group.add(BasicSprite(pygame.image.load("imgs/carrots.png"), flag_position))

horse_group = pygame.sprite.Group()
for index in range(0, len(starting_position_list)):
    if index < len(horse_name_list):
        current = Horse(horse_name_list[index], starting_position_list[index][0], starting_position_list[index][1])
        horse_group.add(current)

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


        ## Horse Collision 
        horse_list = list(horse_group)
        for i in range(len(horse_list)):
            for j in range(i + 1, len(horse_list)):
                h1, h2 = horse_list[i], horse_list[j]
                if pygame.sprite.collide_mask(h1, h2):
                    delta = pygame.math.Vector2(h1.rect.center) - pygame.math.Vector2(h2.rect.center)
                    if delta.length_squared() > 0:
                        normal = delta.normalize()
                        h1.bounce(normal)
                        h2.bounce(-normal)

                        # Move them apart a little to avoid sticking
                        separation_distance = 5
                        h1.rect.center += (normal * separation_distance)
                        h2.rect.center -= (normal * separation_distance)

##########################################################
        
        # Collision with map mask
        for horse in horse_group:
            offset = (horse.rect.left - fence_group.sprite.rect.left,
                    horse.rect.top - fence_group.sprite.rect.top)
            if fence_group.sprite.mask.overlap(horse.mask, offset):
                if horse.velocity.length_squared() > 0:
                    # Step 1: Move the horse backward along its velocity until no longer colliding
                    direction = -horse.velocity.normalize()  # move backwards
                    limit = 10
                    current = 0
                    while fence_group.sprite.mask.overlap(horse.mask, offset) and current < limit:
                        horse.rect.x += direction.x
                        horse.rect.y += direction.y
                        offset = (horse.rect.left - fence_group.sprite.rect.left,
                                horse.rect.top - fence_group.sprite.rect.top)
                        current += 1

                    # Step 2: Bounce (reflect velocity)
                    horse.bounce(direction)



############################################

        flag_collide_dict = pygame.sprite.groupcollide(horse_group, flag_group, False, False, pygame.sprite.collide_mask)

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

            # for horse in horse_group:
            #     draw_mask_debug(screen, horse.mask, horse.rect.topleft, color=(0, 255, 0))  # Green for horse mask
            # draw_mask_debug(screen, fence_group.sprite.mask, fence_group.sprite.rect.topleft, color=(255, 0, 0))    # Red for wall mask
            pygame.display.flip()
            clock.tick(FPS)
        else:
            pygame.display.flip()
