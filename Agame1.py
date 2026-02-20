# A simple, playable Flappy Bird game!

import pygame
import random
import sys

# --- Pygame Setup ---
# Initialize Pygame and set up the window.
pygame.init()
screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# --- Game Variables and Constants ---
# Bird properties
bird_width = 50
bird_height = 40
bird_x = 100
bird_y = screen_height // 2
bird_movement = 0
gravity = 0.25
flap_strength = -6

# Pipe properties
pipe_width = 80
pipe_gap = 250
pipe_speed = 3
# The pipe_list will now store a list for each pipe,
# containing the top rect, bottom rect, and a passed_bird flag.
pipe_list = []
pipe_spawn_event = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn_event, 1200) # Spawn a new pipe every 1.2 seconds

# Game state
score = 0
high_score = 0
game_active = True
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 50)

# Colors
bg_color = (135, 206, 235)  # Sky blue
bird_color = (255, 255, 0)  # Yellow
pipe_color = (0, 128, 0)    # Green
score_color = (255, 255, 255) # White
floor_color = (222, 184, 135) # Burlywood
button_color = (255, 100, 0) # Orange for the button

# Create the bird
bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

# --- Functions ---
def draw_floor():
    # Draw a solid rectangle for the floor
    pygame.draw.rect(screen, floor_color, (0, 900, screen_width, 124))

def create_pipe():
    # Create a new pair of pipes with a random height
    random_pipe_height = random.choice([400, 500, 600])
    top_rect = pygame.Rect(screen_width, 0, pipe_width, random_pipe_height - pipe_gap)
    bottom_rect = pygame.Rect(screen_width, random_pipe_height + pipe_gap, pipe_width, screen_height - (random_pipe_height + pipe_gap))
    
    # Return a list containing both pipes and a flag
    return [top_rect, bottom_rect, False]

def move_pipes(pipes):
    # Move all pipes to the left
    for pipe_set in pipes:
        pipe_set[0].centerx -= pipe_speed
        pipe_set[1].centerx -= pipe_speed
    return pipes

def draw_pipes(pipes):
    # Draw all the pipes on the screen
    for pipe_set in pipes:
        pygame.draw.rect(screen, pipe_color, pipe_set[0])
        pygame.draw.rect(screen, pipe_color, pipe_set[1])

def check_collision(pipes):
    # Check for collisions with the pipes or the ground/ceiling
    for pipe_set in pipes:
        if bird_rect.colliderect(pipe_set[0]) or bird_rect.colliderect(pipe_set[1]):
            return False # Game over
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False # Game over
    
    return True # Game continues

def display_score(game_state):
    # Display the score on the screen
    global high_score
    if game_state == 'main_game':
        score_surface = font.render(str(int(score)), True, score_color)
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over':
        # current score
        score_surface = font.render(f'Score: {int(score)}', True, score_color)
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)
        
        # Display high score
        high_score_surface = font.render(f'High Score: {int(high_score)}', True, score_color)
        high_score_rect = high_score_surface.get_rect(center=(screen_width // 2, 850))
        screen.blit(high_score_surface, high_score_rect)
        
        # Display "Game Over!"
        game_over_surface = font.render("Game Over!", True, score_color)
        game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, 400))
        screen.blit(game_over_surface, game_over_rect)

        #restart button
        restart_text_surface = button_font.render("Restart", True, score_color)
        restart_text_rect = restart_text_surface.get_rect(center=(screen_width // 2, 550))
        
        button_rect = restart_text_rect.inflate(40, 20)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        screen.blit(restart_text_surface, restart_text_rect)
        
        return button_rect

def update_score():
    global score, high_score
    high_score = max(high_score, score)

def reset_game():
    global bird_y, bird_movement, pipe_list, game_active, score
    bird_y = screen_height // 2
    bird_movement = 0
    pipe_list.clear()
    game_active = True
    score = 0

# --- Main Game Loop ---
while True:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = flap_strength
            if event.key == pygame.K_SPACE and not game_active:
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            if restart_button_rect.collidepoint(event.pos):
                reset_game()

        if event.type == pipe_spawn_event:
            if game_active:
                pipe_list.append(create_pipe())

    # --- Game Logic (only runs if game is active) ---
    if game_active:
        # Bird gravity and movement
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # Pipe movement
        pipe_list = move_pipes(pipe_list)

        # Collision check
        game_active = check_collision(pipe_list)

        # Update score
        for pipe_set in pipe_list:
            if pipe_set[0].right < bird_rect.left and not pipe_set[2]:
                score += 1
                pipe_set[2] = True
                
    # --- Drawing elements to the screen ---
    screen.fill(bg_color)
    
    if game_active:
        pygame.draw.rect(screen, bird_color, bird_rect)
        draw_pipes(pipe_list)
        display_score('main_game')
    else:
        update_score()
        restart_button_rect = display_score('game_over')
    
    draw_floor()

    pygame.display.update()
    clock.tick(120)

