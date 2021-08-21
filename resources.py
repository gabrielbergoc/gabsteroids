import os
import pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(name, colorkey=None):
    full_name = os.path.join(main_dir, "images", name)

    try:
        image = pygame.image.load(full_name)
    except pygame.error as e:
        print(f"Cannot load image '{name}'")
        raise SystemExit(e)

    # image = image.convert()   # if it converts image, it gets weirdly resized

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))

        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()
