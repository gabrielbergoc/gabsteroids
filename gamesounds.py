import os
from pygame.mixer import Sound

MAX_VOL = 0.2
CWD = os.getcwd()


class GameSounds:

    def __init__(self):

        self.menu_music = Sound(os.path.join(CWD, "sounds", "Asteroids - menu.wav"))
        self.menu_music.set_volume(MAX_VOL)
        self.menu_music.play(-1)

        self.gameplay_music = Sound(os.path.join(CWD, "sounds", "Asteroids - Gameplay.wav"))
        self.gameplay_music.set_volume(0)
        self.gameplay_music.play(-1)

        self.gameover_music = Sound(os.path.join(CWD, "sounds", "Asteroids - retry.wav"))
        self.gameover_music.set_volume(0)
        self.gameover_music.play(-1)

        self.asteroids_sounds = []
        for i in range(1, 6):
            self.asteroids_sounds.append(Sound(os.path.join(CWD, "sounds", f"Explosao {i}.wav")))

        self.shooting_sound = Sound(os.path.join(CWD, "sounds", "tiro.wav"))
        self.shooting_sound.set_volume(MAX_VOL)

        self.damage_sound = Sound(os.path.join(CWD, "sounds", "spawn.wav"))
