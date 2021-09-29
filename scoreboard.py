import pygame.sprite
from resources import *

CWD = os.getcwd()


def get_highscore():
    """get highscore from file, creates file if inexistent"""

    if "highscore.txt" in os.listdir():
        with open("highscore.txt", mode="r") as file:
            score = file.read()
            score = score.strip()

        return int(score)

    else:
        return 0


class Scoreboard:
    """handle score and highscore"""

    def __init__(self):
        self.__score = 0
        self.__highscore = get_highscore()
        self.__font_obj = pygame.font.Font(os.path.join(CWD, "fonts", "VT323-Regular.ttf"), 30)
        self.__text = f"Score: 0 Highscore: {self.__highscore}"
        self.__surface = self.__font_obj.render(self.__text, True, (0, 0, 0))
        self.__area = pygame.display.get_surface().get_rect()
        self.__pos = (self.__area.midtop[0] - self.__surface.get_width() / 2, self.__area.midtop[1])

    def increment(self, n=1):
        self.__score += n

    def update_score(self):
        """updates rendered __text"""

        self.__text = f"Score: {self.__score} Highscore: {self.__highscore}"
        self.__surface = self.__font_obj.render(self.__text, True, (0, 0, 0))

    def update_highscore(self):
        """updates __highscore and saves it to file"""

        if self.__score > self.__highscore:
            self.__highscore = self.__score
            self.save_highscore()

    def save_highscore(self):
        """saves __highscore to file"""

        with open("highscore.txt", mode="w") as file:
            file.write(str(self.__highscore))

    def get_surface(self):
        return self.__surface

    def get_pos(self):
        return self.__pos
