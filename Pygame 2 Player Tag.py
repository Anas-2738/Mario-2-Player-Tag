import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 800
PLAYER_SIZE = 35
FPS = 60
WHITE = (255, 255, 255)
PLATFORM_COLOR = (100, 100, 100)
GRAVITY = 1
JUMP_HEIGHT = 20
INVINCIBILITY_DURATION = 2
GAME_DURATION = 60
OUTLINE_COLOR = (255, 255, 0)

# Ice power variables
Mario_ice_power_enabled = False
Luigi_ice_power_enabled = False

# Ice power constants
ICE_POWER_DURATION = 8  # Duration of ice power in seconds
ICE_POWER_FLOWER_SIZE = 30
FREEZE_DURATION = 1.5  # Duration of freeze effect in seconds
ICE_FLOWER_SPAWN_INTERVAL = 15  # seconds

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2-Player Tag Game")

# Load background image and scale it
background_image = pygame.transform.scale(pygame.image.load("Miscellaneous_Images\snow.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player images and resize them
Mario_standing_image = pygame.transform.scale(pygame.image.load("Mario_Images\Mario.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
Luigi_standing_image = pygame.transform.scale(pygame.image.load("Luigi_Images\Luigi.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))

# Load walking animations
Mario_walk_frames = [pygame.transform.scale(pygame.image.load(f"Mario_Images\mario_walk_{i}.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(1, 8)]
Luigi_walk_frames = [pygame.transform.scale(pygame.image.load(f"Luigi_Images\luigi_walk_{i}.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(1, 8)]

# Load jumping images
Mario_jump_image = pygame.transform.scale(pygame.image.load("Mario_Images\mario_jump.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
Luigi_jump_image = pygame.transform.scale(pygame.image.load("Luigi_Images\luigi_jump.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))

# Load jumping images for ice power players
Mario_jump_ice_power_image = pygame.transform.scale(pygame.image.load("Mario_Images\mario_jump_ice_power.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
Luigi_jump_ice_power_image = pygame.transform.scale(pygame.image.load("Luigi_Images\luigi_jump_ice_power.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))

# Load ice power images
Mario_ice_power_standing = pygame.transform.scale(pygame.image.load("Mario_Images\mario_ice_power.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
Mario_ice_power_walk_frames = [pygame.transform.scale(pygame.image.load(f"Mario_Images\mario_ice_power_walk_{i}.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(1, 7)]

Luigi_ice_power_standing = pygame.transform.scale(pygame.image.load("Luigi_Images\luigi_ice_power.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))
Luigi_ice_power_walk_frames = [pygame.transform.scale(pygame.image.load(f"Luigi_Images\luigi_ice_power_walk_{i}.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(1, 7)]

# Load ice flower image
ice_flower_image = pygame.transform.scale(pygame.image.load("Miscellaneous_Images\ice_flower.png").convert_alpha(), (ICE_POWER_FLOWER_SIZE, ICE_POWER_FLOWER_SIZE))

# Load ice power animation frames
ice_power_animation_frames = [pygame.transform.scale(pygame.image.load(f"Miscellaneous_Images\ice_power_anim_{i}.png").convert_alpha(), (ICE_POWER_FLOWER_SIZE, ICE_POWER_FLOWER_SIZE)) for i in range(1, 5)]

# Create players
Mario = pygame.Rect(50, SCREEN_HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
Luigi = pygame.Rect(SCREEN_WIDTH - 50 - PLAYER_SIZE, SCREEN_HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)

# Create platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
    pygame.Rect(0.5 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 110, 300, 20),
    pygame.Rect(2.75 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 110, 300, 20),
    pygame.Rect(1.75 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 200, 180, 20),
    pygame.Rect(0.75 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 300, 300, 20),
    pygame.Rect(4 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 300, 100, 20),
    pygame.Rect(1.5 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 420, 500, 20),
    pygame.Rect(3 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 550, 200, 20),
    pygame.Rect(1 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT - 550, 200, 20),
]

# Game variables
on_ground1, Mario_velocity_y = False, 0
on_ground2, Luigi_velocity_y = False, 0

#Starting tagged player should be random
tagged_player = random.choice([Mario, Luigi])
tag_timer = INVINCIBILITY_DURATION * FPS
game_timer = GAME_DURATION * FPS

# Ice power variables
ice_power_flower_rect = pygame.Rect(platforms[0].x + random.randint(0, platforms[0].width - ICE_POWER_FLOWER_SIZE), platforms[0].y - ICE_POWER_FLOWER_SIZE, ICE_POWER_FLOWER_SIZE, ICE_POWER_FLOWER_SIZE)

# Ice power freezing variables for Player 1
freeze_timer1 = 0
freeze_duration1 = FREEZE_DURATION * FPS

# Ice power freezing variables for Player 2
freeze_timer2 = 0
freeze_duration2 = FREEZE_DURATION * FPS

# Create a surface for drawing
draw_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

is_moving_left1 = False
is_moving_left2 = False

# Ice power shooting variables
ice_power_shooting1 = False
ice_power_bullets1 = []
bullet_timer1 = 0
bullet_speed = 10

ice_power_shooting2 = False
ice_power_bullets2 = []
bullet_timer2 = 0

# Game loop
clock = pygame.time.Clock()
game_over = False

frame_index1 = 0  # Index to keep track of the current frame for Player 1
frame_index2 = 0  # Index to keep track of the current frame for Player 2

def spawn_ice_flower():
    global ice_power_flower_rect
    platform = random.choice(platforms)
    ice_power_flower_rect.x = platform.x + random.randint(0, platform.width - ICE_POWER_FLOWER_SIZE)
    ice_power_flower_rect.y = platform.y - ICE_POWER_FLOWER_SIZE

last_flower_spawn_time = time.time()

def handle_ice_power(player, keys, ice_power_walk_frames, frame_index, is_moving_left):
    if keys[pygame.K_DOWN]:
        frame_index = (frame_index + 1) % len(ice_power_walk_frames)
        if frame_index < len(ice_power_walk_frames):
            if is_moving_left:
                draw_surface.blit(pygame.transform.flip(ice_power_walk_frames[frame_index], True, False), (player.x, player.y))
            else:
                draw_surface.blit(ice_power_walk_frames[frame_index], (player.x, player.y))

    # Check for collisions with platforms
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform):
            on_ground = True
            player.y = platform.y - PLAYER_SIZE

    # Draw walking animations
    if keys[pygame.K_LEFT]:
        frame_index = (frame_index + 1) % len(ice_power_walk_frames)
        draw_surface.blit(pygame.transform.flip(ice_power_walk_frames[frame_index], True, False), (player.x, player.y))
        is_moving_left = True
    elif keys[pygame.K_RIGHT]:
        frame_index = (frame_index + 1) % len(ice_power_walk_frames)
        draw_surface.blit(ice_power_walk_frames[frame_index], (player.x, player.y))
        is_moving_left = False
    else:
        # If not moving, show standing frame
        if is_moving_left:
            draw_surface.blit(pygame.transform.flip(ice_power_walk_frames[0], True, False), (player.x, player.y))
        else:
            draw_surface.blit(ice_power_walk_frames[0], (player.x, player.y))

    return frame_index, is_moving_left

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # PLAYER SPEED
    player_speed = 10

    # PlaXwyer 1 controls
    if keys[pygame.K_a] and Mario.x > 0 and freeze_timer1 <= 0:
        Mario.x -= player_speed
        frame_index1 = (frame_index1 + 1) % len(Mario_walk_frames)
    if keys[pygame.K_d] and Mario.x < SCREEN_WIDTH - PLAYER_SIZE and freeze_timer1 <= 0:
        Mario.x += player_speed
        frame_index1 = (frame_index1 + 1) % len(Mario_walk_frames)

    if not on_ground1:
        Mario_velocity_y += GRAVITY
    else:
        Mario_velocity_y = 0

    Mario.y += Mario_velocity_y

    if keys[pygame.K_w] and on_ground1:
        on_ground1 = False
        Mario_velocity_y = -JUMP_HEIGHT

    # Check for collisions with platforms for player 1
    on_ground1 = False
    for platform in platforms:
        if Mario.colliderect(platform):
            on_ground1 = True
            Mario.y = platform.y - PLAYER_SIZE
            Mario_velocity_y = 0

     # Player 2 controls
    if keys[pygame.K_LEFT] and Luigi.x > 0 and freeze_timer2 <= 0:
        Luigi.x -= player_speed
        frame_index2 = (frame_index2 + 1) % len(Luigi_walk_frames)
    if keys[pygame.K_RIGHT] and Luigi.x < SCREEN_WIDTH - PLAYER_SIZE and freeze_timer2 <= 0:
        Luigi.x += player_speed
        frame_index2 = (frame_index2 + 1) % len(Luigi_walk_frames)

    if not on_ground2:
        Luigi_velocity_y += GRAVITY
    else:
        Luigi_velocity_y = 0

    Luigi.y += Luigi_velocity_y

    if keys[pygame.K_UP] and on_ground2:
        on_ground2 = False
        Luigi_velocity_y = -JUMP_HEIGHT

    # Check for collisions with platforms for player 2
    on_ground2 = False
    for platform in platforms:
        if Luigi.colliderect(platform):
            on_ground2 = True
            Luigi.y = platform.y - PLAYER_SIZE
            Luigi_velocity_y = 0

    # Check for tagging
    if tag_timer <= 0 and Mario.colliderect(Luigi):
        tagged_player = Mario if tagged_player == Luigi else Luigi
        tag_timer = INVINCIBILITY_DURATION * FPS

    # Apply invincibility
    if tag_timer > 0:
        tag_timer -= 1

      
    # Ice power mechanics for Player 1
    if Mario_ice_power_enabled:
        if pygame.time.get_ticks() - ice_power_start_time_Mario < ICE_POWER_DURATION * 1000:
            frame_index1, is_moving_left1 = handle_ice_power(Mario, keys, Mario_ice_power_walk_frames, frame_index1, is_moving_left1)
        else:
            print("Mario's ice power duration expired.")
            Mario_ice_power_enabled = False
            Mario_standing_image = pygame.transform.scale(pygame.image.load("Mario_Images\mario.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))

    # Ice power mechanics for Player 2
    if Luigi_ice_power_enabled:
        if pygame.time.get_ticks() - ice_power_start_time_Luigi < ICE_POWER_DURATION * 1000:
            frame_index2, is_moving_left2 = handle_ice_power(Luigi, keys, Luigi_ice_power_walk_frames, frame_index2, is_moving_left2)
        else:
            print("Luigi's ice power duration expired.")
            Luigi_ice_power_enabled = False
            Luigi_standing_image = pygame.transform.scale(pygame.image.load("Luigi_Images\luigi.png").convert_alpha(), (PLAYER_SIZE, PLAYER_SIZE))


    # Ice power mechanics for Player 1
    if Mario_ice_power_enabled:
        if pygame.time.get_ticks() - ice_power_start_time_Mario < ICE_POWER_DURATION * 1000:
            frame_index1, is_moving_left1 = handle_ice_power(Mario, keys, Mario_ice_power_walk_frames, frame_index1, is_moving_left1)
            # Shooting ice power bullets for Player 1
        if keys[pygame.K_s] and freeze_timer1 <= 0:
            if bullet_timer1 <= 0:
                ice_power_shooting1 = True
                bullet_timer1 = 15
                bullet_direction1 = -1 if keys[pygame.K_a] else 1
                bullet_x1 = Mario.x + PLAYER_SIZE // 2
                bullet_y1 = Mario.y + PLAYER_SIZE // 2
                ice_power_bullets1.append((bullet_x1, bullet_y1, bullet_direction1, 0))


    # Ice power mechanics for Player 2
    if Luigi_ice_power_enabled:
        if pygame.time.get_ticks() - ice_power_start_time_Luigi < ICE_POWER_DURATION * 1000:
            frame_index2, is_moving_left2 = handle_ice_power(Luigi, keys, Luigi_ice_power_walk_frames, frame_index2, is_moving_left2)
            # Shooting ice power bullets for Player 2
        if keys[pygame.K_DOWN] and freeze_timer2 <= 0:
            if bullet_timer2 <= 0:
                ice_power_shooting2 = True
                bullet_timer2 = 15
                bullet_direction2 = -1 if is_moving_left2 else 1
                bullet_x2 = Luigi.x + PLAYER_SIZE // 2
                bullet_y2 = Luigi.y + PLAYER_SIZE // 2
                ice_power_bullets2.append((bullet_x2, bullet_y2, bullet_direction2, 0))

    # Update ice power bullet positions for Player 1
    for i, bullet in enumerate(ice_power_bullets1):
        bullet_x1, bullet_y1, bullet_direction1, bullet_frame1 = bullet
        bullet_x1 += bullet_speed * bullet_direction1
        ice_power_bullets1[i] = (bullet_x1, bullet_y1, bullet_direction1, (bullet_frame1 + 1) % 4)

        # Check for collisions with Luigi_rect
        Luigi_rect = pygame.Rect(Luigi.x, Luigi.y, PLAYER_SIZE, PLAYER_SIZE)
        if Luigi_rect.colliderect(pygame.Rect(bullet_x1, bullet_y1, 5, 5)):  # Assuming bullet size is 5x5
            print("Luigi hit by ice power bullet from Mario!")
            # Apply freeze effect to player 2
            freeze_timer2 = FREEZE_DURATION * FPS
            ice_power_bullets1.pop(i)
            break

    # Update ice power bullet positions for Player 2
    for i, bullet in enumerate(ice_power_bullets2):
        bullet_x2, bullet_y2, bullet_direction2, bullet_frame2 = bullet
        bullet_x2 += bullet_speed * bullet_direction2
        ice_power_bullets2[i] = (bullet_x2, bullet_y2, bullet_direction2, (bullet_frame2 + 1) % 4)

        # Check for collisions with Mario_rect
        Mario_rect = pygame.Rect(Mario.x, Mario.y, PLAYER_SIZE, PLAYER_SIZE)
        if Mario_rect.colliderect(pygame.Rect(bullet_x2, bullet_y2, 5, 5)):  # Assuming bullet size is 5x5
            print("Mario hit by ice power bullet from Luigi!")
            # Apply freeze effect to player 1
            freeze_timer1 = FREEZE_DURATION * FPS
            ice_power_bullets2.pop(i)
            break

      # Inside the game loop
    # Ice power flower spawning logic
    current_time = time.time()
    if current_time - last_flower_spawn_time > ICE_FLOWER_SPAWN_INTERVAL:
        spawn_ice_flower()
        last_flower_spawn_time = current_time

    # Check if a player collected the ice flower
    if ice_power_flower_rect.colliderect(Mario) and not Mario_ice_power_enabled:
        print("Mario picked up ice power!")
        Mario_ice_power_enabled = True
        ice_power_start_time_Mario = pygame.time.get_ticks()
        last_flower_spawn_time = time.time()  # Reset the flower spawn timer
        ice_power_flower_rect.x = -ICE_POWER_FLOWER_SIZE  # Move the flower off-screen

    if ice_power_flower_rect.colliderect(Luigi) and not Luigi_ice_power_enabled:
        print("Luigi picked up ice power!")
        Luigi_ice_power_enabled = True
        ice_power_start_time_Luigi = pygame.time.get_ticks()
        last_flower_spawn_time = time.time()  # Reset the flower spawn timer
        ice_power_flower_rect.x = -ICE_POWER_FLOWER_SIZE  # Move the flower off-screen


    # Draw on the surface
    draw_surface.fill((0, 0, 0, 0))  # Clear the surface

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(draw_surface, PLATFORM_COLOR, platform)

    # Draw ice power flower
    draw_surface.blit(ice_flower_image, ice_power_flower_rect)

    # Draw players with outline
    pygame.draw.rect(draw_surface, OUTLINE_COLOR, tagged_player, 2)  # Outline tagged player

    # Draw ice power bullets for Player 1
    for bullet in ice_power_bullets1:
        bullet_x1, bullet_y1, _, bullet_frame1 = bullet
        draw_surface.blit(ice_power_animation_frames[bullet_frame1], (bullet_x1, bullet_y1))

    # Draw ice power bullets for Player 2
    for bullet in ice_power_bullets2:
        bullet_x2, bullet_y2, _, bullet_frame2 = bullet
        draw_surface.blit(ice_power_animation_frames[bullet_frame2], (bullet_x2, bullet_y2))
        # Draw walking animations or jumping images for player 1
    if keys[pygame.K_a]:
        if Mario_ice_power_enabled:
            draw_surface.blit(pygame.transform.flip(Mario_ice_power_walk_frames[frame_index1 % len(Mario_ice_power_walk_frames)], True, False), (Mario.x, Mario.y))
        else:
            draw_surface.blit(pygame.transform.flip(Mario_walk_frames[frame_index1], True, False), (Mario.x, Mario.y))
    elif keys[pygame.K_d]:
        if Mario_ice_power_enabled:
            draw_surface.blit(Mario_ice_power_walk_frames[frame_index1 % len(Mario_ice_power_walk_frames)], (Mario.x, Mario.y))
        else:
            draw_surface.blit(Mario_walk_frames[frame_index1], (Mario.x, Mario.y))
    elif (keys[pygame.K_w] or keys[pygame.K_s]) and not on_ground1:
        draw_surface.blit(Mario_jump_ice_power_image if Mario_ice_power_enabled else Mario_jump_image, (Mario.x, Mario.y))
    elif Mario_ice_power_enabled:
        draw_surface.blit(Mario_ice_power_standing, (Mario.x, Mario.y))
    else:
        draw_surface.blit(Mario_standing_image, (Mario.x, Mario.y))

    # Draw walking animations or jumping images for player 2
    if keys[pygame.K_LEFT]:
        if Luigi_ice_power_enabled:
            draw_surface.blit(pygame.transform.flip(Luigi_ice_power_walk_frames[frame_index2 % len(Luigi_ice_power_walk_frames)], True, False), (Luigi.x, Luigi.y))
        else:
            draw_surface.blit(pygame.transform.flip(Luigi_walk_frames[frame_index2], True, False), (Luigi.x, Luigi.y))
    elif keys[pygame.K_RIGHT]:
        if Luigi_ice_power_enabled:
            draw_surface.blit(Luigi_ice_power_walk_frames[frame_index2 % len(Luigi_ice_power_walk_frames)], (Luigi.x, Luigi.y))
        else:
            draw_surface.blit(Luigi_walk_frames[frame_index2], (Luigi.x, Luigi.y))
    elif (keys[pygame.K_UP] or keys[pygame.K_DOWN]) and not on_ground2:
        draw_surface.blit(Luigi_jump_ice_power_image if Luigi_ice_power_enabled else Luigi_jump_image, (Luigi.x, Luigi.y))
    elif Luigi_ice_power_enabled:
        draw_surface.blit(Luigi_ice_power_standing, (Luigi.x, Luigi.y))
    else:
        draw_surface.blit(Luigi_standing_image, (Luigi.x, Luigi.y))

    # Blit the draw_surface onto the screen
    screen.blit(background_image, (0, 0))
    screen.blit(draw_surface, (0, 0))
      # Timer
    font = pygame.font.Font(None, 36)
    timer_text = font.render(str(int(game_timer / FPS)), True, ("white"))
    screen.blit(timer_text, (SCREEN_WIDTH - 50, 10))

    # Update display
    pygame.display.flip()

    # Tick
    clock.tick(FPS)

    # Decrement freeze timers
    if freeze_timer1 > 0:
        freeze_timer1 -= 1
    if freeze_timer2 > 0:
        freeze_timer2 -= 1

    # Decrement bullet timers
    if bullet_timer1 > 0:
        bullet_timer1 -= 1
    if bullet_timer2 > 0:
        bullet_timer2 -= 1

     # Update timers
    game_timer -= 1
    if game_timer <= 0:
        game_over = True


# Display game over menu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Create game over menu
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over - PLayer {} Wins!".format(1 if tagged_player == Luigi else 2), True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
