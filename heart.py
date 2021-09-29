import pygame.sprite
from resources import *

CWD = os.getcwd()


class Heart(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(os.path.join(CWD, "images", "black-heart.jpg"))[0]
        self.image = pygame.transform.scale(self.image, (38, 35))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
