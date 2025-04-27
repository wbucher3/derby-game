import pygame
import random
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horse Collision Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)

# Dummy surface for horses and map (you can replace with real images)
def create_circle_surface(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return surf

# Horse Sprite
class Horse(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = create_circle_surface(20, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        angle = random.uniform(0, 360)
        self.velocity = pygame.math.Vector2(3, 0).rotate(angle)

    def update(self):
        self.rect.centerx += int(self.velocity.x)
        self.rect.centery += int(self.velocity.y)

        # Bounce off screen edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity.y *= -1

    def bounce(self, normal):
        self.velocity = self.velocity.reflect(normal)

# Map (just a green area with a circular mask in the center)
class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, GREEN, (WIDTH//2, HEIGHT//2), 100)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_threshold(self.image, GREEN, (1, 1, 1, 255))

# Create game objects
map_sprite = Map()
horses = pygame.sprite.Group(
    Horse(100, 100, (255, 0, 0)),
    Horse(700, 500, (0, 0, 255)),
    Horse(500, 700, (0, 100, 255)),
    Horse(200, 200, (100, 0, 255)),
    Horse(50, 50, (0, 30, 255))
)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    horses.update()

    # Collision between horses
    horse_list = list(horses)
    for i in range(len(horse_list)):
        for j in range(i + 1, len(horse_list)):
            h1, h2 = horse_list[i], horse_list[j]
            if pygame.sprite.collide_mask(h1, h2):
                delta = pygame.math.Vector2(h1.rect.center) - pygame.math.Vector2(h2.rect.center)
                if delta.length_squared() > 0:
                    normal = delta.normalize()
                    h1.bounce(normal)
                    h2.bounce(-normal)

    # Collision with map mask
    for horse in horses:
        offset = (horse.rect.left - map_sprite.rect.left, horse.rect.top - map_sprite.rect.top)
        if map_sprite.mask.overlap(horse.mask, offset):
            # Bounce away from center
            center = pygame.math.Vector2(WIDTH//2, HEIGHT//2)
            delta = pygame.math.Vector2(horse.rect.center) - center
            if delta.length_squared() > 0:
                horse.bounce(delta.normalize())

    # Draw
    screen.blit(map_sprite.image, map_sprite.rect)
    horses.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
