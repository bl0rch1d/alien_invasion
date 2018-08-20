import sys
import pygame
from pygame.sprite import Group

from core.settings import Settings
from core.game_stats import GameStats
from entities.button import Button
from entities.ship import Ship
from entities.alien import Alien
from core.scoreboard import Scoreboard
from entities.powerup import PowerUp
import core.game_functions as gf


def run_game():

    # ---initializing---
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((
        ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # ---Make the Play button---
    play_button = Button(ai_settings, screen, "Play")

    # ---instances loading---
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    powerups = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    # ---start---
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        
        if stats.game_active:
            ship.update()
            powerups.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, powerups)
            gf.check_powerup_collisions(ai_settings, screen, ship, powerups, bullets, sb, stats)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        
        gf.screen_update(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, powerups)



run_game()
