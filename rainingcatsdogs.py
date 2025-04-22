import pygame
from sys import exit


pygame.init()
screen =  pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()

# Control variables
# Top and ground
top = 0
ground = 700

# game on/off
rungame = True

# Background graphics
ground_s = pygame.image.load('graphics/floor.png').convert()
ground_r = ground_s.get_rect(midtop = (500,550))
back_s = pygame.image.load('graphics/top.png').convert()

# Player  graphics
player_s = pygame.image.load('graphics/Player/stand_boy.png').convert_alpha()
player_r = player_s.get_rect(midbottom = (500,ground))


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

        screen.blit(player_s,player_r)

    pygame.display.update()
    clock.tick(60)
