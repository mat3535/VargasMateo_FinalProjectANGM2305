import pygame
from sys import exit
from random import randint,choice

import pygame.locals


pygame.init()
screen =  pygame.display.set_mode((1000,800))
pygame.display.set_caption("It's Raining Cats and Dogs")
clock = pygame.time.Clock()

# Keyboard delay
keyboard_delay = 100
keyboard_time = pygame.time.get_ticks() + keyboard_delay


def animal_rain(animal_r_list,dog_index,cat_index):
    """
        Controls which animal is displayed from 
        the list of rectangles and varies the drop rate.

        animal_r_list - a list of rectangles, each at a random x-coordinate
        from the three colum positions available.
        The y-coordinate is a random height above the screen within
        a range, to add variety to the drop rate.
        
        dog_index - a value to select which dog surface to load (for animation)
        
        cat_index - a value to select which cat surface to load (for animation)
        
        The dog's rectangle size is 1 pixel larger to differentiate it from the cat.

        returns animal_r_list
    """
    if animal_r_list:
        print(f'animal_r_list={animal_r_list}')
        for animal_r in animal_r_list:
            animal_r.y += 5
            if animal_r.height == 201:
                screen.blit(dog_frames[dog_index],animal_r)
            else:
                screen.blit(cat_frames[cat_index],animal_r)
        
        animal_r_list = [animal_r for animal_r in animal_r_list if animal_r.midbottom[1] < (ground + 1)]
        
        return animal_r_list
    else:
        return []

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
global rungame
rungame = True

# Animal drop position range boundaries
neg_top_r1 = -300
neg_top_r2 = -500

# Animal list for rain
animal_r_list=[]

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

# Cat graphics
cat1_s = pygame.image.load('graphics/Player/cat_wag1.png').convert_alpha()
cat_r = cat1_s.get_rect(midbottom = (pos1,top))
cat2_s = pygame.image.load('graphics/Player/cat_wag2.png').convert_alpha()
cat_frames = [cat1_s,cat2_s]
cat_index = 0
cat_surface = cat_frames[cat_index]

# Dog graphics
dog1_s = pygame.image.load('graphics/Player/dog_wag1.png').convert_alpha()
dog_r = dog1_s.get_rect(midbottom = (pos2,top))
dog2_s = pygame.image.load('graphics/Player/dog_wag2.png').convert_alpha()
dog_frames = [dog1_s,dog2_s]
dog_index = 0
dog_surface = dog_frames[dog_index]


# Timers
player_animation = pygame.USEREVENT + 2
pygame.time.set_timer(player_animation,200)

animal_animation = pygame.USEREVENT + 3
pygame.time.set_timer(animal_animation,300)

# Used to control delay for rate of animals
loop_start_time = pygame.time.get_ticks()


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

        if event.type == pygame.KEYDOWN:
            if pygame.time.get_ticks() >= keyboard_time:
                keyboard_time = pygame.time.get_ticks() + keyboard_delay
                if event.key == pygame.K_LEFT:
                    if player_r.midbottom == (pos1,ground):
                        pass
                    if player_r.midbottom == (pos2,ground):
                        player_r.midbottom = (pos1,ground)
                    if player_r.midbottom == (pos3,ground):
                        player_r.midbottom = (pos2,ground)
            
                elif event.key == pygame.K_RIGHT:
                    if player_r.midbottom == (pos3,ground):
                        pass
                    if player_r.midbottom == (pos2,ground):
                        player_r.midbottom = (pos3,ground)
                    if player_r.midbottom == (pos1,ground):
                        player_r.midbottom = (pos2,ground)
 
        # Append either a cat or a dog to the list 
        # of cats and dog rectangles.
        # Had to add a delay as default rate was a deluge
        animal_position = choice(pos_list)
        now = pygame.time.get_ticks()
        if now - loop_start_time >= randint(900,1500):
            if randint(0,2):
                animal_r_list.append(dog1_s.get_rect(midbottom = ((animal_position),randint(neg_top_r2,neg_top_r1))))
            else:
                animal_r_list.append(cat1_s.get_rect(midbottom = ((animal_position),randint(neg_top_r2,neg_top_r1))))
            loop_start_time = pygame.time.get_ticks()

        # Animate and show player
        if event.type == player_animation:
            if player_index == 0: 
                player_index = 1
            else: 
                player_index = 0
        player_s = player_frames[player_index]
        screen.blit(player_s,player_r)
        
        # Alternate the animal surface shown to create animation
        if event.type == animal_animation:
            if dog_index == 0:
                dog_index = 1
            else:
                dog_index = 0
            if cat_index == 0:
                cat_index = 1
            else:
                cat_index = 0

        # Make it rain cats and dogs
        animal_r_list = animal_rain(animal_r_list,dog_index,cat_index)

    pygame.display.update()
    clock.tick(60)
