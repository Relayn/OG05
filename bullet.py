import pygame
import math

class Bullet:
    WIDTH, HEIGHT = 5, 5
    COLOR = (0, 0, 255)
    SPEED = 10

    def __init__(self, start_x, start_y, end_pos):
        self.image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect(center=(start_x, start_y))  # Center of the player
        self.angle = math.atan2(end_pos[1] - start_y, end_pos[0] - start_x)

    def update(self):
        self.rect.x += self.SPEED * math.cos(self.angle)
        self.rect.y += self.SPEED * math.sin(self.angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect)