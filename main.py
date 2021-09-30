import sys
import os
import pygame.mixer
from player import Player
from asteroids import Asteroids
from scoreboard import Scoreboard
from heart import Heart
from gamesounds import GameSounds

# global variables
DEFAULT_VEL = 5
DEFAULT_ANG_VEL = 6
MAX_ASTEROID_N = 10
VOL_INCREMENT = 0.005
MAX_VOL = 0.2
CWD = os.getcwd()


def screen_init(caption=""):
    pygame.display.set_caption(caption)
    return pygame.display.set_mode((800, 600))


# initialize pygame and screen
pygame.init()
screen = screen_init()

# sounds
sounds = GameSounds()

# main menu loop - calls game loop
def main():

    background_blit(screen)

    while True:
        text_str = "Press Enter to start a new game or Esc to exit"
        text_font = pygame.font.Font(os.path.join(CWD, "fonts", "VT323-Regular.ttf"), 30)
        text_surf = text_font.render(text_str, True, (0,0,0))
        text_pos = (
            (screen.get_width() - text_surf.get_width()) / 2,
            (screen.get_height() - text_surf.get_height()) / 2
        )

        screen.blit(text_surf, text_pos)
        pygame.display.flip()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # keyboard handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return

        if keys[pygame.K_RETURN]:
            gameloop()


def gameloop():

    # initialize background
    background = background_blit(screen)

    # initialize game objects
    player = Player()
    player_sprite = pygame.sprite.RenderUpdates(player)
    player_lives = pygame.sprite.RenderUpdates()
    for i in range(player.get_lives()):
        player_lives.add(Heart((i * 38, 0)))

    asteroids_sprites = pygame.sprite.RenderUpdates(Asteroids())
    debris_sprites = pygame.sprite.RenderUpdates()
    bullets_sprites = pygame.sprite.RenderUpdates()

    scoreboard = Scoreboard()
    clock = pygame.time.Clock()

    spawn_intervals = 0     # keep track of time to create new asteroids
    music_volume = 0

    # game main loop
    while player.is_alive():

        clock.tick_busy_loop(60)
        time_delta = clock.get_time()
        spawn_intervals += time_delta

        if music_volume < MAX_VOL:
            music_volume += VOL_INCREMENT
            sounds.gameplay_music.set_volume(music_volume)

        player.decrease_immunity(time_delta)

        # create new asteroids every 2 seconds (if there's less than 10)
        if spawn_intervals > 2000 and asteroids_sprites.__len__() < MAX_ASTEROID_N:
            asteroids_sprites.add(Asteroids())
            spawn_intervals = 0

        # event handling
        event_handler(player, bullets_sprites, time_delta)

        # collision checks
        score = collision_bullet_asteroid(bullets_sprites, asteroids_sprites, debris_sprites)

        scoreboard.increment(score)
        scoreboard.update_score()

        collision_player_asteroid(player, asteroids_sprites)

        # update everything
        update_objects(
                background,
                player_sprite,
                player_lives,
                bullets_sprites,
                asteroids_sprites,
                debris_sprites,
                scoreboard
        )

    # game over screen
    time_counter = 0
    while True:

        sounds.gameover_music.set_volume(MAX_VOL)

        clock.tick(60)

        if time_counter < 1000:
            pygame.event.get()
            time_counter += clock.get_time()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    sounds.gameover_music.set_volume(0)
                    pygame.event.get()
                    return

        if music_volume > 0:
            music_volume -= VOL_INCREMENT
            sounds.gameplay_music.set_volume(music_volume)

        # GAME OVER text
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


def collision_bullet_asteroid(bullets, asteroids, debris):
    count = 0
    for bullet in bullets.sprites():

        # get rid of bullets offscreen
        bullet.kill_offscreen()

        # check for bullet-asteroids collisions
        for asteroid in asteroids.sprites():
            if pygame.sprite.collide_mask(bullet, asteroid):
                count += 1
                asteroid_size = round(asteroid.get_size(), 1)

                # divide asteroids into two
                if asteroid_size > 0.1:
                    new_asteroids = asteroid.split()
                    asteroids.add(new_asteroids)
                else:
                    debris_piece = asteroid.debris()
                    debris.add(debris_piece)

                    # delete debris sprites if there are more than 50
                    # to optimize a little bit
                    while debris.__len__() > 50:
                        debris_list = debris.sprites()
                        debris.remove(debris_list[0])

                bullet.kill()
                asteroid.kill()
                sounds.asteroids_sounds[int(asteroid_size * 10 - 1)].play()

    return count


def collision_player_asteroid(player, asteroids):
    if pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_mask) \
            and not player.is_immune():
        player.lose_lives(1)
        player.be_immune()
        sounds.damage_sound.play()


def update_objects(background, player, lives, bullets, asteroids, debris, scoreboard):

    dirty_rects = []

    screen.blit(background, (0, 0))

    player.update()
    dirty_rects += player.draw(screen)

    lives.empty()
    for i in range(player.sprites()[0].get_lives()):
        lives.add(Heart((i * 38, 0)))
    dirty_rects += lives.draw(screen)

    bullets.update()
    dirty_rects += bullets.draw(screen)

    asteroids.update()
    dirty_rects += asteroids.draw(screen)

    debris.update()
    dirty_rects += debris.draw(screen)

    scoreboard.update_highscore()
    screen.blit(scoreboard.get_surface(), scoreboard.get_pos())

    pygame.display.update(dirty_rects)
    pygame.display.flip()


def event_handler(player, bullets, time_delta):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # keyboard handling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        sounds.gameplay_music.set_volume(0)
        sys.exit()

    if keys[pygame.K_UP]:
        player.move(DEFAULT_VEL)
    else:
        player.stop()

    if keys[pygame.K_LEFT]:
        player.turn(DEFAULT_ANG_VEL)
    elif keys[pygame.K_RIGHT]:
        player.turn(-DEFAULT_ANG_VEL)

    if (keys[pygame.K_c] or keys[pygame.K_KP0]) and player.get_shoot_delay() <= 0:
        player.shoot(bullets)
        sounds.shooting_sound.play()
    else:
        player.decrease_shoot_delay(time_delta)


def background_blit(screen: pygame.Surface) -> pygame.Surface:
    # initialize background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    return background


if __name__ == '__main__':
    main()
