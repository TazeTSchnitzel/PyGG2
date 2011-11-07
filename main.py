#!/usr/bin/env python

from __future__ import division, print_function

import math, pygame
from pygame.locals import *
try: import pygame._view # fix for py2exe dependency detection
except: pass

# DEBUG ONLY
import cProfile
import pstats
import os

import gg2

# global settings
PHYSICS_TIMESTEP = 1/30 # always update physics in these steps

# http://pygame.org/wiki/toggle_fullscreen
def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()
    
    w, h = screen.get_width(), screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w, h), flags ^ FULLSCREEN, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)
 
    pygame.key.set_mods(0) # HACK: work-a-round for a SDL bug??
 
    pygame.mouse.set_cursor(*cursor)
    
    return screen

# the main function
def GG2main():
    # initialize pygame
    pygame.init()
    
    # set display mode
    fullscreen = False # are we fullscreen? pygame doesn't track this
    window = pygame.display.set_mode((800, 600), (fullscreen * FULLSCREEN) | DOUBLEBUF)
    window.set_alpha(None)

    # keep state of keys stored for one frame so we can detect down/up events
    keys = pygame.key.get_pressed()
    
    # create game object
    game = gg2.GG2()
    
    # pygame time tracking
    clock = pygame.time.Clock()
    accumulator = 0.0 # this counter will accumulate time to be used by the physics
    
    # DEBUG code: calculate average fps
    average_fps = 0
    num_average_fps = 0
    
    font = pygame.font.Font(None, 17)
    text = font.render("%d FPS" % clock.get_fps(), True, (255, 255, 255), (159, 182, 205))
    
    # game loop
    while True:        
        # check if user exited the game
        if QUIT in {event.type for event in pygame.event.get()}:
            break
        
        # handle input
        oldkeys = keys
        keys = pygame.key.get_pressed()
        game.up = keys[K_w]
        game.down = keys[K_s]
        game.left = keys[K_a]
        game.right = keys[K_d]
        
        # DEBUG quit game with escape
        if keys[K_ESCAPE]: break
        
        # did we just release the F11 button? if yes, go fullscreen
        if oldkeys[K_F11] and not keys[K_F11]:
            fullscreen = not fullscreen
            if not pygame.display.toggle_fullscreen():
                game.window = toggle_fullscreen()

        leftmouse, middlemouse, rightmouse = pygame.mouse.get_pressed()
        game.leftmouse = leftmouse
        game.middlemouse = middlemouse
        game.rightmouse = rightmouse
        game.mouse_x, game.mouse_y = pygame.mouse.get_pos()
        
        # update the game and render
        clock.tick(80)
        frame_time = min(0.25, clock.get_time() / 1000) # a limit of 0.25 seconds to prevent complete breakdown
        
        accumulator += frame_time
        while accumulator > PHYSICS_TIMESTEP:
            accumulator -= PHYSICS_TIMESTEP
            game.update(PHYSICS_TIMESTEP)
        
        game.render(accumulator / PHYSICS_TIMESTEP)
        
        text = font.render("%d FPS" % clock.get_fps(), True, (255, 255, 255), (159, 182, 205))
        game.window.blit(text, (0, 0))
        
        pygame.display.flip()
    
    # clean up
    pygame.quit()

def profileGG2():
    cProfile.run("GG2main()", "game_profile")
    p = pstats.Stats("game_profile", stream=open("profile.txt", "w"))
    p.sort_stats("cumulative")
    p.print_stats(30)
    os.remove("game_profile")
    
if __name__ == "__main__":
    # when profiling:
    profileGG2()
    # GG2main()