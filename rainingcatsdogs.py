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
player1_s = pygame.image.load('graphics/Player/stand_boy.png').convert_alpha()
player_r = player1_s.get_rect(midbottom = (pos2,ground))
player2_s = pygame.image.load('graphics/Player/squat_boy.png').convert_alpha()
player_frames = [player1_s, player2_s]
player_index = 0
player_surface = player_frames[player_index]


# Timers
player_animation = pygame.USEREVENT + 1
pygame.time.set_timer(player_animation,300)


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

        # Mouse clicks for player position control / game restart
        if event.type == pygame.MOUSEBUTTONDOWN:
            (xcord, ycord) = pygame.mouse.get_pos()
            if xcord >=50 and xcord <= 350:
                player_r.midbottom = (pos1,ground)
            if xcord >= 351 and xcord <= 699:
                player_r.midbottom = (pos2,ground)
            if xcord >=700 and xcord <=950:
                player_r.midbottom = (pos3,ground)

        # Animate and show player
        if event.type == player_animation:
            if player_index == 0: 
                player_index = 1
            else: 
                player_index = 0
        player_s = player_frames[player_index]
        screen.blit(player_s,player_r)

    pygame.display.update()
    clock.tick(60)
