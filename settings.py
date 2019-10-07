class Settings:

    def __init__(self):
        """initialize the game's static settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # ship settings
        self. ship_speed_factor = 1.5
        self.ship_limit = 3

        # bullet settings

        self.bullet_speed_factor = 3
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = 84, 242, 9
        self.bullets_allowed = 25

        # alien settings
        self.fleet_drop_speed = 10
        # Values are set in later functions
        self.alien_speed_factor = None
        self.fleet_direction = None
        self.alien_points = None
        self.Yellow_alien_points = None
        self.Blue_alien_points = None
        self.Red_alien_points = None

        # how quickly the game speeds up
        self.speed_scale = 1.1
        # how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5

        self.fleet_direction = 1

        # scoring
        self.alien_points = 50
        self.Yellow_alien_points = 10
        self.Blue_alien_points = 20
        self.Red_alien_points = 40

    def increase_speed(self):
        """increase speed settings and alien point values"""
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
