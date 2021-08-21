import sys
import pygame

class GameObject:

    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > 600:
            self.pos.left = 0


def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    background = pygame.image.load("liquid.bmp").convert()
    background = pygame.transform.scale2x(background)
    background = pygame.transform.scale2x(background)
    screen.blit(background, (0, 0))

    player = pygame.image.load("player1.gif").convert()

    objects = []

    for i in range(10):
        obj = GameObject(player, 40 * i, i)
        objects.append(obj)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        for obj in objects:
            screen.blit(background, obj.pos, obj.pos)

        for obj in objects:
            obj.move()
            screen.blit(obj.image, obj.pos)

        pygame.display.update()
        pygame.time.delay(100)

if __name__ == '__main__':
    main()