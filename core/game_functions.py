import sys
from time import sleep
import time
from random import randint
import pygame
from entities.bullet import Bullet
from entities.alien import Alien
from entities.powerup import PowerUp
# from bullet import Bullet
# from alien import Alien
# from powerup import PowerUp
import sched


# ---KeyDown events check---
def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
       fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # if event.key == pygame.K_r:
    #     ai_settings.game_active = False
    #     sleep(0.5)
    #     start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

# ---Bullets firing and quantity limitation---
def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

# ---KeyUp events check---
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

# ---Game event listener---
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # ---Event listener---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # ---Mouse events---
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        # ---KeyDown event---
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)

        # ---KeyUp event---
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)         

# ---Play button appearance condition---
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # ---Start a new game when the player clicks Play---
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
       start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

# ---Start game conditions---
def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ai_settings.initialize_dynamic_settings()

     # ---Hide mouse cursor---
    pygame.mouse.set_visible(False)

    # ---Reset game stats---
    stats.reset_stats()
    stats.game_active = True

    # ---Reset the scoreboard images---
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # ---Empty the list of aliens and bullets---
    aliens.empty()
    bullets.empty()

    # ---Create a new fleet and center the ship---
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

# ---Calculate the number of aliens which can be fit in a row on the screen---
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

# ---Calculate the number of alien rows which can be fit on the screen---
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

# ---Alien creation---
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    # print(alien.coordinates)
    # print(alien.x)
    # print("X: " + str(alien.rect.x))
    # print("Y: " + str(alien.rect.y))

# ---Fleet creation---
def create_fleet(ai_settings, screen, ship, aliens):
    # ---Create an alien to find a number of aliens in a row---
    # ---Spacing between each alien is equal to one alien width---
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # number_rows = 2
    
    # ---Create the fleet of aliens---
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
# ---Frame update---
def screen_update(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, powerups):
    screen.fill(ai_settings.bg_color)

    # ---Redraw all bullets behind ship and aliens---
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    powerups.draw(screen)

    #---Draw the play button if the game is inactive---
    if not stats.game_active:
        play_button.draw_button() 

    pygame.display.flip()

# ---Bullets state update---
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, powerups):
    # ---update bullet positions---
    bullets.update()

    # ---deleting bullets when they reach the top of the screen---
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, powerups)
    
# ---ALien-Bullet collision condition check---
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, powerups):
    # ---Check for any bullets that have hit aliens---
    # if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            for alien in aliens:
                create_powerup(ai_settings, screen, powerups, alien)
                # print(alien.coordinates)
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # ---Destroy existing bullets and create a new fleet---
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        ai_settings.powerup_probability_range -= 1
        create_fleet(ai_settings, screen, ship, aliens)

# ---Fleet edge of the screen collision check---
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

# ---Fleet direction changing on reaching the edge of the screen---
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

# ---Actions which runs after ship hit---
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        # ---Decrement ships left---
        stats.ships_left -= 1

        # ---Update scoreboard---
        sb.prep_ships()

        # ---Empty the list of aliens and bullets---
        aliens.empty()
        bullets.empty()

        # ---Create a new fleet and center the ship---
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # ---Pause---
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

# ---If alien reach the bottom of the screen  - ship_hit()---
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

# ---Aliens state update on collision condition---
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # ---Check if the fleet is at an edge, and then update the positions of all aliens in the fleet---
    check_fleet_edges(ai_settings, aliens)
    # ---Update the position of all aliens in the fleet---
    
    aliens.update()
    
    # ---Look for alien-ship collisions---
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # --Look for alien hitting the bottom of the screen---
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def create_powerup(ai_settings, screen, powerups, alien):
    powerup_probability_factor = randint(0, 101)
    alienX = alien.coordinates[0]
    alienY = alien.coordinates[1]
    if powerup_probability_factor > ai_settings.powerup_probability_range:
        powerup = PowerUp(ai_settings, screen, alienX, alienY)
        print("Powerup probability factor = " + str(powerup_probability_factor))
        powerups.add(powerup)


def check_powerup_collisions(ai_settings, screen, ship, powerups, bullets, sb, stats):
    rect_x = list(range(ship.rect.x + 60))
    rect_right_x = ship.rect.x + 60
    rect_hitbox = rect_x[ship.rect.x:rect_right_x]
    for powerup in powerups:
        if powerup.rect.bottom >= ship.rect.top:
            if powerup.rect.x in rect_hitbox:
                
                # ---Powerup type initialization---
                powerup_type_factor = randint(0, 101)
                print("Powerup type factor = " + str(powerup_type_factor))
                if powerup_type_factor < 25:
                    ai_settings.mega_bullet_active = True
                    print("Mega Bullet")
                elif powerup_type_factor < 50:
                    ai_settings.super_sonic_bullets_active = True
                    print("Sonic bullets")
                elif powerup_type_factor < 75:
                    ai_settings.alien_freezing_active = True
                    print("Alien freezing")
                elif powerup_type_factor < 100:
                    ai_settings.additional_ship_active = True
                    print("Additional ship")

                ai_settings.current_time = time.time()
                ai_settings.current_time = int(ai_settings.current_time)

                powerups.remove(powerup)

        if powerup.rect.bottom >= ship.screen_rect.bottom:
            powerups.remove(powerup)
            print("Out of screen!")


    # ---Mega Bullet---
    if ai_settings.mega_bullet_active and int(time.time()) < ai_settings.current_time + 3:
        ai_settings.bullet_width = 300
        # print("Test")
    else:
       ai_settings.mega_bullet_active = False
       ai_settings.bullet_width = 3

    # ---Super Sonic bullets---
    if ai_settings.super_sonic_bullets_active and int(time.time()) < ai_settings.current_time + 3:
        ai_settings.bullet_speed_factor = 4
        ai_settings.bullets_allowed = 20
    else:
        ai_settings.super_sonic_bullets_active = False
        ai_settings.bullet_speed_factor = 1
        ai_settings.bullets_allowed = 10

    # ---Aliens freezing---
    if ai_settings.alien_freezing_active and int(time.time()) < ai_settings.current_time + 4:
        ai_settings.alien_speed_factor = 0
    else:
        ai_settings.alien_freezing_active = False
        ai_settings.alien_speed_factor = 1
    
    # ---Additional ship---
    if ai_settings.additional_ship_active:
        if stats.ships_left < 8:
            stats.ships_left += 1
            print("Ship limit: " + str(stats.ships_left))
            sb.prep_ships()
        else:
            print("You reached the maximum of ships limit!")
        ai_settings.additional_ship_active = False





