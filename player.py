import math
import pygame.sprite
from resources import *
from stats import Stats

DEFAULT_IMMUNE_TIME = 2000
IMMUNITY_INTERVALS = [125 * i for i in range(1, DEFAULT_IMMUNE_TIME // 125 + 1)]
MAX_VEL = 10
CWD = os.getcwd()


class Player(pygame.sprite.Sprite):
    """handle player's spaceship"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(os.path.join(CWD, "images", "rsz_2black-arrow.png"))
        self.original = self.image
        self.transparent = load_image(os.path.join(CWD, "images", "transparent-arrow.png"))[0]
        self.area = pygame.display.get_surface().get_rect()
        self.rect.center = (self.area.width / 2, self.area.height / 2)
        self.radius = self.image.get_width() / 2
        self.nose = self.rect.midright
        self.__stats = Stats()

    def update(self):
        """moves player and maintains it onscreen"""

        self.rect.move_ip(self.__get_deltas())
        self.__check_boundaries()
        self.__turn_nose()
        self.__sprite_update()

    def __sprite_update(self):
        for i in range(0, len(IMMUNITY_INTERVALS), 2):
            if IMMUNITY_INTERVALS[i] < self.__stats.immune_for <= IMMUNITY_INTERVALS[i + 1]:
                self.image = self.transparent
                break
            else:
                self.image = pygame.transform.rotozoom(self.original, self.__stats.angle, 1)
                self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, value=5):
        self.__stats.vel = value

    def stop(self):
        self.__stats.vel = 0

    def turn(self, value=6):
        self.__stats.angle += value
        self.__turn_nose()

    def __turn_nose(self):
        nose_dx = math.cos(math.radians(self.__stats.angle)) * self.radius
        nose_dy = -math.sin(math.radians(self.__stats.angle)) * self.radius
        self.nose = tuple(map(lambda x, y: x + y, (nose_dx, nose_dy), self.rect.center))
        # the minus in -sin is because the y coordinate increases downwards

    def __check_boundaries(self):

        if self.rect.left < self.area.left:
            self.rect.left = self.area.left

        if self.rect.right > self.area.right:
            self.rect.right = self.area.right

        if self.rect.top < self.area.top:
            self.rect.top = self.area.top

        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom

    def __get_deltas(self):
        dx = math.cos(math.radians(self.__stats.angle)) * self.__stats.vel
        dy = -math.sin(math.radians(self.__stats.angle)) * self.__stats.vel
        # the minus in -sin is because the y coordinate increases downwards

        return dx, dy

    def get_lives(self):
        return self.__stats.lives

    def lose_lives(self, n=1):
        self.__stats.lives -= n

    def get_nose(self):
        return self.nose

    def get_angle(self):
        return self.__stats.angle

    def be_immune(self):
        self.__stats.immune_for = DEFAULT_IMMUNE_TIME

    def is_immune(self):
        return True if self.__stats.immune_for > 0 else False

    def decrease_immunity(self, time: float):
        if self.__stats.immune_for > 0:
            self.__stats.immune_for -= time

    def get_shoot_delay(self):
        return self.__stats.shoot_delay

    def set_shoot_delay(self, delay=500):
        self.__stats.shoot_delay = delay

    def decrease_shoot_delay(self, time: float):
        if self.__stats.shoot_delay > 0:
            self.__stats.shoot_delay -= time

    def is_alive(self):
        return True if self.__stats.lives > 0 else False
