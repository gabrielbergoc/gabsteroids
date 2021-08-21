import pygame
from pygame.locals import *
from functions import *


class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image("fist.bmp", -1)
        self.punching = False

    def update(self):
        """move the fist based on mouse position"""

        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        """returns true if the fist collides with target"""

        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)

            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """called to pull the fist back"""

        self.punching = False


class Chimp(pygame.sprite.Sprite):
    """moves a monkey across the screen and spins it if hit"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image("chimp.bmp", -1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (10, 10)
        self.move = 9
        self.dizzy = 0

    def update(self):
        """walk or spin, depending on the monkey's state"""

        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move monkey across the screen"""

        new_pos = self.rect.move((self.move, 0))

        if not self.area.contains(new_pos):
            if self.rect.left < self.area.left \
                    or self.rect.right > self.area.right:
                self.move = -self.move
                new_pos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = new_pos

    def _spin(self):
        """spin the chimp image"""
        center = self.rect.center
        self.dizzy += 12

        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, self.dizzy)

        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """cause monkey to start spinning"""

        if not self.dizzy:
            self.dizzy = 1
