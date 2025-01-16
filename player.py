import pygame

class Player:
    WIDTH, HEIGHT = 50, 50
    COLOR = (0, 255, 0)

    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)