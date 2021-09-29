import math
import pygame.sprite
from resources import *
from stats import Stats

CWD = os.getcwd()


class Bullets(pygame.sprite.Sprite):
    """handle bullets"""

    def __init__(self, pos, angle, vel=10):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(os.path.join(CWD, "images", "bullet-v2.png"))
        self.area = pygame.display.get_surface().get_rect()
        self.rect.center = pos
        self.image = pygame.transform.rotozoom(self.image, angle, 1)
        self.__stats = Stats(vel=vel, angle=angle)

    def update(self):
        """moves bullet"""

        self.rect.move_ip(self.__get_deltas())

    def __get_deltas(self):
        dx = math.cos(math.radians(self.__stats.angle)) * self.__stats.vel
        dy = -math.sin(math.radians(self.__stats.angle)) * self.__stats.vel
        # the minus in -sin is because the y coordinate increases downwards

        return dx, dy

    def kill_offscreen(self):
        if not self.area.contains(self.rect):
            self.kill()
