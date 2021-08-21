import os
import sys
import pygame
from pygame.locals import *
from functions import *
from objects import *


def main():
    pygame.init()

    screen = pygame.display.set_mode((468, 60))
    pygame.display.set_caption("Monkey Fever")
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((250, 250, 250))

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Pummel The Chimp And Win $$$", True, (10, 10, 10))
        text_pos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, text_pos)
    else:
        print("Warning! Fonts disabled")

    screen.blit(background, (0, 0))
    pygame.display.flip()

    if not pygame.mixer:
        print("Warning! Sounds disabled")

    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")

    chimp = Chimp()
    fist = Fist()
    all_sprites = pygame.sprite.RenderPlain((fist, chimp))

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()
                    chimp.punched()
                else:
                    whiff_sound.play()
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        all_sprites.update()

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()