import pygame
from pygame.locals import *
import random

from pygame.sprite import Group



clock = pygame.time.Clock()
fps = 60
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

#load image
bg = pygame.image.load("space/images/bg.png")

#game variables
rows = 5
cols= 5
last_alien_shot = pygame.time.get_ticks()
alien_cooldown = 1000


#colors

red = (255,0,0)
green = (0,255,0)

#def draw image
def draw_bg():
    screen.blit(bg, (0,0))

#create spaceship class
class spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("space/images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.health_start = health
        self.health_remain = health
        self.last_shot = pygame.time.get_ticks()
    def update(self):
        cooldown = 500 #in miliseconds
        speed = 8
        #get the pressed keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right <= screen_width:
            self.rect.x += speed
        #for shooting

        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and (time_now - self.last_shot > cooldown):
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = pygame.time.get_ticks()

        #draw health
        pygame.draw.rect(screen, red, (self.rect.x,self.rect.bottom + 10, self.rect.width, 15))
        if self.health_remain > 0:
            pygame.draw.rect(screen, green, (self.rect.x,self.rect.bottom + 10, (self.rect.width*self.health_remain/self.health_start), 15))
        
        
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("space/images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("space/images/alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
      
    
    def update(self):
        
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction*= -1
            self.move_counter *= self.move_direction


class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("space/images/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        




        
#create sprite groups
alien_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

#create player
player = spaceship(int(screen_width/2), screen_height-100, 3)
spaceship_group.add(player)

def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item*100,100 + row*70)
            alien_group.add(alien)

create_aliens()
run = True
while run:

    clock.tick(fps)
    draw_bg()

    time_now = pygame.time.get_ticks()

    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        aBullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        last_alien_shot = pygame.time.get_ticks()
        alien_bullet_group.add(aBullet)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #update the player
    player.update()

    #update sprite groupds
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()

    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)


    pygame.display.update()



pygame.quit()
