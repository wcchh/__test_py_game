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

import numpy as np
from PIL import Image
import pygame

# ================================================================================== Global Variables
# ==================================================================================
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

def my_game():
    pygame.init()
    pygame.font.init()

    width, height, channels = (1280,720,3) 
    display = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    # Open the image form working directory
    image = Image.open(os.path.join('images','SSD180.jpg'))
    np_canvas = np.asarray(image).swapaxes(0, 1)

    # np_canvas = np.zeros((height, width, channels), dtype="uint8").swapaxes(0, 1)
    base_surface = pygame.surfarray.make_surface(np_canvas)
    base_surface.set_colorkey((0, 0, 0))

    while True:
        time.sleep(0.033) # 30fps
        if key_parse(): return


        if base_surface.get_size() != display.get_size():
            base_surface = pygame.transform.scale(base_surface, display.get_size())

        display.blit(base_surface, (0, 0))

        pygame.display.flip()

    pygame.quit()

# ==================================================================================

if __name__ == '__main__':
    my_game()