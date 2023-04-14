import random
import math
import pygame as py
from pygame.locals import *
from pygame import mixer
py.init()
#create a screen
screen = py.display.set_mode((800,600))
#game name
py.display.set_caption("invader")
#game logo
icon = py.image.load("invasion.png")
py.display.set_icon(icon)
#background
background = py.image.load("background.png")
#add music
mixer.music.load('background.wav')
mixer.music.play(-1)
#add player
playerimg = py.image.load("spaceship.png")
playerX=350
playerY=470
playerX_change =0

enemyimg=[]
enemyY=[]
enemyX=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemis =6

for i in range(no_of_enemis):
    enemyimg.append(py.image.load("skull.png"))
    enemyX.append(random.randint(66,734))
    enemyY.append(random.randint(40,150))
    enemyX_change.append(4)
    enemyY_change.append(40)


#bullet
#ready state you cant see the bullet
#fire state bullet is moving
bullet = py.image.load("bullet.png")
bulletX=playerX
bulletY=playerY
bulletX_change = 2
bulletY_change = 10
bullet_state="ready"

score_value = 0
font = py.font.Font('TheQualityBrave-Regular.ttf',32)
textX=15
textY=20

def show_score(x,y):
    score=font.render("score : "+str(score_value),True,(0,255,0))
    screen.blit(score, (x, y))

def player(X,Y):
    screen.blit(playerimg,(X,Y))
def enemy(X,Y,i):
    screen.blit(enemyimg[i],(X,Y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet,(x+16,y+10))

def iscollison(enemyX,enemyY,bulletX,bulletY):
    dis = math.sqrt(pow((enemyX-bulletX),2) + math.pow((enemyY-bulletY),2))
    if dis <=27:
        return True
    else:
        return False

def game_over():
    gameover = py.font.Font('TheQualityBrave-Regular.ttf', 42)
    game = gameover.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game, (330,200))


running =True
#gameloop
while running:
    screen.fill((0, 0, 0))
    #background
    screen.blit(background,(0,0))
   # enemyX+=0.1
    for event in py.event.get():
        if event.type == py.QUIT:
            running=False
      #check weather the right or left
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                playerX_change=-5
                print("left down")
            if event.key == py.K_RIGHT:
                playerX_change=5
                print("right down")
            if event.key == py.K_SPACE:
                if bullet_state == "ready":
                    bullletsound=mixer.Sound('laser.wav')
                    bullletsound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0.1
                print("pressed and released")
    playerX += playerX_change
    if playerX >= 734:
     playerX = 734
    if playerX <= 0:
        playerX = 0

    for i in range(no_of_enemis):
        if enemyY[i]>=300:
            for j in range(no_of_enemis):
                enemyY[j]=2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 734:
            enemyX_change[i] =-4
            enemyY[i]+=enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        if iscollison(enemyX[i], enemyY[i], bulletX, bulletY):
            collison_sound=mixer.Sound('explosion.wav')
            collison_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(66, 734)
            enemyY[i] = random.randint(40, 150)
        enemy(enemyX[i], enemyY[i],i)


    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    player(playerX,playerY)
    show_score(textX,textY)
    py.display.update()
