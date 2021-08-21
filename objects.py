import pygame
import math
from random import randint, choice
from pygame.locals import *
from resources import *


class Player(pygame.sprite.Sprite):
    """handle player's spaceship"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("black-arrow-cropped-resized.png")
        self.original = self.image
        self.area = pygame.display.get_surface().get_rect()
        self.rect.center = (self.area.width / 2, self.area.height / 2)
        self.vel = 0
        self.angle = 0
        self.ang_vel = 0

    def update(self):

        dx = math.cos(math.radians(self.angle)) * self.vel
        dy = -math.sin(math.radians(self.angle)) * self.vel

        self.angle += self.ang_vel
        self.image = pygame.transform.rotozoom(self.original, self.angle, 1)
        self.rect.move_ip(dx, dy)

        if self.rect.left < self.area.left:
            self.rect.left = self.area.left
        if self.rect.right > self.area.right:
            self.rect.right = self.area.right
        if self.rect.top < self.area.top:
            self.rect.top = self.area.top
        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom

    def _turn(self, value=6):
        self.ang_vel = value

    def _stop_turn(self):
        self.ang_vel = 0

    def _move(self, value=5):
        self.vel = value

    def _stop(self):
        self.vel = 0


class Asteroids(pygame.sprite.Sprite):
    """create and control asteroids"""

    def __init__(self, x_vel=0, y_vel=0, size=0, center=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("black-boulder-pixel-cropped.png")[0]
        self.area = pygame.display.get_surface().get_rect()
        if x_vel == 0:
            self.x_vel = randint(1, 3)
        else:
            self.x_vel = x_vel
        if y_vel == 0:
            self.y_vel = randint(1, 3)
        else:
            self.y_vel = y_vel
        self.angle = randint(0, 360)
        if size == 0:
            self.size = randint(1, 5) / 10
        else:
            self.size = size
        self.original = pygame.transform.rotozoom(self.image, self.angle, self.size)
        self.image = self.original
        self.rect = self.image.get_rect()
        if center == 0:
            self.rect.center = (choice((randint(-200, 0), randint(800, 1000))),
                                choice((randint(-200, 0), randint(600, 800))))
        else:
            self.rect.center = center
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = min(self.rect.width, self.rect.height) / 2

    def update(self):
        self.rect.move_ip(self.x_vel, self.y_vel)

        if self.rect.left < self.area.left - 300:
            self.rect.left = self.area.left - 300
            self.x_vel = -self.x_vel
        if self.rect.right > self.area.right + 300:
            self.rect.right = self.area.right + 300
            self.x_vel = -self.x_vel
        if self.rect.top < self.area.top - 300:
            self.rect.top = self.area.top - 300
            self.y_vel = -self.y_vel
        if self.rect.bottom > self.area.bottom + 300:
            self.rect.bottom = self.area.bottom + 300
            self.y_vel = -self.y_vel

    def _split(self):
        astA_vector = rotate_vector([self.x_vel, self.y_vel], 45)
        astB_vector = rotate_vector([self.x_vel, self.y_vel], -45)
        return Asteroids(astA_vector[0][0], astA_vector[1][0], self.size - 0.1, self.rect.center),\
               Asteroids(astB_vector[0][0], astB_vector[1][0], self.size - 0.1, self.rect.center)


class Bullets(pygame.sprite.Sprite):

    def __init__(self, pos, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = min(self.rect.width, self.rect.height)
        self.area = pygame.display.get_surface().get_rect()
        self.vel = 5
        self.rect.center = pos
        self.angle = angle
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1)

    def update(self):

        dx = math.cos(math.radians(self.angle)) * self.vel
        dy = -math.sin(math.radians(self.angle)) * self.vel
        self.rect.move_ip(dx, dy)
