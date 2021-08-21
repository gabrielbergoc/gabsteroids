import os
import sys
import pygame
import pygame_menu
from random import randint
from pygame.locals import *
from objects import *

default_vel = 5
default_ang_vel = 6
max_asteroid_n = 10

pygame.init()
screen = pygame.display.set_mode((800, 600))

def main():

    menu = pygame_menu.Menu("Welcome to Gabsteroids", 800, 600)
    menu.add.button("Play", gameloop)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)

def gameloop():
    pygame.display.set_caption("Gabsteroids")
    pygame.key.set_repeat(100)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))

    player = Player()
    player_sprite = pygame.sprite.RenderPlain(player)

    asteroids_sprites = pygame.sprite.RenderPlain(Asteroids())
    debris_sprites = pygame.sprite.RenderPlain()

    bullets_sprites = pygame.sprite.RenderPlain()

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    time_intervals = 0

    while True:
        clock.tick(60)
        time_intervals += clock.get_time()

        if time_intervals > 2000 and asteroids_sprites.__len__() < max_asteroid_n:
            asteroids_sprites.add(Asteroids())
            time_intervals = 0

        for event in pygame.event.get():
            # print(event)
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
            if event.type == KEYDOWN and \
                    (event.key == K_c  or event.key == K_KP0):
                bullets_sprites.add(Bullets(player.rect.center, player.angle))

        for bullet in bullets_sprites.sprites():
            if not bullet.area.contains(bullet.rect):
                bullet.kill()

            for asteroid in asteroids_sprites.sprites():
                if pygame.sprite.collide_mask(bullet, asteroid):
                    if asteroid.size > 0.1:
                        new_asteroids = asteroid._split()
                        if new_asteroids[0].size < 0.1:
                            debris_sprites.add(new_asteroids)
                        else:
                            asteroids_sprites.add(new_asteroids)
                    bullet.kill()
                    asteroid.kill()
        if pygame.sprite.spritecollide(player, asteroids_sprites, True):
            break

        screen.blit(background, (0, 0))
        player_sprite.update()
        player_sprite.draw(screen)
        asteroids_sprites.update()
        asteroids_sprites.draw(screen)
        debris_sprites.update()
        debris_sprites.draw(screen)
        bullets_sprites.update()
        bullets_sprites.draw(screen)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                return

        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 40)
        text = font.render("GAME OVER", True, (0, 0, 0))
        text_pos = (background.get_width() / 2, background.get_height() / 2)
        text_rect = text.get_rect(centerx=text_pos[0], centery=text_pos[1])
        background.blit(text, text_rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()
