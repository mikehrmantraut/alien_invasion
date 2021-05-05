class Settings:
    # Alien Invasion oyunu için gerekli tüm ayarları depolar.
    def __init__(self):
        # ekran ayarları
        self.screen_width = 1500
        self.screen_height = 800
        #arkaplan rengi
        self.bg_color = (230, 230, 230)
        # geminin hızı
        self.ship_speed = 1.5
        # merminin hızı
        self.bullet_speed = 2.0
        # merminin genişliği
        self.bullet_width = 3
        # merminin boyu
        self.bullet_height = 10
        # merminin rengi
        self.bullet_color = (60, 60, 60)
        # şarjör
        self.bullets_allowed = 90
        # uzaylı hızı
        self.alien_speed = 1.0
        # uzaylının ölüm hızı
        self.fleet_drop_speed = 10
        # +1 sağı -1 solu simgeliyor.
        self.fleet_direction = 1
        # kaç tane gemi hakkı olduğunu gösterir.
        self.ship_limit = 3
        # hızlanmanın hızı
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.score_scale = 1.5
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
