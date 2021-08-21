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

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("black-boulder-pixel-cropped.png")
        self.area = pygame.display.get_surface().get_rect()
        self.rect.center = (choice((randint(-200, 0), randint(800, 1000))), choice((randint(-200, 0), randint(600, 800))))
        self.x_vel = randint(1, 4)
        self.y_vel = randint(1, 4)
        self.angle = randint(0, 360)
        self.size = randint(1, 5)
        self.original = pygame.transform.rotozoom(self.image, self.angle, self.size / 10)
        self.image = self.original

    def update(self):
        self.rect.move_ip(self.x_vel, self.y_vel)

        if self.rect.left < self.area.left - 500:
            self.rect.left = self.area.left - 500
            self.x_vel = -self.x_vel
        if self.rect.right > self.area.right + 500:
            self.rect.right = self.area.right + 500
            self.x_vel = -self.x_vel
        if self.rect.top < self.area.top - 500:
            self.rect.top = self.area.top - 500
            self.y_vel = -self.y_vel
        if self.rect.bottom > self.area.bottom + 500:
            self.rect.bottom = self.area.bottom + 500
            self.y_vel = -self.y_vel


class Bullets(pygame.sprite.Sprite):

    def __init__(self, pos, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet.png")
        self.area = pygame.display.get_surface().get_rect()
        self.vel = 5
        self.rect.center = pos
        self.angle = angle
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1)

    def update(self):

        dx = math.cos(math.radians(self.angle)) * self.vel
        dy = -math.sin(math.radians(self.angle)) * self.vel
        self.rect.move_ip(dx, dy)
