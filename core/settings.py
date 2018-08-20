from random import randint

class Settings():
    def __init__(self):
        # ---Static settings---
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # ---Ship settings---
        self.ship_limit = 3

        # ---Bullet settings---
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # ---Alien settings---
        self.fleet_drop_speed = 10

        # ---Powerup settings---
        self.powerup_probability_range = 95
        self.current_time = 0
        self.mega_bullet_active = False
        self.super_sonic_bullets_active = False
        self.alien_freezing_active = False
        self.additional_ship_active = False



        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        # ---fleet direction of 1 represents right, of -1 left.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
        
    