import pygame
# from pygame.sprite import Sprite
from random import randint


class Stars():
    def __init__(self, ai_game):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        xloc = randint(0, self.setting.screen_width)
        yloc = randint(0, self.setting.screen_height)
        self.size = self.settings.star_size
        self.rect = pygame.Rect(xloc, yloc, self.size, self.size)

        for i in range(self.settings.no_stars + 1):
            pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

    # def _sprinkle_stars(self):
