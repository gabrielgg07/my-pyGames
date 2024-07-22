import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 600
screen_height = 500


fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

#game variables
font = pygame.font.SysFont('Constantia',30)
margin = 50
cpu_score = 0
player_score = 0
fps = 60
live_ball = False
winner = 0
speed_increase = 0
game_mode = 0


#colours
bg = (50,25, 50)
white = (255,255,255)


def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen,white,(0,50),(screen_width, margin), 2)


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#paddle class 

class paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(x,y, 20, 100)
        self.speed = 5
        self.ai_speed = 5


    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip(0,-1*self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.move_ip(0,self.speed)

    def draw(self):
        pygame.draw.rect(screen,white, self.rect) 

    def ai(self):
        #move paddle auto
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.ai_speed)
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1*self.ai_speed)
    def move2(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.top > margin:
            self.rect.move_ip(0,-1*self.speed)
        if key[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.move_ip(0,self.speed)
class ball():
    def __init__(self, x, y):
        self.reset(x,y)
    def move(self):

        #check collision
        if self.rect.top < margin or self.rect.bottom > screen_height:
            self.speed_y *= -1
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1
       
        #check out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > screen_width:
            self.winner = -1

        #update ball pos
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(x,y, self.ball_rad*2, self.ball_rad*2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0 #1 is player -1 is cpu


player_paddle = paddle(screen_width - 40, screen_height//2)
cpu_paddle = paddle(20, screen_height//2)

pong = ball(screen_width - 60, screen_height//2 + 50)

run = True
while run:

    fpsClock.tick(fps)

    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, white, 20, 15)
    draw_text('P1: ' + str(player_score), font, white,screen_width -100, 15)
    draw_text('Ball Speed ' + str(abs(pong.speed_x)), font, white, screen_width//2 -60, 15)

    

    player_paddle.draw()
    cpu_paddle.draw()
   

    if live_ball == True:
        speed_increase+=1
        winner = pong.move()
        if winner == 0:
            pong.draw()
            player_paddle.move()
            if game_mode == 0:
                cpu_paddle.ai()
            elif game_mode == 1:
                cpu_paddle.move2()
        else:
            live_ball = False
            if winner == 1:
                player_score+=1
            else:
                cpu_score+=1

    #print player instructions
    if live_ball == False:
        if winner == 0:
            draw_text("Click to start", font, white, 220, screen_height//2 - 100)
        if winner ==1:
            draw_text("You Scored!", font, white, 220, screen_height//2 - 100)
            draw_text("Click to play again", font, white, 200, screen_height//2 - 50)
            draw_text("Press Space for P2", font, white, 200, screen_height//2 - 20)
        if winner ==-1:
            draw_text("You Lost Bitch!", font, white, 220, screen_height//2 - 100)
            draw_text("Click to play again", font, white, 200, screen_height//2 - 50)
            draw_text("Press Space for P2", font, white, 200, screen_height//2 - 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            game_mode = 0
            pong.reset(screen_width - 60, screen_height//2 + 50)
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                game_mode = 1
                live_ball = True
                pong.reset(screen_width - 60, screen_height//2 + 50)
                print(live_ball)


    if speed_increase > 500:
        speed_increase = 0
        if pong.speed_x < 0:
            pong.speed_x -= 1
        if pong.speed_x > 0:
            pong.speed_x += 1
        if pong.speed_y < 0:
            pong.speed_y -= 1
        if pong.speed_y > 0:
            pong.speed_y += 1
        

    pygame.display.update()


pygame.quit()