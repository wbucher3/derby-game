import pygame
import math
import random
from MyPythonUtils.util import scale_image

class Horse(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.x, self.y = x, y
        self.image = scale_image(pygame.image.load("imgs/horses/" + name + ".png"), 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.rect.x = x
        self.rect.y = y
        self.speed = 7
        random_starting_angle = math.radians(random.randint(0, 360))
        self.x_speed = self.speed * math.cos(random_starting_angle)
        self.y_speed = self.speed * math.sin(random_starting_angle)


    def update(self, horse_group, wall_group):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        for other_horse in horse_group:
            if other_horse != self and pygame.sprite.collide_mask(self, other_horse):
                self.handle_horse_collision(other_horse)

        for wall in wall_group:
            if pygame.sprite.collide_mask(self, wall):
                self.handle_wall_collision(wall)

    def handle_wall_collision(self, wall):
        offset_x = self.rect.x - wall.rect.x
        offset_y = self.rect.y - wall.rect.y
        offset = (offset_x, offset_y)
        overlap_point = wall.mask.overlap(self.mask, offset)

        dx = overlap_point[0] - self.rect.centerx
        dy = overlap_point[1] - self.rect.centery
        collision_angle = math.atan2(dy, dx)

        if abs(math.degrees(collision_angle)) < 45 or abs(math.degrees(collision_angle)) > 135:
            self.bounce_x()
        else:
            self.bounce_y()

        self.move_apart_wall(wall)

    def handle_horse_collision(self, other_sprite):
        offset_x = self.rect.centerx - other_sprite.rect.centerx
        offset_y = self.rect.centery - other_sprite.rect.centery
        offset = (offset_x, offset_y)
        overlap_point = other_sprite.mask.overlap(self.mask, offset)

        dx = overlap_point[0] - self.rect.centerx
        dy = overlap_point[1] - self.rect.centery
        collision_angle = math.atan2(dy, dx)

        # Calculate the collision angle
        # collision_angle = math.atan2(dy, dx)

        # Calculate the velocities of the sprites
        v1 = math.sqrt(self.x_speed * self.x_speed + self.y_speed * self.y_speed)
        v2 = math.sqrt(other_sprite.x_speed * other_sprite.x_speed + other_sprite.y_speed * other_sprite.y_speed)

        # Calculate the angles of the velocities

        angle1 = math.atan2(self.y_speed, self.x_speed)
        angle2 = math.atan2(other_sprite.y_speed, other_sprite.x_speed)

        # Calculate the new velocities after the collision
        new_angle1 = 2 * collision_angle - angle1
        new_angle2 = 2 * collision_angle - angle2

        # Update the speeds of the sprites
        self.x_speed = self.x_speed * -1
        self.y_speed = self.y_speed * -1

        other_sprite.x_speed = other_sprite.x_speed * -1
        other_sprite.y_speed = other_sprite.y_speed * -1

        self.speed = math.sqrt(self.x_speed**2 + self.y_speed**2)
        other_sprite.speed = math.sqrt(other_sprite.x_speed**2 + other_sprite.y_speed**2)

        # Move the sprite out of the wall
        self.move_apart_horse(other_sprite)

    def move_apart_horse(self, other_sprite):
        offset_x = self.rect.x - other_sprite.rect.x
        offset_y = self.rect.y - other_sprite.rect.y
        offset = (offset_x, offset_y)
        overlap_point = other_sprite.mask.overlap(self.mask, offset)

        if overlap_point:
            overlap_x_world = other_sprite.rect.x + overlap_point[0]
            overlap_y_world = other_sprite.rect.y + overlap_point[1]

            center1_x = other_sprite.rect.centerx
            center1_y = other_sprite.rect.centery

            direction_x = overlap_x_world - center1_x
            direction_y = overlap_y_world - center1_y

            magnitude = (direction_x**2 + direction_y**2)**0.5
            if magnitude > 0:
                normal_x = direction_x / magnitude
                normal_y = direction_y / magnitude
            else:
                normal_x = 1
                normal_y = 0

            separation_amount = 2
            self.rect.x -= normal_x * separation_amount
            self.rect.y -= normal_y * separation_amount
            other_sprite.rect.x -= normal_x * separation_amount
            other_sprite.rect.y -= normal_y * separation_amount
            
    def move_apart_wall(self, wall):
        offset_x = self.rect.centerx - wall.rect.centerx
        offset_y = self.rect.centery - wall.rect.centery
        offset = (offset_x, offset_y)
        overlap_point = wall.mask.overlap(self.mask, offset)

        if overlap_point:
            overlap_x_world = wall.rect.x + overlap_point[0]
            overlap_y_world = wall.rect.y + overlap_point[1]

            center1_x = wall.rect.centerx
            center1_y = wall.rect.centery

            direction_x = overlap_x_world - center1_x
            direction_y = overlap_y_world - center1_y

            magnitude = (direction_x**2 + direction_y**2)**0.5
            if magnitude > 0:
                normal_x = direction_x / magnitude
                normal_y = direction_y / magnitude
            else:
                normal_x = 1
                normal_y = 0

            separation_amount = 2
            self.rect.x -= normal_x * separation_amount
            self.rect.y -= normal_y * separation_amount

    def display_celebration(self, window, center):
        self.image = scale_image(pygame.image.load("imgs/horses/" + self.name + ".png"), 7)
        self.rect = self.image.get_rect(center=center)
        x,y = center
        self.rect.x = x - (self.rect.width / 2)
        self.rect.y = y - (self.rect.height / 2)
        window.blit(self.image, (self.rect.x, self.rect.y))

    def bounce_x(self):
        """Reverse horizontal velocity."""
        self.x_speed *= -1
        self.angle_radians = math.atan2(self.y_speed, self.x_speed)

    def bounce_y(self):
        """Reverse vertical velocity."""
        self.y_speed *= -1
        self.angle_radians = math.atan2(self.y_speed, self.x_speed)

    def display_name(self, window, center):
        white = (255, 255, 255)
        black = (0, 0, 0)
        font = pygame.font.Font('assets/Comic-Sans-MS.ttf', 120)
        text = font.render(self.name + " is Victorious!", True, white, black)
        textRect = text.get_rect()
        textRect.center = center
        window.blit(text, textRect)