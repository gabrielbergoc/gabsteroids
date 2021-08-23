import math
from random import randint, choice

import pygame.sprite

from resources import *

immunity_intervals = [125 * i for i in range(1, 17)]
max_vel = 10


class Player(pygame.sprite.Sprite):
    """handle player's spaceship"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("images/black-arrow-cropped-resized.png")
        self.original = self.image
        self.transparent = load_image("images/transparent-arrow.png")[0]
        self.radius = 14
        self.area = pygame.display.get_surface().get_rect()
        self.rect.center = (self.area.width / 2, self.area.height / 2)
        self.vel = 0
        self.x_momentum = 0
        self.y_momentum = 0
        self.angle = 0
        self.ang_vel = 0
        self.lives = 3
        self.immune = 0

    def update(self):
        """moves player and maintains it onscreen"""

        self.angle += self.ang_vel
        self.rect.move_ip(self.x_momentum, self.y_momentum)

        if self.rect.left < self.area.left:
            self.rect.left = self.area.left
        if self.rect.right > self.area.right:
            self.rect.right = self.area.right
        if self.rect.top < self.area.top:
            self.rect.top = self.area.top
        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom

        for i in range(0, len(immunity_intervals), 2):
            if immunity_intervals[i] < self.immune <= immunity_intervals[i + 1] :
                self.image = self.transparent
                break
            else:
                self.image = pygame.transform.rotozoom(self.original, self.angle, 1)

    def _turn(self, value=6):
        self.ang_vel = value

    def _stop_turn(self):
        self.ang_vel = 0

    def _accel(self, value=5):
        self.x_momentum += math.cos(math.radians(self.angle)) * value
        if self.x_momentum > max_vel:
            self.x_momentum = max_vel

        self.y_momentum += -math.sin(math.radians(self.angle)) * value
        if self.y_momentum > max_vel:
            self.y_momentum = max_vel


class Asteroids(pygame.sprite.Sprite):
    """create and control asteroids"""

    def __init__(self, x_vel=0, y_vel=0, size=0, center=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/black-boulder-pixel-cropped.png")[0]
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
        self.radius = min(self.rect.width, self.rect.height) / 2

    def update(self):
        """moves asteroid and bounces it 300 pixels offscreen"""

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

    # splits asteroid into two new smaller asteroids
    def _split(self):
        astA_vector = rotate_vector([self.x_vel, self.y_vel], 45)
        astB_vector = rotate_vector([self.x_vel, self.y_vel], -45)
        return Asteroids(astA_vector[0][0], astA_vector[1][0], self.size - 0.1, self.rect.center),\
            Asteroids(astB_vector[0][0], astB_vector[1][0], self.size - 0.1, self.rect.center)

    def _debris(self):
        astA_vector = rotate_vector([self.x_vel, self.y_vel], 45)
        astB_vector = rotate_vector([self.x_vel, self.y_vel], -45)
        return Asteroids(astA_vector[0][0], astA_vector[1][0], self.size - 0.09, self.rect.center),\
            Asteroids(astB_vector[0][0], astB_vector[1][0], self.size - 0.09, self.rect.center)


class Bullets(pygame.sprite.Sprite):
    """handle bullets"""

    def __init__(self, pos, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("images/bullet.png")
        self.radius = min(self.rect.width, self.rect.height)
        self.area = pygame.display.get_surface().get_rect()
        self.vel = 5
        self.rect.center = pos
        self.angle = angle
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1)

    def update(self):
        """moves bullet"""

        dx = math.cos(math.radians(self.angle)) * self.vel
        dy = -math.sin(math.radians(self.angle)) * self.vel
        self.rect.move_ip(dx, dy)


class Scoreboard:
    """handle score and highscore"""

    def __init__(self):
        self.score = 0
        self.highscore = self.get_highscore()
        self.font_obj = pygame.font.Font(None, 30)
        self.text = f"Score: 0 Highscore: {self.highscore}"
        self.surface = self.font_obj.render(self.text, True, (0, 0, 0))
        self.area = pygame.display.get_surface().get_rect()
        self.pos = (self.area.midtop[0] - self.surface.get_width() / 2, self.area.midtop[1])

    def update_score(self):
        """updates rendered text"""

        self.text = f"Score: {self.score} Highscore: {self.highscore}"
        self.surface = self.font_obj.render(self.text, True, (0, 0, 0))

    def update_highscore(self):
        """updates highscore and saves it to file"""

        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore()

    def get_highscore(self):
        """get highscore from file, creates file if inexistent"""

        if "highscore.txt" in os.listdir():
            with open("highscore.txt", mode="r") as file:
                score = file.read()
                score = score.strip()

            return int(score)

        else:
            return 0

    def save_highscore(self):
        """saves highscore to file"""

        with open("highscore.txt", mode="w") as file:
            file.write(str(self.highscore))


class Heart(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/black-heart.jpg", -1)[0]
        self.image = pygame.transform.scale(self.image, (38, 35))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
