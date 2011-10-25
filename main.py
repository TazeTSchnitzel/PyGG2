#!/usr/bin/env python

from __future__ import division

from gg2 import GG2
import pygame
import pygame._view # fix for 7-zip compressed dependencies
from pygame.locals import *

import cProfile

# global settings
framerate = 80

# the main function
def GG2main():
    # initialize
    pygame.init()
    game = GG2()

    # game loop
    while True:        
        # check if user exited the game
        if QUIT in {event.type for event in pygame.event.get()}:
            break
        
        # handle input
        key = pygame.key.get_pressed()
        game.up = key[K_w]
        game.left = key[K_a]
        game.right = key[K_d]

        leftmouse, middlemouse, rightmouse = pygame.mouse.get_pressed()
        game.leftmouse = leftmouse
        game.middlemouse = middlemouse
        game.rightmouse = rightmouse
        
        # update the game and render
        seconds_since_last_frame = game.clock.get_time() / 1000
        if seconds_since_last_frame > 0.2:
            seconds_since_last_frame = 0.2 # the game locks at 5 fps. Anything slower and we might fall through the floor
        game.update(seconds_since_last_frame)
        game.render()

        # wait to get steady frame rate
        game.clock.tick(framerate)
        
    # clean up
    pygame.quit()

# when profiling:
cProfile.run("GG2main()")
# GG2main()