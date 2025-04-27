import pygame
from sys import exit


pygame.init()
screen =  pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()

# Control variables
# Top and ground
top = 0
ground = 700

# Column positions
pos1 = 200
pos2 = 500
pos3 = 800
pos_list = [pos1,pos2,pos3]

# game on/off
rungame = True

# Background graphics
ground_s = pygame.image.load('graphics/floor.png').convert()
ground_r = ground_s.get_rect(midtop = (500,550))
back_s = pygame.image.load('graphics/top.png').convert()

# Player  graphics
player_s = pygame.image.load('graphics/Player/stand_boy.png').convert_alpha()
player_r = player_s.get_rect(midbottom = (pos2,ground))


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if rungame:

        # Draw background graphics
        screen.blit(ground_s,(0,ground))
        screen.blit(back_s,(0,0))

        if event.type == pygame.MOUSEBUTTONDOWN:
            (xcord, ycord) = pygame.mouse.get_pos()
            if xcord >=50 and xcord <= 350:
                player_r.midbottom = (pos1,ground)
            if xcord >= 351 and xcord <= 699:
                player_r.midbottom = (pos2,ground)
            if xcord >=700 and xcord <=950:
                player_r.midbottom = (pos3,ground)

        screen.blit(player_s,player_r)

    pygame.display.update()
    clock.tick(60)

