import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

#icon and title
icon = pygame.image.load("images/monitor.png")
title = "Space Invader"
pygame.display.set_icon(icon)
pygame.display.set_caption(title)

# background
background = pygame.image.load("images/bg1.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
player_img = pygame.image.load("images/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load("images/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(-200, -10))
    enemyX_change.append(4)
    enemyY_change.append(15)

# bullet
bullet_img = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over
Over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over():
    over_text = Over_font.render("GAME OVER", True, (0, 0, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False


# game loop
run = True
while run:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # keys for control
        if event.type == pygame.KEYDOWN:
            if enemyY[i] > 400:
                for j in range(no_of_enemies):
                    enemyY[j] = 1000

                game_over()
                break

            if event.key == pygame.K_LEFT:
                playerX_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change

    # boundary line for player
    if playerX <= 5:
        playerX = 5
    elif playerX >= 731:
        playerX = 731

    enemyX += enemyX_change

    # boundary line for player
    for i in range(no_of_enemies):

        # Game over
        if enemyY[i] > 400:
            for j in range(no_of_enemies):
                enemyY[j] = 1000

            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 731:
            enemyX_change[i] = -2.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(-200, -10)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= -10:
        bulletY = 480
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
