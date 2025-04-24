import pygame
import math
import random

class MovingSprite(pygame.sprite.Sprite):
    """
    A sprite that moves and bounces off walls and other sprites.
    """
    def __init__(self, x, y, image, speed, angle_degrees, size):
        """
        Initialize the MovingSprite.

        Args:
            x (int): Initial X position.
            y (int): Initial Y position.
            image (pygame.Surface): The sprite's image.
            speed (int or float): The speed of the sprite.
            angle_degrees (int or float): Initial angle.
            size (int): The size of the sprite.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle_radians = math.radians(angle_degrees)
        self.x_speed = speed * math.cos(self.angle_radians)
        self.y_speed = speed * math.sin(self.angle_radians)
        self.size = size

    def update(self, screen_width, screen_height, wall_group, other_sprites):
        """
        Update the sprite's position and handle bouncing off walls and other sprites.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            wall_group (pygame.sprite.Group): Group containing the wall sprites.
            other_sprites (pygame.sprite.Group): Group of other moving sprites.
        """
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Bounce off screen edges
        if self.rect.left < 0:
            self.rect.left = 0
            self.bounce_x()
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.bounce_x()
        if self.rect.top < 0:
            self.rect.top = 0
            self.bounce_y()
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.bounce_y()

        # Check for collision with wall sprites
        for wall in wall_group:
            if pygame.sprite.collide_rect(self, wall):
                self.handle_wall_collision(wall)

        # Check for collision with other moving sprites
        for other_sprite in other_sprites:
            if other_sprite != self and pygame.sprite.collide_rect(self, other_sprite):
                self.handle_sprite_collision(other_sprite)

    def bounce_x(self):
        """Reverse horizontal velocity."""
        self.x_speed *= -1
        self.angle_radians = math.atan2(self.y_speed, self.x_speed)

    def bounce_y(self):
        """Reverse vertical velocity."""
        self.y_speed *= -1
        self.angle_radians = math.atan2(self.y_speed, self.x_speed)

    def handle_wall_collision(self, wall):
        """
        Handle collision with a wall sprite.  Bounce logic.
        """
        # Calculate the collision angle
        dx = wall.rect.centerx - self.rect.centerx
        dy = wall.rect.centery - self.rect.centery
        collision_angle = math.atan2(dy, dx)

        # Determine which side of the wall was hit
        if abs(math.degrees(collision_angle)) < 45 or abs(math.degrees(collision_angle)) > 135:
            self.bounce_x()  # Bounce horizontally
        else:
            self.bounce_y()  # Bounce vertically

        # Move the moving sprite out of the wall
        self.move_apart(wall)

    def handle_sprite_collision(self, other_sprite):
        """
        Handle collision with another moving sprite.
        """
        # Calculate the collision angle
        dx = other_sprite.rect.centerx - self.rect.centerx
        dy = other_sprite.rect.centery - self.rect.centery
        collision_angle = math.atan2(dy, dx)

        # Calculate the velocities of the sprites after collision
        v1 = self.speed
        v2 = other_sprite.speed

        # Calculate the angles of the velocities
        angle1 = self.angle_radians
        angle2 = other_sprite.angle_radians

        # Calculate new speeds and angles after collision.  This is simplified because mass is the same.
        new_x_speed1 = (v1 * math.cos(angle1 - collision_angle) * (0) + 2 * v2 * math.cos(angle2 - collision_angle)) / (2) * math.cos(collision_angle) + v1 * math.sin(angle1 - collision_angle) * math.cos(collision_angle + math.pi / 2)
        new_y_speed1 = (v1 * math.cos(angle1 - collision_angle) * (0) + 2 * v2 * math.cos(angle2 - collision_angle)) / (2) * math.sin(collision_angle) + v1 * math.sin(angle1 - collision_angle) * math.sin(collision_angle + math.pi / 2)
        new_x_speed2 = (v2 * math.cos(angle2 - collision_angle) * (0) + 2 * v1 * math.cos(angle1 - collision_angle)) / (2) * math.cos(collision_angle) + v2 * math.sin(angle2 - collision_angle) * math.sin(collision_angle + math.pi / 2)
        new_y_speed2 = (v2 * math.cos(angle2 - collision_angle) * (0) + 2 * v1 * math.cos(angle1 - collision_angle)) / (2) * math.sin(collision_angle) + v2 * math.sin(angle2 - collision_angle) * math.sin(collision_angle + math.pi / 2)

        # Set the new speeds.
        self.x_speed = new_x_speed1
        self.y_speed = new_y_speed1
        other_sprite.x_speed = new_x_speed2
        other_sprite.y_speed = new_y_speed2

        # Rescale the velocities to ensure the speeds are the same as before the collision.
        self_new_speed = math.sqrt(self.x_speed**2 + self.y_speed**2)
        other_new_speed = math.sqrt(other_sprite.x_speed**2 + other_sprite.y_speed**2)

        if self_new_speed != 0:
            self.x_speed = self.x_speed * v1 / self_new_speed
            self.y_speed = self.y_speed * v1 / self_new_speed

        if other_new_speed != 0:
            other_sprite.x_speed = other_sprite.x_speed * v2 / other_new_speed
            other_sprite.y_speed = other_sprite.y_speed * v2 / other_new_speed

        # Update the angles.
        self.angle_radians = math.atan2(self.y_speed, self.x_speed)
        other_sprite.angle_radians = math.atan2(other_sprite.y_speed, other_sprite.x_speed)

        # Move the sprite out of the wall
        self.move_apart(other_sprite)

    def move_apart(self, other_sprite):
        """Move sprite out of wall after collision."""
        overlap = pygame.Rect.clip(self.rect, other_sprite.rect)
        if overlap.width > 0 and overlap.height > 0:
            if overlap.width > overlap.height:
                if self.rect.centery < other_sprite.rect.centery:
                    self.rect.y -= overlap.height + 1  # Add 1 to ensure separation
                    other_sprite.rect.y += overlap.height + 1 # Move other sprite as well
                else:
                    self.rect.y += overlap.height + 1
                    other_sprite.rect.y -= overlap.height + 1 # Move other sprite as well
            else:
                if self.rect.centerx < other_sprite.rect.centerx:
                    self.rect.x -= overlap.width + 1
                    other_sprite.rect.x += overlap.width + 1 # Move other sprite
                else:
                    self.rect.x += overlap.width + 1
                    other_sprite.rect.x -= overlap.width + 1 # Move other sprite

    def draw(self, surface):
        """Draw the sprite."""
        surface.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    """
    A static wall sprite.
    """
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        """Wall does not need to be updated."""
        pass


def main():
    """Main function to run the example."""
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Bouncing Sprites with Walls")
    clock = pygame.time.Clock()

    # Create moving sprites
    num_sprites = 5
    all_sprites = pygame.sprite.Group()
    size = 40 # All sprites are the same size now.
    for i in range(num_sprites):
        sprite_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(sprite_image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (0, 0, size, size))
        x = random.randint(size, screen_width - size)
        y = random.randint(size, screen_height - size)
        speed = 5
        angle = random.randint(0, 360)
        moving_sprite = MovingSprite(x, y, sprite_image, speed, angle, size)
        all_sprites.add(moving_sprite)

    # Create wall sprites
    wall_color = (255, 255, 255)  # White
    wall1 = Wall(200, 200, 100, 20, wall_color)  # Horizontal wall
    wall2 = Wall(400, 300, 20, 150, wall_color)  # Vertical wall
    wall_group = pygame.sprite.Group(wall1, wall2)  # Add walls to a group

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Update moving sprites (pass the wall group AND the moving sprite group)
        for sprite in all_sprites:
            sprite.update(screen_width, screen_height, wall_group, all_sprites)
        wall_group.update() #update the walls.

        # Draw all sprites
        all_sprites.draw(screen)
        wall_group.draw(screen)  # Draw the walls

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
