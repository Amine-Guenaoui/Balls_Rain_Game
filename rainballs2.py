import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Rain Clicker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
clock = pygame.time.Clock()
FPS = 60
score = 0
game_time = 30  # 30 seconds
start_time = pygame.time.get_ticks()
ball_speed = 5

# Load sound
pop_sound = pygame.mixer.Sound("pop.mp3")  # Add a "pop.wav" file to your project folder

# Ball class
class Ball:
    def __init__(self):
        self.size = random.randint(20, 50)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = ball_speed
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def clicked(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.size and
                self.y <= mouse_pos[1] <= self.y + self.size)

# Arrow class (to highlight mouse)
class Arrow:
    def __init__(self):
        self.color = GREEN
        self.last_click_time = 0

    def draw(self, mouse_pos):
        # Draw a small arrow at the mouse position
        x, y = mouse_pos
        pygame.draw.polygon(screen, self.color, [(x, y), (x - 10, y + 20), (x + 10, y + 20)])

    def change_color(self):
        self.color = YELLOW
        self.last_click_time = pygame.time.get_ticks()

    def reset_color(self):
        if pygame.time.get_ticks() - self.last_click_time > 200:  # Reset color after 200ms
            self.color = GREEN

# Create a list to hold the balls
balls = []

# Create an arrow object
arrow = Arrow()

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for ball in balls:
                if ball.clicked(mouse_pos):
                    balls.remove(ball)
                    score += 10  # Increase score for clicking a ball
                    pop_sound.play()  # Play pop sound
                    arrow.change_color()  # Change arrow color
                    break

    # Spawn new balls randomly
    if random.randint(1, 20) == 1:
        balls.append(Ball())

    # Move and draw balls
    for ball in balls:
        ball.move()
        ball.draw()

    # Remove balls that go off-screen
    balls = [ball for ball in balls if ball.y < HEIGHT]

    # Increase ball speed over time
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
    if elapsed_time < game_time:
        ball_speed = 5 + (elapsed_time // 5) * 2  # Increase speed every 5 seconds
    else:
        running = False  # End the game after 30 seconds

    # Draw the arrow at the mouse position
    mouse_pos = pygame.mouse.get_pos()
    arrow.draw(mouse_pos)
    arrow.reset_color()  # Reset arrow color if needed

    # Display score and timer
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Time: {int(game_time - elapsed_time)}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (WIDTH - 150, 10))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Game over screen
screen.fill(BLACK)
font = pygame.font.SysFont("Arial", 50)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 25))
pygame.display.flip()

# Wait for a few seconds before closing
pygame.time.wait(3000)

# Quit PyGame
pygame.quit()
sys.exit()