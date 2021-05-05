import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # uzay gemisinden ateşlenen mermileri içeren class.
    
    def __init__(self, ai_game):
        # uzay gemisinin bulunduğu pozisyondan bir mermi yaratır.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # merminin dikdörtgenini (0,0)'dan normal pozisyona yaratır.
        
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, \
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # merminin pozisyonunu kesirli halde depolar.
        self.y = float(self.rect.y)
    
    def update(self):
        # mermiyi ekranın yukarısına gönderir.
        # merminin pozisyonunu kesirli ifade eder.
        self.y -= self.settings.bullet_speed
        # dikdörtgenin pozisyonunu günceller.
        self.rect.y = self.y
    
    def draw_bullet(self):
        # ekrana mermiyi çizer.
        pygame.draw.rect(self.screen, self.color, self.rect)
