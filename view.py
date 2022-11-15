#!/usr/bin/env python
"""
This is a sample implementation.
"""

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import time
import os
import sys
import logging

import random

import numpy as np
from PIL import Image
import pygame

# ================================================================================== Global Variables
# ================================================================================== Global Functions
def  key_parse():
    from pygame.locals import K_ESCAPE, K_q, KMOD_CTRL, KSCAN_Z

    keys = pygame.key.get_pressed()

    # print(f"{KSCAN_Z}:{keys[KSCAN_Z]}")
    if keys[KSCAN_Z]: 
        print("Z has been pressed!!")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            return (event.key == K_ESCAPE) or (event.key == K_q and pygame.key.get_mods() & KMOD_CTRL)
    return False

def cycle_formula(x, ct, r, t):
    cx, cy = ct
    import math
    # return x*x +2*x +1
    # return math.sqrt( abs(25 - x*x) )
    v = math.pow(r*t, 2) - math.pow(x-cx*t, 2)
    # v = abs(v)
    if v < 0: return None, None
    v = math.sqrt(v)
    return v + cy*t, -v + cy*t

def my_game():
    pygame.init()
    pygame.font.init()

    width, height, channels = (1280,720,3) 
    display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Open the image form working directory
    # image = Image.open(os.path.join('images','SSD180.jpg'))
    # np_canvas = np.asarray(image).swapaxes(0, 1)
    # base_surface = pygame.surfarray.make_surface(np_canvas)
    # base_surface.set_colorkey((0, 0, 0))

    cx, cy = (0, 0)
    ind = 0
    while True:
        # time.sleep(0.033) # 30fps
        if key_parse(): return

        np_canvas = np.zeros((height, width, channels), dtype="uint8").swapaxes(0, 1)
        centerx, centery = width/2, height/2

        def draw_on_center(x, y, color):
            x = int(x + centerx)
            y = int(y + centery)
            if y > 0 and y < height and x > 0 and x < width:
                np_canvas[x][y] = color

        def new_center(cx, cy):
            rate = random.uniform(-100,100) 
            cx = cx + rate
            rate = random.uniform(-100,100) 
            cy = cy + rate
            if cx > width/4 or cx < -width/4: cx = 3
            if cy > height/4 or cy < -height/4: cy = 2
            return cx, cy

        def new_color():
            random.seed(time.time())
            R=random.uniform(0,255)
            G=random.uniform(0,255)
            B=random.uniform(0,255)
            return (R,G,B)
        
        times = 100 
        if ind <= 0:
            cx, cy = new_center(cx, cy)
            color = new_color()
            r_max = random.uniform(10,100)
            ind = 11
        ind -= 1
        r = int(r_max *ind/10)

        for x in range(width*times):
        # for x in range(int(2 * r_max)*times):
            x = x - centerx*times
            # x = x - cx*times
            y1, y2 = cycle_formula(x, [cx, cy], r, times)

            if x is None or y1 is None or y2 is None: 
                continue
            draw_on_center(x/times, y1/times, color)
            draw_on_center(x/times, y2/times, color)
        # draw_on_center(3, 2)
        # for x in range(160):
        #     x = x - 80
        #     y = 2
        #     draw_on_center(x, y)

        base_surface = pygame.surfarray.make_surface(np_canvas)
        base_surface.set_colorkey((0, 0, 0))

        if base_surface.get_size() != display.get_size():
            base_surface = pygame.transform.scale(base_surface, display.get_size())

        display.blit(base_surface, (0, 0))

        pygame.display.flip()

    pygame.quit()

# ==================================================================================

if __name__ == '__main__':
    my_game()