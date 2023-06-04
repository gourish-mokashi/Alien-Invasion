class Settings:
    def __init__(self):
        self.screen_width = 1366
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # ship settings
        self.ship_speed = 10.0
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 5.0
        self.bullet_height = 20.0
        self.bullet_color = (150, 152, 255)
        self.bullet_allowed = 5

        # alien settings
        self.ufo_drop_speed = 10.0

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # self.star_size = 5
        # self.no_stars = 10

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.bullet_speed = 5
        self.ufo_speed = 3
        self.ufo_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ufo_speed *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
