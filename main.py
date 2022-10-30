import pygame
import random
import math
from pygame import mixer

# Initialize PyGame
pygame.init()

# Define screen resolution
display = pygame.display.set_mode((800, 600))

# Title, icon and background
pygame.display.set_caption('Monster Invasion by Franco Sparn')
icon = pygame.image.load('static/img/icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('static/img/background.png')

# Game music
mixer.music.load('static/sounds/main.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

# Player variables
img_player = pygame.image.load('static/img/dragon.png')
player_x = 368
player_y = 530
player_x_change = 0

# Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_amount = 5

for e in range(enemy_amount):
    img_enemy.append(pygame.image.load('static/img/enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 300))
    enemy_x_change.append(2.5)
    enemy_y_change.append(50)

# Bullet variables
img_bullet = pygame.image.load('static/img/bullet.png')
bullet_x = 0
bullet_y = 530
bullet_x_change = 0
bullet_y_change = 5
bullet_visible = False

# Score variable
score = 0
font = pygame.font.Font('static/fonts/VCR_OSD_MONO_1.001.ttf', 28)
text_x = 10
text_y = 10

# Endgame text
end_font = pygame.font.Font('static/fonts/VCR_OSD_MONO_1.001.ttf', 48)


# End text function
def end_text():
    end_message = end_font.render('Game Over', True, (0, 0, 0))
    display.blit(end_message, (290, 200))
    

# Show score function
def show_score(x, y):
    text = font.render(f'Score:{score}', True, (255, 255, 255))
    display.blit(text, (x, y))


# Enemy function
def enemy(x, y, enem):
    display.blit(img_enemy[enem], (x, y))


# Player function
def player(x, y):
    display.blit(img_player, (x, y))


# Bullet function
def shooting_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    display.blit(img_bullet, (x + 16, y + 10))


# Detect collisions function
def collision_ok(x_1, y_1, x_2, y_2):
    distance = math.sqrt((math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
run = True

while run:

    # Background image
    display.blit(background, (0, 0))

    # Iterate events
    for event in pygame.event.get():

        # Close event
        if event.type == pygame.QUIT:
            run = False

        # Event to check if a keys is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('static/sounds/shoot.mp3')
                bullet_sound.set_volume(0.3)
                bullet_sound.play()
                if not bullet_visible:
                    bullet_x = player_x
                    shooting_bullet(bullet_x, bullet_y)

        # Event that checks if a key was released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Modify player location
    player_x += player_x_change

    # Keep player location
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Modify enemy location
    for e in range(enemy_amount):

        # End of the game
        if enemy_y[e] > 490:
            for k in range(enemy_amount):
                enemy_y[k] = 1000
            end_text()
            break

        enemy_x[e] += enemy_x_change[e]

        # Keep enemy location
        if enemy_x[e] <= 0:
            enemy_x_change[e] = 3.5
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 736:
            enemy_x_change[e] = -3.5
            enemy_y[e] += enemy_y_change[e]

        # Collision
        collision = collision_ok(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
        if collision:
            hit_sound = mixer.Sound('static/sounds/hit.mp3')
            hit_sound.set_volume(0.3)
            hit_sound.play()
            bullet_y = 500
            bullet_visible = False
            score += 1
            enemy_x[e] = random.randint(0, 736)
            enemy_y[e] = random.randint(0, 300)

        enemy(enemy_x[e], enemy_y[e], e)

    # Bullet motion
    if bullet_y <= 0:
        bullet_y = 500
        bullet_visible = False

    if bullet_visible:
        shooting_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Run functions
    player(player_x, player_y)
    show_score(text_x, text_y)

    # Run update
    pygame.display.update()
