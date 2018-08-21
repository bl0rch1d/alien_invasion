import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):

        # ---create a bullet obj at the ship current position---
        super().__init__(self, Bullet)
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship

        # ---create a bullet rect at (0, 0) and then set initial postion---
        self.rect = pygame.Rect(0, 0, self.ai_settings.bullet_width, self.ai_settings.bullet_height)
        self.rect.centerx = self.ship.rect.centerx
        self.rect.top = self.ship.rect.top

        # ---store the bullet's pos as a decimal point---
        self.y = float(self.rect.y)

        # ---bullet color and speed---
        self.color = self.ai_settings.bullet_color
        self.speed_factor = self.ai_settings.bullet_speed_factor
    
    def update(self):
        
        # ---bullet position update---
        self.y -= self.speed_factor
        # ---rect position update---
        self.rect.y = self.y
       
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
