import pygame
import random

class Target:
    WIDTH, HEIGHT = 30, 30
    COLOR = (255, 0, 0)
    SPEED = 2

    def __init__(self, width, height):
        self.image = pygame.image.load("assets/target.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect(topleft=(random.randint(0, width - self.WIDTH), 0))

    def update(self):
        self.rect.y += self.SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)