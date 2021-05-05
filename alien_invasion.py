import pygame # oyun fonksiyonlarını içerir.
import sys   # önemli işlevlere sahiptir. (exit, argv. gibi)
from time import sleep
from settings import Settings # ayarlar importlandı.
from ship import Ship  # uzay gemisi görseli importlandı.
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    
    def __init__(self):
        pygame.init()
        # oyun penceresi oluşturmak için kullanılır. 1200 genişlik, 800 yükseklik
        # __init__ 'e dahil edildi ki tüm oyun boyunca çalışsın.
        
        self.settings = Settings() # ayarlar modülü çağrıldı.
        # ekran genişlik ve yüksekliği çağrıldı.
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # oyun penceresinin üstüne başlık atar.
        pygame.display.set_caption("Alien Invasion") 
        
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # buradaki self AlienInvasion instance'ını ifade ediyor.
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() 
        self._create_fleet()
        self.play_button = Button(self, "Play")
               
    def run_game(self):
        # oyunun sürekli çalışması için yazılan ana döngü.
        while True:
            # klavye ve mouse işlemlerini(eventlerini) bekleyen komut.
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()   
                self._update_aliens()
            self._update_screen()
            # klavye ve mouse kullanımlarına yanıt vermek için yazılan komut.
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: 
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
            
            
    def _check_keydown_events(self, event):
        # klavye tuş basışlarına ait komutlar.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        # klavye tuş kaldırışlarına ait komutlar.    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    # mermi ateşlemek için kullanılan komutlar.                
    def _fire_bullet(self):
        # yeni mermi yaratıp mermiler grubuna ekler.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
        
    def _update_bullets(self):
       self.bullets.update()
       for bullet in self.bullets.copy():
           if bullet.rect.bottom <= 0:
               self.bullets.remove(bullet)
       self._check_bullet_alien_collisions()
    # mermi ve uzaylı yok olmasına yanıt vermek amacıyla oluşturuldu.
    
    def _check_bullet_alien_collisions(self):
        # uzaylıyı vuran mermi varsa, hem mermiyi hem uzaylıyı siler.
       collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
       if collisions:
           for aliens in collisions.values():
               self.stats.score += self.settings.alien_points*len(aliens)
           self.sb.prep_score()
           self.sb.check_high_score()
       if not self.aliens:
           self.bullets.empty()
           self._create_fleet()
           self.settings.increase_speed()
           
           self.stats.level += 1
           self.sb.prep_level()
           
        
    
    def _update_aliens(self):
        # önce uzaylının köşede olup olmadığına bakar sonra günceller.  
        self._check_fleet_edges()
        self.aliens.update()
        
        # rakip uzay gemilerinin patlayıp patlamadığına bakma.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
    
    # uzaylı filosu yaratmak.
    def _create_fleet(self):
        # bir uzaylı yap ve bir satıra kaç tane sığar diye bak.
        # aralarındaki boşluk bir uzaylı kadar olcak.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # ekrana kaç tane uzaylı sığacağını hesaplama
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # uzaylıların tüm filosunu yaratma
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # bir uzaylı yaratma ve onu satıra yerleştirme.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    # ekranın en altına bir uzaylının gelip gelmediğinine bakma.    
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
        
    def _check_fleet_edges(self):
        # ekranın kenarına bir uzaylı geldiğinde uygun yaklaşımı vermek gerekir.
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    # rakip gemi tarafından vurulursa olacaklar.
    
    def _ship_hit(self):
        # kalan gemi sayısı 1 azalır.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # kalan rakipler ve mermilerden kurtulunur.
            self.aliens.empty()
            self.bullets.empty()
            # yeni filo oluşturulur.
            self._create_fleet()
            # gemi merkeze yerleştirilir.
            self.ship.center_ship()
            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            
            
    # ekrandaki resimleri güncellemek ve son hali döndürmek için yazılan komut.
    def _update_screen(self):
        # her ekran geçişinde ekranın belirlenen renge boyanmasını sağlar.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # draw() metodu bir argüman alır o da konumlanacağı yüzey.
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        pygame.display.flip() # her zaman ekranın son halini döndürür.
         
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
