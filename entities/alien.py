import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # ---Load alien image---
        self.image = pygame.image.load('./images/alien.bmp')
        self.rect = self.image.get_rect()

        # ---Start each new alien near the top of the screen---
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.coordinates = (0, 0)

        # ---Store the alien exact position---
        self.x = float(self.rect.x)

    # ---Check if alien reached the edge of the screen---
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    # ---Update aliens position---
    def update(self):
        # ---Move the alien right or left
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.coordinates = (self.rect.x, self.rect.y)
        # print("X: " + str(self.rect.x))
        # print("Y: " + str(self.rect.y))
        # print(self.coordinates)

    # ---Alien rendering---
    def blitme(self):
        self.screen.blit(self.image, self.rect)