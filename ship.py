import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        # geminin başlangıç pozisyonu ayarlandı.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # geminin hitbox'ı için dikdörtgen seçildi.
        self.screen_rect = ai_game.screen.get_rect()
        
        # uzay gemisi resmi yüklendi.
        self.image = pygame.image.load('images/ship.png')
        # uzay gemisinin yüzeyine ulaşıldı.
        self.rect = self.image.get_rect()
        
        # konumu belirlendi.
        self.rect.midbottom = self.screen_rect.midbottom
        
        # rect integer kabul ediyor. gemi hızı;
        # ondalıklı sayı olduğu için floata çevrildi.
        self.x = float(self.rect.x)
        
        # hareket kontrol komutu
        self.moving_right = False
        self.moving_left = False
    
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
        
        
    # eğer self.moving_right yani sağa gitme komutu doğruysa,
    # resmin bulunduğu hitbox dikdörtgenini x yönünde 1 birim sağa kaydırır.
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed            
        
        self.rect.x = self.x
    # blitme() methodu, self.rect ile belirlenen konuma resmi çizdi.
    def blitme(self):
        self.screen.blit(self.image, self.rect)
