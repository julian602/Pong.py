import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1900, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 50
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
SPEED_INCREMENT = 2
MAX_INSULTS = 25  # Maximum number of insults allowed on the screen

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chaotic Pong')

# Clock to control frame rate
clock = pygame.time.Clock()

# Paddles and ball
player1 = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Scoring
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

# Insults for each player
player1_insults = []
player2_insults = []

# Track consecutive scores
player1_streak = 0
player2_streak = 0

# List of 100 random insults
insults = [
    "You suck", "Your ass", "Garbage", "Pathetic", "Noob", "Amateur", "Just quit", "You're hopeless", "Loser", "Weak",
    "Clown", "So bad", "Get rekt", "GG no re", "Trash", "Uninstall", "Try harder", "You call this playing?",
    "I’ve seen better", "Do you even game?", "Disaster", "Epic fail", "Just stop", "Worse than I thought",
    "Why do you even try?", "Sad", "Not even close", "Go home", "Waste of time", "Useless", "Embarrassing",
    "You're a joke", "Terrible", "Can't even", "Wow, really?", "Is that it?", "Is this your best?", "You're finished",
    "Walk away", "Quitter", "So lame", "I've seen toddlers play better", "Worst player ever", "Just give up",
    "You're a mess", "Unbelievable", "Nice try (not)", "LOL", "ROFL", "Please stop", "Game over for you", "Zero skill",
    "Your skill level is negative", "Rage quit incoming", "Just throw in the towel", "Is this even real?",
    "I’m embarrassed for you", "Totally cringe", "Epic defeat", "Time to retire", "Not even in the same league",
    "Go back to training", "You got lucky last time", "The worst", "Absolutely nothing", "Utter failure", "Do better",
    "Beyond redemption", "Zero potential", "Out of your league", "You're like a bot", "You’re a glitch in the system",
    "Keep crying", "Can't touch this", "Burnt out?", "Noob move", "That's cute", "Give it up already", "Wipeout",
    "Just delete the game", "You're lagging in skill", "No competition", "Rusty player detected", "Outclassed",
    "Way out of your depth", "Can’t handle this", "Joke of a player", "Clearly rusty", "Your defeat is inevitable",
    "Best to leave now", "Take the L", "Just no", "Too slow", "Forever stuck at this level", "You peaked early",
    "Doesn't get worse", "So outplayed", "Completely clueless", "Move along", "GG", "It’s painful to watch you",
    "Not even close to good", "Disappointment", "RIP your skill"
]

def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, player1_score, player2_score
    global player1_streak, player2_streak

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

    # Ball collision with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        BALL_SPEED_X = -BALL_SPEED_X

    # Scoring when the ball goes off the screen
    if ball.left <= 0:
        player2_score += 1
        player2_streak += 1
        player1_streak = 0
        insult_player(1)
        if player2_streak == 3:
            player1_insults.append(("Three in a row, just give up now", random_position(1), random_font_size()))
        if player2_score == 10:
            player1_insults.append(("Stay Sigma", random_position(1), random_font_size()))
        reset_ball()

    if ball.right >= WIDTH:
        player1_score += 1
        player1_streak += 1
        player2_streak = 0
        insult_player(2)
        if player1_streak == 3:
            player2_insults.append(("Three in a row, just give up now", random_position(2), random_font_size()))
        if player1_score == 10:
            player2_insults.append(("Stay Sigma", random_position(2), random_font_size()))
        reset_ball()

def random_position(player):
    if player == 1:
        return (random.randint(0, WIDTH // 2 - 300), random.randint(0, HEIGHT - 100))
    elif player == 2:
        return (random.randint(WIDTH // 2, WIDTH - 300), random.randint(0, HEIGHT - 100))

def random_font_size():
    return random.randint(30, 100)

def move_paddles():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED

def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    # Reset ball position
    ball.center = (WIDTH // 2, HEIGHT // 2)
    
    # Reverse ball direction after scoring
    BALL_SPEED_X *= -1

def insult_player(player):
    insults_to_add = random.sample(insults, 5)  # Pick 5 random insults
    for insult in insults_to_add:
        if player == 1:
            player1_insults.append((insult, random_position(1), random_font_size()))
        elif player == 2:
            player2_insults.append((insult, random_position(2), random_font_size()))

    # Check if number of insults exceeds the limit and reset
    if len(player1_insults) + len(player2_insults) >= MAX_INSULTS:
        player1_insults.clear()
        player2_insults.clear()

def draw_ball():
    pygame.draw.ellipse(screen, WHITE, ball)

def draw_scores():
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (WIDTH // 4, 50))
    screen.blit(player2_text, (3 * WIDTH // 4, 50))

def draw_midline():
    pygame.draw.line(screen, RED, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

def draw_insults():
    # Draw insults for player 1 (left side)
    for insult, position, font_size in player1_insults:
        insult_surface = pygame.font.Font(None, font_size).render(insult, True, RED)
        screen.blit(insult_surface, position)

    # Draw insults for player 2 (right side)
    for insult, position, font_size in player2_insults:
        insult_surface = pygame.font.Font(None, font_size).render(insult, True, RED)
        screen.blit(insult_surface, position)

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move_paddles()
        move_ball()

        # Drawing
        screen.fill(BLACK)
        draw_midline()  # Draw the middle line
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        draw_ball()  # Draw the ball

        # Draw the scores
        draw_scores()

        # Draw the insults
        draw_insults()

        pygame.display.flip()
        clock.tick(120)  # 120 frames per second

if __name__ == "__main__":
    game_loop()

