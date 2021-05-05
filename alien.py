import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # Filodaki tek bir uzaylıyı temsil ediyor.
    def __init__(self, ai_game):
        # uzaylının başlangıç pozisyonunu ayarlar.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # uzaylı resmini yükleme ve bir dikdörtgene atama.
        self.image = pygame.image.load('images/alienn.png')
        self.rect = self.image.get_rect()
        
        # her bir uzaylıyı ekranın sol üstünde konumlandırma.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # uzaylının tam yatay pozisyonunu kaydetme.
        self.x = float(self.rect.x)
    
    def check_edges(self):
        # eğer uzaylı ekranın köşesindeyse True'yu döndür.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    # uzaylıyı sağa ya da sola kaydırma
    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
