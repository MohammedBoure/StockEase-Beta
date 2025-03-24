import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Chaos")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

PLAYER_SIZE = 40
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT // 2 - PLAYER_SIZE // 2
player_speed = 6
player_lives = 3

ENEMY_SIZE = 30
ENEMY_SPEED_BASE = 3
ENEMY_SPAWN_RATE = 20
enemies = []

PARTICLE_COUNT = 20
particles = []

font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)

clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.color = (random.randint(100, 255), random.randint(0, 100), 0)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 30

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(1, self.size - 0.2)

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Enemy:
    def __init__(self):
        self.size = ENEMY_SIZE
        self.speed = ENEMY_SPEED_BASE + random.uniform(0, 2)
        direction = random.randint(0, 3)
        if direction == 0:  # Top
            self.x = random.randint(0, WIDTH - self.size)
            self.y = -self.size
            self.dx = random.uniform(-0.5, 0.5)
            self.dy = self.speed
        elif direction == 1:  # Bottom
            self.x = random.randint(0, WIDTH - self.size)
            self.y = HEIGHT
            self.dx = random.uniform(-0.5, 0.5)
            self.dy = -self.speed
        elif direction == 2:  # Left
            self.x = -self.size
            self.y = random.randint(0, HEIGHT - self.size)
            self.dx = self.speed
            self.dy = random.uniform(-0.5, 0.5)
        else:  # Right
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT - self.size)
            self.dx = -self.speed
            self.dy = random.uniform(-0.5, 0.5)

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (int(self.x), int(self.y), self.size, self.size))

    def off_screen(self):
        return (self.x < -self.size or self.x > WIDTH or 
                self.y < -self.size or self.y > HEIGHT)

    def collides_with(self, px, py, psize):
        return (px < self.x + self.size and px + psize > self.x and
                py < self.y + self.size and py + psize > self.y)

def main():
    global player_x, player_y, enemies, particles, player_lives, ENEMY_SPAWN_RATE  # Added ENEMY_SPAWN_RATE
    running = True
    score = 0
    spawn_counter = 0
    game_over = False

    while running:
        if not game_over:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and game_over:
                    if event.key == pygame.K_r:
                        player_x = WIDTH // 2 - PLAYER_SIZE // 2
                        player_y = HEIGHT // 2 - PLAYER_SIZE // 2
                        player_lives = 3
                        enemies = []
                        particles = []
                        score = 0
                        spawn_counter = 0
                        game_over = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < HEIGHT - PLAYER_SIZE:
                player_y += player_speed

            spawn_counter += 1
            if spawn_counter >= ENEMY_SPAWN_RATE:
                enemies.append(Enemy())
                spawn_counter = 0
                if score % 10 == 0 and score > 0:
                    ENEMY_SPAWN_RATE = max(5, ENEMY_SPAWN_RATE - 1)

            for enemy in enemies[:]:
                enemy.update()
                if enemy.off_screen():
                    enemies.remove(enemy)
                    score += 1
                elif enemy.collides_with(player_x, player_y, PLAYER_SIZE):
                    for _ in range(PARTICLE_COUNT):
                        particles.append(Particle(player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2))
                    enemies.remove(enemy)
                    player_lives -= 1
                    if player_lives <= 0:
                        game_over = True
                else:
                    enemy.draw(screen)

            for particle in particles[:]:
                particle.update()
                particle.draw(screen)
                if particle.life <= 0:
                    particles.remove(particle)

            pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {player_lives}", True, GREEN if player_lives > 1 else RED)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 40))

        else:
            screen.fill(BLACK)
            game_over_text = large_font.render(f"Game Over! Score: {score}", True, WHITE)
            restart_text = font.render("Press R to Restart", True, YELLOW)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()