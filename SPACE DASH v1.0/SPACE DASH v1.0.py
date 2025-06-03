
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.thrust = 0.5
        self.max_speed = 8
        self.angle = 0
        self.fuel = 100
        self.max_fuel = 100

    def update(self, keys):
        # Handle input
        if keys[pygame.K_UP] and self.fuel > 0:
            self.vel_y -= self.thrust
            self.fuel -= 0.2
        if keys[pygame.K_DOWN]:
            self.vel_y += self.thrust * 0.5
        if keys[pygame.K_LEFT]:
            self.vel_x -= self.thrust * 0.7
        if keys[pygame.K_RIGHT]:
            self.vel_x += self.thrust * 0.7

        # Apply drag
        self.vel_x *= 0.95
        self.vel_y *= 0.95

        # Limit speed
        if abs(self.vel_x) > self.max_speed:
            self.vel_x = self.max_speed if self.vel_x > 0 else -self.max_speed
        if abs(self.vel_y) > self.max_speed:
            self.vel_y = self.max_speed if self.vel_y > 0 else -self.max_speed

        # Update position
        self.x += self.vel_x
        self.y += self.vel_y

        # Keep rocket on screen
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.vel_x = 0
        if self.y < 0:
            self.y = 0
            self.vel_y = 0
        elif self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.vel_y = 0

        # Calculate angle based on velocity
        if self.vel_x != 0 or self.vel_y != 0:
            self.angle = math.atan2(self.vel_y, self.vel_x) * 180 / math.pi + 90

    def draw(self, screen):
        # Draw rocket body
        rocket_points = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width - 5, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height - 10),
            (self.x + 5, self.y + self.height)
        ]
        pygame.draw.polygon(screen, WHITE, rocket_points)

        # Draw rocket details
        pygame.draw.circle(screen, RED, (int(self.x + self.width // 2), int(self.y + 15)), 8)
        pygame.draw.rect(screen, BLUE, (self.x + 10, self.y + 25, self.width - 20, 20))

        # Draw thrust flames when moving up
        if pygame.key.get_pressed()[pygame.K_UP] and self.fuel > 0:
            flame_points = [
                (self.x + 8, self.y + self.height),
                (self.x + self.width // 2, self.y + self.height + 15),
                (self.x + self.width - 8, self.y + self.height)
            ]
            pygame.draw.polygon(screen, ORANGE, flame_points)
            # Inner flame
            inner_flame_points = [
                (self.x + 12, self.y + self.height),
                (self.x + self.width // 2, self.y + self.height + 8),
                (self.x + self.width - 12, self.y + self.height)
            ]
            pygame.draw.polygon(screen, YELLOW, inner_flame_points)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, ORANGE, (self.x + 5, self.y + 5, self.width - 10, self.height - 10))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class FuelPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 2
        self.bob_offset = 0

    def update(self):
        self.x -= self.speed
        self.bob_offset += 0.2

    def draw(self, screen):
        bob_y = self.y + math.sin(self.bob_offset) * 3
        pygame.draw.circle(screen, GREEN, (int(self.x + self.width // 2), int(bob_y + self.height // 2)), self.width // 2)
        pygame.draw.circle(screen, WHITE, (int(self.x + self.width // 2), int(bob_y + self.height // 2)), self.width // 2 - 3)
        pygame.draw.circle(screen, GREEN, (int(self.x + self.width // 2), int(bob_y + self.height // 2)), 4)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2)
        self.brightness = random.randint(100, 255)

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT)

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Rocket Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.rocket = Rocket(100, SCREEN_HEIGHT // 2)
        self.obstacles = []
        self.fuel_pickups = []
        self.stars = [Star() for _ in range(100)]

        self.score = 0
        self.lives = 3
        self.game_over = False
        self.obstacle_timer = 0
        self.fuel_timer = 0

    def spawn_obstacle(self):
        height = random.randint(50, 150)
        y = random.randint(0, SCREEN_HEIGHT - height)
        speed = random.uniform(3, 6)
        self.obstacles.append(Obstacle(SCREEN_WIDTH, y, 30, height, speed))

    def spawn_fuel(self):
        y = random.randint(50, SCREEN_HEIGHT - 50)
        self.fuel_pickups.append(FuelPickup(SCREEN_WIDTH, y))

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.rocket.update(keys)

        # Update stars
        for star in self.stars:
            star.update()

        # Spawn obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer > 90:  # Spawn every 1.5 seconds at 60 FPS
            self.spawn_obstacle()
            self.obstacle_timer = 0

        # Spawn fuel
        self.fuel_timer += 1
        if self.fuel_timer > 300:  # Spawn every 5 seconds
            self.spawn_fuel()
            self.fuel_timer = 0

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.x < -obstacle.width:
                self.obstacles.remove(obstacle)
                self.score += 10
            elif obstacle.get_rect().colliderect(self.rocket.get_rect()):
                self.obstacles.remove(obstacle)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True

        # Update fuel pickups
        for fuel in self.fuel_pickups[:]:
            fuel.update()
            if fuel.x < -fuel.width:
                self.fuel_pickups.remove(fuel)
            elif fuel.get_rect().colliderect(self.rocket.get_rect()):
                self.fuel_pickups.remove(fuel)
                self.rocket.fuel = min(self.rocket.max_fuel, self.rocket.fuel + 30)
                self.score += 5

        # Check if out of fuel and falling
        if self.rocket.fuel <= 0 and self.rocket.y >= SCREEN_HEIGHT - self.rocket.height:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.rocket.fuel = 50  # Give some fuel back

        # Increase score over time
        self.score += 1

    def draw(self):
        self.screen.fill(BLACK)

        # Draw stars
        for star in self.stars:
            star.draw(self.screen)

        # Draw game objects
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for fuel in self.fuel_pickups:
            fuel.draw(self.screen)
        self.rocket.draw(self.screen)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        fuel_text = self.font.render(f"Fuel: {int(self.rocket.fuel)}", True, GREEN if self.rocket.fuel > 20 else RED)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(fuel_text, (10, 50))
        self.screen.blit(lives_text, (10, 90))

        # Draw fuel bar
        fuel_bar_width = 200
        fuel_bar_height = 20
        fuel_percentage = self.rocket.fuel / self.rocket.max_fuel
        pygame.draw.rect(self.screen, WHITE, (10, 130, fuel_bar_width, fuel_bar_height), 2)
        pygame.draw.rect(self.screen, GREEN if self.rocket.fuel > 20 else RED,
                        (12, 132, int((fuel_bar_width - 4) * fuel_percentage), fuel_bar_height - 4))

        # Draw instructions
        instructions = [
            "Arrow Keys: Move",
            "UP: Thrust (uses fuel)",
            "Avoid red obstacles",
            "Collect green fuel"
        ]
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, GRAY)
            self.screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 25))

        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("GAME OVER", True, RED)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to restart or Q to quit", True, WHITE)

            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(final_score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def restart(self):
        self.rocket = Rocket(100, SCREEN_HEIGHT // 2)
        self.obstacles = []
        self.fuel_pickups = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.obstacle_timer = 0
        self.fuel_timer = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart()
                    elif event.key == pygame.K_q and self.game_over:
                        running = False

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
