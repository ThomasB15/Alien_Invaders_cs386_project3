
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf
import time


def run_game():
    # initialize game
    pygame.init()

    ai_settings = Settings()
    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    clock = pygame.time.Clock()

    # make the play button
    play_button = Button(ai_settings, screen, "Play!")
    high_score_button = Button(ai_settings, screen, "High Score")

    # create an instance to store game stats and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # make a ship
    ship = Ship(ai_settings, screen)
    # make a group to store bullets, and a group of aliens
    bullets = Group()
    aliens = Group()
    ufos = Group()

    #add music
    pygame.mixer.music.load("spaceinvaders1.mpeg")
    pygame.mixer.music.play(-1, 0.0)
    # create the fleet of aliens
    #gf.create_fleet(ai_settings, screen, ship, aliens)
    loop = False
    # start the main loop
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_UFO(ai_settings, screen, stats, sb, ship, bullets, ufos)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, high_score_button, ufos)


run_game()
