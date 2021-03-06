import sys
import pygame.mixer
from objects import *

# global variables
DEFAULT_ACCEL = 1
DEFAULT_VEL = 5
DEFAULT_BULLET_VEL = 10
DEFAULT_ANG_VEL = 6
MAX_ASTEROID_N = 10
VOL_INCREMENT = 0.005
MAX_VOL = 0.2
CWD = os.getcwd()

# initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gabsteroids")

# sounds
menu_music = pygame.mixer.Sound(os.path.join(CWD, "sounds", "Asteroids - menu.wav"))
menu_music.set_volume(MAX_VOL)
gameplay_music = pygame.mixer.Sound(os.path.join(CWD, "sounds", "Asteroids - Gameplay.wav"))
gameplay_music.set_volume(0)
gameover_music = pygame.mixer.Sound(os.path.join(CWD, "sounds", "Asteroids - retry.wav"))
gameover_music.set_volume(0)
asteroids_sounds = []
for i in range(1, 6):
    asteroids_sounds.append(pygame.mixer.Sound(os.path.join(CWD, "sounds", f"Explosao {i}.wav")))
shooting_sound = pygame.mixer.Sound(os.path.join(CWD, "sounds", "tiro.wav"))
shooting_sound.set_volume(MAX_VOL)
damage_sound = pygame.mixer.Sound(os.path.join(CWD, "sounds", "spawn.wav"))

# main menu loop - calls game loop
def main():

    menu_music.play(-1)
    gameplay_music.play(-1)
    gameover_music.play(-1)

    # initialize background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        text_str = "Press Enter to start a new game or Esc to exit"
        text_font = pygame.font.Font(os.path.join(CWD, "fonts", "VT323-Regular.ttf"), 30)
        text_surf = text_font.render(text_str, True, (0,0,0))
        text_pos = ((screen.get_width() - text_surf.get_width()) / 2, (screen.get_height() - text_surf.get_height()) / 2)

        screen.blit(text_surf, text_pos)
        pygame.display.flip()

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        # keyboard handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            gameplay_music.set_volume(0)
            return

        if keys[pygame.K_RETURN]:
            gameloop()

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
    shoot_delay = 0
    music_volume = 0

    # game main loop
    while True:
        clock.tick_busy_loop(60)
        time_intervals = clock.get_time()
        spawn_intervals += time_intervals

        if music_volume < MAX_VOL:
            music_volume += VOL_INCREMENT
            gameplay_music.set_volume(music_volume)

        if player.immune > 0:
            player.immune -= time_intervals

        # create new asteroids every 2 seconds (if there's less than 10)
        if spawn_intervals > 2000 and asteroids_sprites.__len__() < MAX_ASTEROID_N:
            asteroids_sprites.add(Asteroids())
            spawn_intervals = 0

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        # keyboard handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            gameplay_music.set_volume(0)
            return

        if keys[pygame.K_UP]:
            player.move(DEFAULT_VEL)
            # player.accel(DEFAULT_ACCEL)   # realistic movement
        else:
            player.stop()

        if keys[pygame.K_LEFT]:
            player.turn(DEFAULT_ANG_VEL)
        elif keys[pygame.K_RIGHT]:
            player.turn(-DEFAULT_ANG_VEL)
        else:
            player.stop_turn()

        if (keys[pygame.K_c] or keys[pygame.K_KP0]) and shoot_delay <= 0:
            bullets_sprites.add(Bullets(player.nose, player.angle, DEFAULT_BULLET_VEL))
            shooting_sound.play()
            shoot_delay = 500
        else:
            shoot_delay -= time_intervals

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
                        new_asteroids = asteroid.split()
                        asteroids_sprites.add(new_asteroids)
                    else:
                        debris = asteroid.debris()
                        debris_sprites.add(debris)

                        # delete debris sprites if there are more than 50
                        # to optimize a little bit
                        while debris_sprites.__len__() > 50:
                            debris_list = debris_sprites.sprites()
                            debris_sprites.remove(debris_list[0])

                    bullet.kill()
                    asteroid.kill()
                    asteroids_sounds[int(asteroid_size * 10 - 1)].play()
                    scoreboard.score += 1
                    scoreboard.update_score()

        # check player-asteroids collisions
        if pygame.sprite.spritecollide(player, asteroids_sprites, False, pygame.sprite.collide_mask) \
                and player.immune <= 0:
            player.lives -= 1
            player.immune = 2000
            damage_sound.play()

        # end game if there are no lives left
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

        if time_counter > 1000:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    gameover_music.set_volume(0)
                    pygame.event.get()
                    return
        else:
            pygame.event.get()

        if music_volume > 0:
            music_volume -= VOL_INCREMENT
            gameplay_music.set_volume(music_volume)

        # GAME OVER
        screen.blit(background, (0, 0))
        gameover_font = pygame.font.Font(os.path.join(CWD, "fonts", "VT323-Regular.ttf"), 40)
        gameover_surf = gameover_font.render("GAME OVER", True, (0, 0, 0))
        gameover_pos = (
            (background.get_width() - gameover_surf.get_width()) / 2,
            (background.get_height() - gameover_surf.get_height()) / 2
        )
        background.blit(gameover_surf, gameover_pos)

        # play again/exit text
        text_str = "Press Enter to start a new game or Esc to exit"
        text_font = pygame.font.Font(os.path.join(CWD, "fonts", "VT323-Regular.ttf"), 30)
        text_surf = text_font.render(text_str, True, (0, 0, 0))
        text_pos = (
            (screen.get_width() - text_surf.get_width()) / 2,
            (screen.get_height() + text_surf.get_height()) / 2
        )
        background.blit(text_surf, text_pos)

        pygame.display.flip()


if __name__ == '__main__':
    main()
