import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy
from squadron import Squadron

# Game Settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GAME_SIDE_MARGIN = 10
GAME_TOP_MARGIN = 40
GAME_BOTTOM_MARGIN = GAME_TOP_MARGIN
GAME_BORDER_WIDTH = 3

GAME_WALL_TOP = GAME_TOP_MARGIN + GAME_BORDER_WIDTH
GAME_WALL_RIGHT = WINDOW_WIDTH - GAME_SIDE_MARGIN - GAME_BORDER_WIDTH
GAME_WALL_BOTTOM = WINDOW_HEIGHT - GAME_BOTTOM_MARGIN - GAME_BORDER_WIDTH
GAME_WALL_LEFT = GAME_SIDE_MARGIN + GAME_BORDER_WIDTH


# COLORS
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)
COLOR_BLUE = (0,0,255)
COLOR_RED = (255,0,0)

# Setup Pygame Elements
pygame.init()
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('SPACE INVADERS')
title_font = pygame.font.SysFont('Courier', 40, True)
score_font = pygame.font.SysFont('Courier', 28, True)
title_text = title_font.render('SPACE INVADERS', False, COLOR_RED)
clock = pygame.time.Clock()


# Load Media
player_img = pygame.image.load('Media/si-player.png')
bullet_img = pygame.image.load('Media/si-bullet.gif')
enemy_img = pygame.image.load('Media/si-enemy.gif')
background_img = pygame.image.load('Media/si-background.gif')
laser_sound = pygame.mixer.Sound('Media/laser.wav')
explosion_sound = pygame.mixer.Sound('Media/explode.wav')
pygame.mixer.music.load('Media/Space Jump Music Loop copy.wav')
pygame.mixer.music.play(-1)


arrow_key_events = []
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.is_alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                arrow_key_events.append("LEFT")
            elif event.key == pygame.K_RIGHT:
                arrow_key_events.append("RIGHT")
            elif event.key == pygame.K_SPACE:
                player.shoot(bullet_img, laser_sound)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if arrow_key_events[len(arrow_key_events) - 1] == "LEFT":
                    arrow_key_events.pop()
            elif event.key == pygame.K_RIGHT:
                if arrow_key_events[len(arrow_key_events) - 1] == "RIGHT":
                    arrow_key_events.pop()
    
        if len(arrow_key_events) > 0:        
            if arrow_key_events[len(arrow_key_events) - 1] == "LEFT":
                player.move_left()
            elif arrow_key_events[len(arrow_key_events) - 1] == "RIGHT":
                player.move_right()
        else:
            player.stop_moving()
            
            



def show_game_scene(score):
    game_display.blit(game_display, (0,0))
    game_display.fill(COLOR_BLACK)
    pygame.draw.rect(game_display, COLOR_WHITE, \
        (GAME_SIDE_MARGIN, GAME_TOP_MARGIN, \
        WINDOW_WIDTH - GAME_SIDE_MARGIN * 2, \
        WINDOW_HEIGHT - GAME_TOP_MARGIN - GAME_BOTTOM_MARGIN))
    game_display.blit(background_img, \
        (GAME_WALL_LEFT, GAME_WALL_TOP), \
        (0, 0, GAME_WALL_RIGHT - GAME_WALL_LEFT, GAME_WALL_BOTTOM - GAME_WALL_TOP))
    game_display.blit(title_text, (WINDOW_WIDTH / 2 - title_text.get_width() / 2, 1))
    score_text = score_font.render('SCORE: ' + str(score), False, COLOR_RED)
    game_display.blit(score_text, (GAME_SIDE_MARGIN, WINDOW_HEIGHT - score_text.get_height()))

player = Player(GAME_WALL_LEFT, GAME_WALL_RIGHT, GAME_WALL_BOTTOM, player_img)
levels = []
levels.append(Squadron(GAME_WALL_LEFT, GAME_WALL_TOP, 3, 5, 2, enemy_img))
levels.append(Squadron(GAME_WALL_LEFT, GAME_WALL_TOP, 3, 5, 4, enemy_img))
levels.append(Squadron(GAME_WALL_LEFT, GAME_WALL_TOP, 5, 6, 2, enemy_img))
levels.append(Squadron(GAME_WALL_LEFT, GAME_WALL_TOP, 5, 6, 4, enemy_img))
levels.append(Squadron(GAME_WALL_LEFT, GAME_WALL_TOP, 8, 8, 4, enemy_img))
level_number = 0



# Main Game Loop
while player.is_alive:

    squadron = levels[level_number]

    if len(squadron.enemies) == 0:
        level_number += 1
        squadron = levels[level_number]
    
    handle_events()


    squadron.move(GAME_WALL_LEFT, GAME_WALL_RIGHT)
    player.remove_missed_bullets(GAME_WALL_TOP)
    player.kill_enemies_colliding_with_bullets(squadron, game_display, explosion_sound)
    player.kill_player_if_invaded(squadron, GAME_WALL_BOTTOM)

    show_game_scene(player.score)
    player.show(GAME_WALL_LEFT, GAME_WALL_RIGHT, game_display)
    squadron.show(game_display)
    Bullet.show_all_bullets(game_display, player.bullets_fired)

    pygame.display.update()
    clock.tick(60)

pygame.quit()