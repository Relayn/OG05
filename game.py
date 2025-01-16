import pygame
from player import Player
from target import Target
from bullet import Bullet

class Game:
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    TARGET_SPAWN_INTERVAL = 1000  # milliseconds

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Shooting Game")
        self.clock = pygame.time.Clock()
        self.player = Player(self.WIDTH // 2, self.HEIGHT - 50)
        self.targets = []
        self.bullets = []
        self.last_target_spawn_time = pygame.time.get_ticks()

        # Загрузка звуков
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
        self.hit_sound = pygame.mixer.Sound("sounds/hit.wav")
        self.miss_sound = pygame.mixer.Sound("sounds/miss.wav")

        # Счётчик очков и жизней
        self.score = 0
        self.lives = 3

        # Шрифт для отображения текста
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.shoot(event.pos)

            self.spawn_target()
            self.update_objects()
            self.check_collisions()
            self.draw()

            self.clock.tick(self.FPS)

    def shoot(self, mouse_pos):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.top, mouse_pos)
        self.bullets.append(bullet)
        self.shoot_sound.play()

    def spawn_target(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_target_spawn_time > self.TARGET_SPAWN_INTERVAL:
            target = Target(self.WIDTH, self.HEIGHT)
            self.targets.append(target)
            self.last_target_spawn_time = current_time

    def update_objects(self):
        self.player.update()
        for target in self.targets:
            target.update()
        for bullet in self.bullets:
            bullet.update()

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for target in self.targets[:]:
                if bullet.rect.colliderect(target.rect):
                    self.bullets.remove(bullet)
                    self.targets.remove(target)
                    self.score += 10
                    self.hit_sound.play()
                    break
            else:
                if bullet.rect.bottom < 0:
                    self.bullets.remove(bullet)
                    self.miss_sound.play()

        for target in self.targets[:]:
            if target.rect.colliderect(self.player.rect):
                self.targets.remove(target)
                self.lives -= 1
                self.miss_sound.play()
                if self.lives <= 0:
                    self.game_over()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for target in self.targets:
            target.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Отрисовка очков и жизней
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (self.WIDTH - 100, 10))

        pygame.display.flip()

    def game_over(self):
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(game_over_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.targets = []
        self.bullets = []