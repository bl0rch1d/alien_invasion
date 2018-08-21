import pygame
from pygame.sprite import Sprite
from random import randint

class PowerUp(Sprite):
    def __init__(self, ai_settings, screen, alienX, alienY):
        super(PowerUp, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load('./images/star24x.png')
        self.rect = self.image.get_rect()
        
        self.rect.x = alienX
        self.rect.y = alienY

        self.speed_factor = 0.5
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

