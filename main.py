import os
import sys
import pygame
from random import randint
from pygame.locals import *
from objects import *

default_vel = 5
default_ang_vel = 6
max_asteroid_n = 10

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gabsteroids")
    pygame.key.set_repeat(100)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))

    player = Player()
    player_sprite = pygame.sprite.RenderPlain(player)

    asteroids_sprites = pygame.sprite.RenderPlain(Asteroids())

    bullets_sprites = pygame.sprite.RenderPlain()

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    time_intervals = 0

    while True:
        clock.tick(60)
        time_intervals += clock.get_time()

        if time_intervals > 2000 and len(asteroids_sprites.sprites()) < max_asteroid_n:
            asteroids_sprites.add(Asteroids())
            time_intervals = 0

        for event in pygame.event.get():
            print(event)
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and event.key == K_UP:
                player._move(default_vel)
            if event.type == KEYUP and event.key == K_UP:
                player._stop()
            if event.type == KEYDOWN and event.key == K_LEFT:
                player._turn(default_ang_vel)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player._turn(-default_ang_vel)
            if event.type == KEYUP and event.key == K_LEFT:
                player._stop_turn()
            if event.type == KEYUP and event.key == K_RIGHT:
                player._stop_turn()
            if event.type == KEYDOWN and event.key == K_c:
                bullets_sprites.add(Bullets(player.rect.center, player.angle))

        screen.blit(background, (0, 0))
        player_sprite.update()
        player_sprite.draw(screen)
        asteroids_sprites.update()
        asteroids_sprites.draw(screen)
        bullets_sprites.update()
        bullets_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()