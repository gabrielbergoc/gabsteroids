import pygame.sprite
from resources import *
from stats import Stats
from random import randint, choice

CWD = os.getcwd()


class Asteroids(pygame.sprite.Sprite):
    """create and control asteroids"""

    def __init__(self, x_vel=None, y_vel=None, size=None, center=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(os.path.join(CWD, "images", "black-boulder-pixel-cropped.png"))[0]
        self.area = pygame.display.get_surface().get_rect()
        self.__stats = AsteroidsStats(x_vel, y_vel, size)
        self.image = self.original = pygame.transform.rotozoom(self.image, self.__stats.angle, self.__stats.size)
        self.rect = self.image.get_rect()
        if center is None:
            self.rect.center = (
                choice((randint(-200, 0), randint(800, 1000))),
                choice((randint(-200, 0), randint(600, 800)))
            )
        else:
            self.rect.center = center

    def update(self):
        """moves asteroid and bounces it 300 pixels offscreen"""

        # move asteroid
        self.rect.move_ip(self.__stats.x_vel, self.__stats.y_vel)
        self.__bounce()

    def __bounce(self):
        # bounce left
        if self.rect.left < self.area.left - 300:
            self.rect.left = self.area.left - 300
            self.__stats.x_vel = -self.__stats.x_vel

        # bounce right
        if self.rect.right > self.area.right + 300:
            self.rect.right = self.area.right + 300
            self.__stats.x_vel = -self.__stats.x_vel

        # bounce top
        if self.rect.top < self.area.top - 300:
            self.rect.top = self.area.top - 300
            self.__stats.y_vel = -self.__stats.y_vel

        # bounce bottom
        if self.rect.bottom > self.area.bottom + 300:
            self.rect.bottom = self.area.bottom + 300
            self.__stats.y_vel = -self.__stats.y_vel

    # splits asteroid into two new smaller asteroids
    def split(self):
        astA_vector = rotate_vector([self.__stats.x_vel, self.__stats.y_vel], 45)
        astB_vector = rotate_vector([self.__stats.x_vel, self.__stats.y_vel], -45)
        return Asteroids(astA_vector[0][0], astA_vector[1][0], self.__stats.size - 0.1, self.rect.center),\
            Asteroids(astB_vector[0][0], astB_vector[1][0], self.__stats.size - 0.1, self.rect.center)

    # splits asteroid into two debris pieces if it gets too small
    def debris(self):
        astA_vector = rotate_vector([self.__stats.x_vel, self.__stats.y_vel], 45)
        astB_vector = rotate_vector([self.__stats.x_vel, self.__stats.y_vel], -45)
        return Asteroids(astA_vector[0][0], astA_vector[1][0], self.__stats.size - 0.09, self.rect.center),\
            Asteroids(astB_vector[0][0], astB_vector[1][0], self.__stats.size - 0.09, self.rect.center)

    def get_size(self):
        return self.__stats.size


class AsteroidsStats(Stats):

    def __init__(self, x_vel=None, y_vel=None, size=None):
        Stats.__init__(self)

        if x_vel is None:
            self.x_vel = randint(1, 3)
        else:
            self.x_vel = x_vel

        if y_vel is None:
            self.y_vel = randint(1, 3)
        else:
            self.y_vel = y_vel

        if size is None:
            self.size = randint(1, 5) / 10
        else:
            self.size = size

        self.angle = randint(0, 360)
