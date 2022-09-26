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
import pygame

# ================================================================================== Global Variables
DEF_CFG = {}

# ==============================================================================
# -- function() ---------------------------------------------------------------
# ==============================================================================

# ==============================================================================
# -- class() ---------------------------------------------------------------
# ==============================================================================
class Customize(): 
    def __init__(self, options={}):
        self.cfg = {**DEF_CFG, **options}
    def __del__(self): return self.release()

    def render(self, pygame, display, res):
        width, height = res # base_dimention # display.get_size()
        channels = 3
        np_canvas = np.zeros((height, width, channels), dtype="uint8").swapaxes(0, 1)
        base_surface = pygame.surfarray.make_surface(np_canvas)

        if base_surface.get_size() != display.get_size():
            base_surface = pygame.transform.scale(base_surface, display.get_size())
        base_surface.set_colorkey((0, 0, 0))
        display.blit(base_surface, (0, 0))
        return
    def release(self):
        return

class View():
    def __init__(self, options={}):
        self.cfg = {**DEF_CFG, **options}
        pygame.init()
        pygame.font.init()


    def __del__(self): return self.release()
    def release(self):
        pygame.quit()
        return

    def  key_parse(self):
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

    def game_loop(self, args=None):
        try: 
            width, height = (args.width, args.height) if args is not None else (1280,720) 
            display = pygame.display.set_mode(
                (width, height),
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            display.fill((0,0,0))
            pygame.display.flip()

            cu = self.cfg.get("custom")
        
            while True:
                time.sleep(0.03)

                if self.key_parse(): return

                cu.render(pygame, display, (width, height))
                pygame.display.flip()
        finally:
            cu.release()

# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================

def show(args=None):
    cu = Customize()
    gv = View({"custom":cu})

    gv.game_loop(args)
    return

def main(params={}):
    import argparse
    argparser = argparse.ArgumentParser(
        description='View')
    argparser.add_argument("-d", "--debug",
        action='store_true',
        help="Debug Run (show debug logs)")    
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        # default='1280x720',
        default=params.get("res", '1280x720'),
        help='window resolution (default: 1280x720)')

    args = argparser.parse_args()
    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    print(__doc__)

    return show(args)


# ==============================================================================
if __name__ == '__main__':
    main()
    pass