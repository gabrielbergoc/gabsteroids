import sys

import pygame.mixer
import pygame_menu
from objects import *

# global variables
DEFAULT_ACCEL = 1
DEFAULT_VEL = 5
DEFAULT_ANG_VEL = 6
MAX_ASTEROID_N = 10
VOL_INCREMENT = 0.005
MAX_VOL = 0.3

# initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gabsteroids")
pygame.key.set_repeat(100)

menu_music = pygame.mixer.Sound("sounds/Asteroids - menu.wav")
menu_music.set_volume(MAX_VOL)
gameplay_music = pygame.mixer.Sound("sounds/Asteroids - Gameplay.wav")
gameplay_music.set_volume(0)
gameover_music = pygame.mixer.Sound("sounds/Asteroids - retry.wav")
gameover_music.set_volume(0)
asteroids_sounds = [pygame.mixer.Sound(f"sounds/Explosão {i}.wav") for i in range(1, 6)]
shooting_sound = pygame.mixer.Sound("sounds/tiro.wav")
shooting_sound.set_volume(MAX_VOL)
damage_sound = pygame.mixer.Sound("sounds/spawn.wav")

# main menu loop - calls game loop
def main():

    menu_music.play(-1)
    gameplay_music.play(-1)
    gameover_music.play(-1)

    menu = pygame_menu.Menu("Welcome to Gabsteroids", 800, 600)
    menu.add.button("Play", gameloop)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)

def gameloop():

    # initialize background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # initialize game objects
    player = Player()
    player_sprite = pygame.sprite.RenderUpdates(player)
    player_lives = pygame.sprite.RenderUpdates()
    for i in range(player.lives):
        player_lives.add(Heart((i * 38, 0)))

    asteroids_sprites = pygame.sprite.RenderUpdates(Asteroids())
    debris_sprites = pygame.sprite.RenderUpdates()

    bullets_sprites = pygame.sprite.RenderUpdates()

    scoreboard = Scoreboard()

    clock = pygame.time.Clock()
    spawn_intervals = 0     # keep track of time to create new asteroids
    music_volume = 0

    # game main loop
    while True:
        clock.tick_busy_loop(60)
        print(clock.get_fps())
        time_intervals = clock.get_time()
        spawn_intervals += time_intervals

        if music_volume < MAX_VOL:
            music_volume += VOL_INCREMENT
            gameplay_music.set_volume(music_volume)

        if player.immune > 0:
            player.immune -= time_intervals

        # create new asteroids every 2 seconds
        if spawn_intervals > 2000 and asteroids_sprites.__len__() < MAX_ASTEROID_N:
            asteroids_sprites.add(Asteroids())
            spawn_intervals = 0

        # event handling
        for event in pygame.event.get():
            # print(event)
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameplay_music.set_volume(0)
                return
            if event.type == KEYDOWN and event.key == K_UP:
                player._move(DEFAULT_VEL)
                # player._accel(DEFAULT_ACCEL)
            if event.type == KEYUP and event.key == K_UP:
                player._stop()
            # if event.type == KEYDOWN and event.key == K_DOWN:
                # player._accel(-DEFAULT_ACCEL)
            if event.type == KEYDOWN and event.key == K_LEFT:
                player._turn(DEFAULT_ANG_VEL)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player._turn(-DEFAULT_ANG_VEL)
            if event.type == KEYUP and event.key == K_LEFT:
                player._stop_turn()
            if event.type == KEYUP and event.key == K_RIGHT:
                player._stop_turn()
            if event.type == KEYDOWN and \
                    (event.key == K_c  or event.key == K_KP0):
                bullets_sprites.add(Bullets(player.rect.center, player.angle))
                shooting_sound.play()

        # collision checks
        for bullet in bullets_sprites.sprites():
            if not bullet.area.contains(bullet.rect):
                bullet.kill()   # get rid of bullets offscreen

            # check bullet-asteroids collisions
            for asteroid in asteroids_sprites.sprites():
                if pygame.sprite.collide_mask(bullet, asteroid):
                    asteroid_size = round(asteroid.size, 1)

                    # divide asteroids into two
                    if asteroid_size > 0.1:
                        new_asteroids = asteroid._split()
                        asteroids_sprites.add(new_asteroids)
                    else:
                        debris = asteroid._debris()
                        debris_sprites.add(debris)
                        debris_list = debris_sprites.sprites()
                        while len(debris_list) > 50:
                            debris_sprites.remove(debris_list[0])
                            debris_list = debris_sprites.sprites()

                    bullet.kill()
                    asteroid.kill()
                    asteroids_sounds[int(asteroid_size * 10 - 1)].play()
                    scoreboard.score += 1
                    scoreboard.update_score()

        # check player-asteroids collisions, break if True
        if pygame.sprite.spritecollide(player, asteroids_sprites, False, pygame.sprite.collide_mask) \
                and player.immune <= 0:
            player.lives -= 1
            player.immune = 2000
            damage_sound.play()

        if player.lives < 1:
            scoreboard.update_highscore()
            break

        # update everything
        dirty_rects = []
        screen.blit(background, (0, 0))
        player_sprite.update()
        dirty_rects += player_sprite.draw(screen)
        player_lives.empty()
        for i in range(player.lives):
            player_lives.add(Heart((i * 38, 0)))
        dirty_rects += player_lives.draw(screen)
        asteroids_sprites.update()
        dirty_rects += asteroids_sprites.draw(screen)
        debris_sprites.update()
        dirty_rects += debris_sprites.draw(screen)
        bullets_sprites.update()
        dirty_rects += bullets_sprites.draw(screen)
        screen.blit(scoreboard.surface, scoreboard.pos)
        pygame.display.update(dirty_rects)
        pygame.display.flip()

    # game over screen
    time_counter = 0
    while True:

        gameover_music.set_volume(MAX_VOL)

        clock.tick(60)
        time_counter += clock.get_time()

        if time_counter > 2000:
            for event in pygame.event.get():
                # print(event)
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    gameover_music.set_volume(0)
                    return
        if music_volume > 0:
            music_volume -= VOL_INCREMENT
            gameplay_music.set_volume(music_volume)

        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 40)
        text = font.render("GAME OVER", True, (0, 0, 0))
        text_pos = (background.get_width() / 2, background.get_height() / 2)
        text_rect = text.get_rect(centerx=text_pos[0], centery=text_pos[1])
        background.blit(text, text_rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()
