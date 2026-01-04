import pygame
from actions import Actions

def get_actions_player1() -> Actions:
    key = pygame.key.get_pressed()

        #movement
    #movement
    movex = 0
    if key[pygame.K_LEFT]:
        movex = -1
    elif key[pygame.K_RIGHT]:
        movex = 1

    #jump
    jump = key[pygame.K_UP]
    #attack actions
    punch = key[pygame.K_r]
    kick = key[pygame.K_t]

    return Actions(movex=movex, jump=jump, punch=punch, kick=kick)