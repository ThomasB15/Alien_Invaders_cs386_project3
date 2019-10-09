import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien
from ufo import UFO
from pygame.sprite import Group
from Barrier import Barrier
import threading


time_counter = 0
WHITE = [255, 255, 255]

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens"""
    available_space_y = (ai_settings.screen_height - (8 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    if row_number > 0 and row_number <= 2:
        #alien = BlueAlien(ai_settings, screen)
        alien.image = pygame.image.load('Blue Alien-1.png.png')
        alien.alien_color = "Blue"

    elif row_number > 2:
        #alien = YellowAlien(ai_settings, screen)
        alien.image = pygame.image.load('Yellow Alien-1.png.png')
        alien.alien_color = "Yellow"
    else:
        #alien = RedAlien(ai_settings, screen)
        alien.image = pygame.image.load('Red Alien-1.png.png')
        alien.alien_color = "Red"


    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_ufo(ai_settings, screen, ufos):
    ufo = UFO(ai_settings, screen)
    ufo_width = ufo.rect.width
    ufo.x = ufo_width + 2 * ufo_width
    ufo.rect.x = ufo.x
    ufo.rect.y = ufo.rect.height +2 * ufo.rect.height
    ufos.add(ufo)



def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # create an client and find the number of aliens in a row

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key presses"""
    if event.key == pygame.K_RIGHT:
        # move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def create_barriers():
    Barrier = Group()
    for row in range(4):
        for column in range(9):
            barriers = Barrier(10, WHITE, row, column)
            barriers.rect.x = 50 + (200 * 4) + (column * barriers.width)



def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game settings
        ai_settings.initialize_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # reset the scoreboard image
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty the list of aliens
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #create_barriers()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """update position of bullets and get rid of old bullets"""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def update_UFO(ai_settings, screen, stats, sb, ship, bullets, UFO):
    UFO.update()

    check_bullet_UFO_collision(ai_settings, screen, stats, sb, ship, bullets, UFO)

def check_bullet_UFO_collision(ai_settings, screen, stats, sb, ship, bullets, UFO):
    collision = pygame.sprite.groupcollide(bullets, UFO, True, False)

def alien_explosion(alien, counter, screen):
    if counter > 100:
        alien.image = pygame.image.load('Blue Alien-1.png.png')
        alien.blitme()
        counter = counter + 1
        alien_explosion(alien, counter, screen)
        print(counter)
    else:
        alien.kill()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check for any bullets that have hit aliens

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                if alien.check_color() == "Yellow" or alien.check_color() == "Yellow2":
                    stats.score += ai_settings.Yellow_alien_points * len(aliens)
                    counter = 0
                    alien_explosion(alien, counter, screen)
                    print("alien killed")

                    #sb.prep_score
                elif alien.check_color() == "Blue" or alien.check_color() == "Blue2":
                    stats.score += ai_settings.Blue_alien_points * len(aliens)
                    alien.kill()
                else:
                    stats.score += ai_settings.Red_alien_points * len(aliens)
                    alien.kill()

            #stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # if the entire fleet is destroyed start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    # create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        shoot = pygame.mixer.Sound('shoot.wav')
        shoot.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, high_score_button, ufos):
    """update images on the screen and flip to the new screen"""
    # redraw the screen
    screen.fill(ai_settings.bg_color)
    # redraw all bullets behind ship
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    ufos.draw(screen)
    # draw the score info
    sb.show_score()
    # draw the play button if the game is inactive
    if not stats.game_active:
        font = pygame.font.SysFont("Times New Roman", 20)
        TextSurf = font.render(" = 10 pts", True, WHITE)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((610), (200))
        screen.blit(TextSurf, TextRect)

        TextSurf2 = font.render(" = 20 pts", True, WHITE)
        TextRect2 = TextSurf2.get_rect()
        TextRect2.center = ((610), (250))
        screen.blit(TextSurf2, TextRect2)

        TextSurf3 = font.render(" = 40 pts", True, WHITE)
        TextRect3 = TextSurf2.get_rect()
        TextRect3.center = ((610), (300))
        screen.blit(TextSurf3, TextRect3)

        TextSurf4 = font.render(" = ?? pts", True, WHITE)
        TextRect4 = TextSurf2.get_rect()
        TextRect4.center = ((610), (350))
        screen.blit(TextSurf4, TextRect4)
        alienImage1 = pygame.image.load('Yellow Alien-1.png.png')
        alien1Rect = alienImage1.get_rect()
        alien1Rect.center = (560, 200)
        screen.blit(alienImage1, alien1Rect)

        alienImage2 = pygame.image.load('Blue Alien-1.png.png')
        alien2Rect = alienImage2.get_rect()
        alien2Rect.center = (560, 250)
        screen.blit(alienImage2, alien2Rect)

        alienImage3 = pygame.image.load('Red Alien-1.png.png')
        alien3Rect = alienImage3.get_rect()
        alien3Rect.center = (560, 300)
        screen.blit(alienImage3, alien3Rect)

        alienImage4 = pygame.image.load('UFO-1.png.png')
        alien4Rect = alienImage4.get_rect()
        alien4Rect.center = (560, 350)
        screen.blit(alienImage4, alien4Rect)

        high_score_button.hs_draw_button()
        play_button.draw_button()

    # make the most recently drawn screen
    pygame.display.flip()


def check_fleet_edges(ai_settings, aliens):
    """respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1



def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # decrement ships left
        stats.ships_left -= 1
        ship.image = pygame.image.load('Blue Alien-1.png.png')
        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # update the scoreboard
        sb.prep_ships()

        # create a new fleet
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        aliens.empty()
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings,  screen, stats, sb, ship, aliens, bullets):
    """check if any aliens have reached the bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings,  screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    global time_counter

    for alien in aliens.sprites():
        if alien.check_color() == "Red" and time_counter >= 10000:
            alien.image = pygame.image.load('Red Alien-2.png.png')
            alien.alien_color = "Red2"
            time_counter += 1
        elif alien.check_color() == "Red2" and time_counter > 0 and time_counter < 1000:
            alien.image = pygame.image.load('Red Alien-1.png.png')
            alien.alien_color = "Red"
            time_counter += 1
        elif alien.check_color() == "Blue" and time_counter >= 10000:
            alien.image = pygame.image.load('Blue Alien-2.png.png')
            alien.alien_color = "Blue2"
            time_counter += 1
        elif alien.check_color() == "Blue2" and time_counter > 0 and time_counter < 1000:
            alien.image = pygame.image.load('Blue Alien-1.png.png')
            alien.alien_color = "Blue"
            time_counter += 1
        elif alien.check_color() == "Yellow" and time_counter >= 10000:
            alien.image = pygame.image.load('Yellow Alien-2.png.png')
            alien.alien_color = "Yellow2"
            time_counter += 1
        elif alien.check_color() == "Yellow2" and time_counter > 0 and time_counter < 1000:
            alien.image = pygame.image.load('Yellow Alien-1.png.png')
            alien.alien_color = "Yellow"
            time_counter += 1
        elif alien.check_color() == "explode1":
            alien.image = pygame.image.load('Alien explosion-1.png.png')

        elif alien.check_color() == "explode2":
            alien.image = pygame.image.load('Alien explosion-2.png.png')

        elif alien.check_color() == "explode3":
            alien.image = pygame.image.load('Alien explosion-3.png.png')

        elif alien.check_color() == "explode4":
            alien.image = pygame.image.load('Alien explosion-4.png.png')
        else:
            time_counter += 1
        if time_counter >= 20000:
            time_counter = 0

    aliens.update()
    # look for alien ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

