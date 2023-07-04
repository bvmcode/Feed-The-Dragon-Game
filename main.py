import pygame
import random

pygame.init()

# PLAY GAME CONSTANTS
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_VELOCITY = 10
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

# DISPLAY
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
SCOREBOX_HEIGHT = 64
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

# IMAGES
dragon_img = pygame.image.load("./assets/dragon_right.png")
dragon_rect = dragon_img.get_rect()
dragon_rect.left = 32
dragon_rect.centery = WINDOW_HEIGHT//2

coin_img = pygame.image.load("./assets/coin.png")
coin_rect = coin_img.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.top = random.randint(SCOREBOX_HEIGHT, WINDOW_HEIGHT-32)

# SOUNDS
coin_sound = pygame.mixer.Sound("./assets/coin_sound.wav")
miss_sound = pygame.mixer.Sound("./assets/miss_sound.wav")
miss_sound.set_volume(.1)
pygame.mixer.music.load("./assets/ftd_background_music.wav")
pygame.mixer.music.play(-1, 0)

# STARTING VALS
running = True
score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_VELOCITY

# COLORS
GREEN = (0,255,0)
DARK_GREEN = (10,50,10)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# FONTS AND TEXT
font = pygame.font.Font("./assets/AttackGraffiti.ttf", 32)

score_text = font.render(f"Score: {score}", True, GREEN, DARK_GREEN)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

title_text = font.render("Feed the Dragon", True, GREEN, WHITE)
title_text_rect = title_text.get_rect()
title_text_rect.centerx = WINDOW_WIDTH//2
title_text_rect.y = 10

lives_text = font.render(f"Lives: {player_lives}", True, GREEN, DARK_GREEN)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WINDOW_WIDTH-10, 10)

game_over_text = font.render("GAMEOVER", True, GREEN, DARK_GREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, GREEN, DARK_GREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

# CLOCK SETTINGS
clock = pygame.time.Clock()
FPS = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if not dragon_rect.top<SCOREBOX_HEIGHT:
            dragon_rect.y -= 10
    if keys[pygame.K_DOWN]:
        if not dragon_rect.bottom>WINDOW_HEIGHT:
            dragon_rect.y += 10

    if coin_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        coin_rect.x= WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(SCOREBOX_HEIGHT, WINDOW_HEIGHT-32)
    else:
        coin_rect.x -= coin_velocity

    if dragon_rect.colliderect(coin_rect):
        score+=1
        coin_sound.play()
        coin_velocity+=COIN_ACCELERATION
        coin_rect.x= WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(SCOREBOX_HEIGHT, WINDOW_HEIGHT-32)

    score_text = font.render(f"Score: {score}", True, GREEN, DARK_GREEN)
    lives_text = font.render(f"Lives: {player_lives}", True, GREEN, DARK_GREEN)

    if player_lives == 0:
        pygame.mixer.music.stop()
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    coin_velocity = COIN_VELOCITY
                    is_paused = False
                    score_text = font.render(f"Score: {score}", True, GREEN, DARK_GREEN)
                    lives_text = font.render(f"Lives: {player_lives}", True, GREEN, DARK_GREEN)
                    dragon_rect.centery = WINDOW_HEIGHT//2
                    pygame.display.update()
                    pygame.mixer.music.play(-1, 0)


    display_surface.fill(BLACK)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(lives_text, lives_text_rect)
    pygame.draw.line(display_surface, WHITE, (0, SCOREBOX_HEIGHT), (WINDOW_WIDTH, SCOREBOX_HEIGHT), 2)

    display_surface.blit(dragon_img, dragon_rect)
    display_surface.blit(coin_img, coin_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()