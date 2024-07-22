import pygame
from pygame.locals import *
import random

pygame.init()

#initialize screen and clock
screen_width = 600
screen_height = 500
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

#game vars
fps = 60


#colours
white = (255,255,255)
black = (100,100,100)
dark_gray = (120, 120, 120)
gray  = (211,211,211)
cherry_red = (255, 8, 0)
green = (0,100,0)
yellow = (255,255,0)


def draw_board():
    screen.fill(gray)

class paddle():
    def __init__(self):
        self.x = screen_width//2 - 50
        self.y = screen_height - 60
        self.Orect = Rect(self.x, self.y, 100, 16)
        self.Irect = Rect(self.x + 3, self.y + 2, 94, 12)
        self.speed = 5

    def draw(self):
        pygame.draw.rect(screen,black, self.Orect) 
        pygame.draw.rect(screen,dark_gray, self.Irect) 
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.Orect.left > 0:
            self.Orect.move_ip(-1*self.speed,0)
            self.Irect.move_ip(-1*self.speed,0)
        if key[pygame.K_RIGHT] and self.Orect.right < screen_width:
            self.Orect.move_ip(self.speed,0)
            self.Irect.move_ip(self.speed,0)


class block():
    def __init__(self, x , y, lives):
        self.x = x
        self.y = y
        self.Orect = Rect(self.x, self.y, 94, 50)
        self.Irect = Rect(self.x + 3, self.y + 3, 88, 44)
        self.lives = lives

    def draw(self):
        pygame.draw.rect(screen,dark_gray, self.Orect)
        color = (0,0,0)
        if self.lives == 3:
            color = green
        elif self.lives == 2:
            color = yellow
        elif self.lives == 1:
            color = cherry_red
        pygame.draw.rect(screen,color, self.Irect) 


class ball():
    def __init__(self, x, y):
        self.reset(x,y)
    def move(self):

        #check collision
        if self.rect.right > screen_width or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
       
        #check out of block hit
        for a in range(3):
            for b in range(6):
                if blockA[a][b].Orect.colliderect(self.rect):
                    if blockA[a][b].Orect.bottom >= self.rect.top and self.speed_y < 0:
                        self.speed_y *= -1
                    if blockA[a][b].Orect.top >= self.rect.bottom and self.speed_y > 0:
                        pass
                    if blockA[a][b].Orect.left <= self.rect.right and self.speed_x > 0:
                        self.speed_x *= -1
                    if blockA[a][b].Orect.right >= self.rect.left and self.speed_x < 0:
                        self.speed_x *= -1
                   
                    blockA[a][b].lives -= 1
                    if blockA[a][b].lives == 0:
                        blockA[a][b].Orect = Rect(0,0, 0, 0)
                        blockA[a][b].Irect = Rect(0,0, 0, 0)
        
        if self.rect.colliderect(player.Orect):
            self.speed_x *= -1 + player.speed
            if self.speed_x > 8:
                self.speed_x = 8
            if self.speed_x < -8:
                self.speed_x = 8


        #update ball pos
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(x,y, self.ball_rad*2, self.ball_rad*2)
        self.speed_x = 4
        self.speed_y = -4
        self.winner = 0 #1 is player -1 is cpu



player = paddle()
pong = ball(400,400)
blockA = [[None]*6,[None]*6,[None]*6]



def create_row(y, lives, row):
    for i in range(6):
        blockA[row][i] = block(100*i + 3,y,lives)
def draw_row(row):
    for i in range(6):
        if blockA[row][i].lives != 0:
            blockA[row][i].draw()


create_row(3,3,0)
create_row(60,2,1)
create_row(117,1,2)

run = True
while run:

    fpsClock.tick(fps)
    draw_board()
    player.draw()
    player.move()
    
    draw_row(0)
    draw_row(1)
    draw_row(2)
    pong.move()
    pong.draw()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()