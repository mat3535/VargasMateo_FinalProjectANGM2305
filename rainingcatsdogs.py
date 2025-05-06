import pygame
from sys import exit
from random import randint,choice

import pygame.locals


pygame.init()
screen =  pygame.display.set_mode((1000,800))
pygame.display.set_caption("It's Raining Cats and Dogs")
clock = pygame.time.Clock()
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)
large_font = pygame.font.Font("font/Pixeltype.ttf", 70)
title_text_color = (255,255,255)
text_color = (65,65,65)
speed_rate = 3

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

        speed_rate - a base level of speed for animal drop rate
        
        The dog's rectangle size is 1 pixel larger to differentiate it from the cat.

        returns animal_r_list
    """
    # Increase animal drop speed every minute
    global speed_start_time
    global speed_rate
    now = pygame.time.get_ticks()
    if now - speed_start_time < 60000:
        pass
    else:
        speed_rate += 1
        speed_start_time = pygame.time.get_ticks()

    if animal_r_list:
        print(f'animal_r_list={animal_r_list}')
        for animal_r in animal_r_list:
            animal_r.y += randint(speed_rate,speed_rate+1)
            if animal_r.height == 201:
                screen.blit(dog_frames[dog_index],animal_r)
            else:
                screen.blit(cat_frames[cat_index],animal_r)
        
        animal_r_list = [animal_r for animal_r in animal_r_list if animal_r.midbottom[1] < (ground + 1)]
        
        return animal_r_list
    else:
        return []

def show_score(catches, misses):
    """
       Displays the total catches and misses in two different formats
       depending if the game is still running or if it has ended.

       catches - number of times the player rectangle collided with
       an animal rectangle

       misses - number of times an animal rectangle collided with the
       ground
    
    """
    
    if rungame == True:
        catches_pos = (30,750)
        misses_pos = (970,750)
        catches_s = game_font.render(f'Catches: {catches}',False,text_color)
        catches_r = catches_s.get_rect(midleft = catches_pos)
        misses_s = game_font.render(f'Misses: {misses}',False,text_color)
        misses_r = misses_s.get_rect(midright = misses_pos)
    else:
        catches_pos = (pos1,500)
        misses_pos = (pos3,500)
        end_msg_s = large_font.render('Final Scores',False,title_text_color)
        end_msg_r = end_msg_s.get_rect(midbottom = (500,450))
        catches_s = large_font.render(f'Catches: {catches}',False,text_color)
        catches_r = catches_s.get_rect(midleft = catches_pos)
        misses_s = large_font.render(f'Misses: {misses}',False,text_color)
        misses_r = misses_s.get_rect(midright = misses_pos)
        screen.blit(end_msg_s,end_msg_r)

    screen.blit(catches_s,catches_r)
    screen.blit(misses_s,misses_r)

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
rungame = False

# Animal drop position range boundaries
neg_top_r1 = -300
neg_top_r2 = -500

# Animal list for rain
animal_r_list=[]

# Collision tracking
catches = 0
misses = 0

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
pygame.time.set_timer(animal_animation,200)

# Used to control delay for rate of animals
loop_start_time = pygame.time.get_ticks()
speed_start_time = pygame.time.get_ticks()

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
        # Had to skip delay if the list gets down to one rectangle to keep the list
        # from emptying.
        animal_position = choice(pos_list)
        now = pygame.time.get_ticks()
        if now - loop_start_time >= randint(800,1200) or len(animal_r_list) == 1:
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

        # Count collisions (catches and misses)
        # - Catches are collisions between an animal rectangle and the player's rectangle
        # - Misses are collisions between an animal rectangle and the ground rectangle
        # Remove the rectacle from the list when a collision occurs to make it dissapear
        for animal_r in animal_r_list:
            if player_r.colliderect(animal_r):
                animal_r_list.remove(animal_r)
                #if len(animal_r_list) > 1:
                catches += 1
            elif  animal_r.colliderect(ground_r):
                #if len(animal_r_list) > 1:
                animal_r_list.remove(animal_r)
                misses += 1

            # Show catches and misses on screen
            show_score(catches,misses)
        
        # If we have 3 misses, switch to end screen
        if misses == 3:
            rungame = False
    else:
        # This is the end screen
        screen.fill((0,0,0))

        if catches != 0:
            # Show final scores
            show_score(catches,misses)

            # Play again?
            play_again_s = game_font.render('Press spacebar to play again!',False,text_color)
            play_again_r = play_again_s.get_rect(midtop = (500,550))
            screen.blit(play_again_s,play_again_r)
        else:
            # Welcome to game
            welcome_s = large_font.render("Welcome to It's Raining Cats and Dogs",False,title_text_color)
            welcome_r = welcome_s.get_rect(midtop = (500,350))
            screen.blit(welcome_s,welcome_r)

            instructions0_s = game_font.render("How to play:",False,text_color)
            instructions0_r = instructions0_s.get_rect(midbottom = (500,450))
            instructions1_s = game_font.render("1. Click to move the player to the desired catch position.",False,text_color)
            instructions1_r = instructions1_s.get_rect(midbottom = (500,500))
            instructions2_s = game_font.render("2. Don't let them drop!",False,text_color)
            instructions2_r = instructions2_s.get_rect(midbottom = (500,550))
            screen.blit(instructions0_s,instructions0_r)
            screen.blit(instructions1_s,instructions1_r)
            screen.blit(instructions2_s,instructions2_r)

            start_s = game_font.render('Press spacebar to start playing!',False,text_color)
            start_r = start_s.get_rect(midbottom = (500,650))
            screen.blit(start_s,start_r)

        # Show player and animal graphics on final screen
        dog1_r = dog1_s.get_rect(midbottom =  (pos1,300))
        screen.blit(dog1_s,dog1_r)

        player1_r = player1_s.get_rect(midbottom = (pos2,300))
        screen.blit(player1_s,player1_r)

        cat1_r = cat1_s.get_rect(midbottom = (pos3,300))
        screen.blit(cat1_s,cat1_r)

        # Capture the mouse click to restartt
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            # Empty the animals list to start again
            animal_r_list.clear()
            # Zero out the score counters
            catches = 0
            misses = 0
            # Speed control over time
            speed_start_time = pygame.time.get_ticks()
            # Restart game
            rungame = True

    pygame.display.update()
    clock.tick(60)
