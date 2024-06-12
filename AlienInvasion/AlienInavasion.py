import pygame, sys
from time import sleep

#from pygame.locals import QUIT

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

pygame.font.init()
FONT = pygame.font.SysFont("Consolas",30)

class AlienInvasion:
  def __init__(self):
    pygame.init()
    self.settings = Settings()
    self.screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
    self.settings.screen_width = self.screen.get_rect().width
    self.settings.screen_height = self.screen.get_rect().height
    pygame.display.set_caption("Masons Alien Invasion")

    self.stats = GameStats(self)

    self.bg_color = (50,230,230)
    self.ship = Ship(self)
    self.bullets = pygame.sprite.Group()

    self.livesL = self.settings.lives
    self.aliensK = self.settings.aliensKilled

    self.aliens = pygame.sprite.Group()
    self._create_fleet()


  def run_game(self):
    while True:
      self._check_events()
      if self.stats.game_active and self.livesL >= 0:
        self.ship.update()
        self._update_bullets()
        self._update_aliens()
      self._update_screen()

  def _check_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        self._check_keydown_events(event)
      elif event.type == pygame.KEYUP:
        self._check_keyup_events(event)

  def _check_keydown_events(self, event):
    if event.key == pygame.K_RIGHT:
      self.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
      self.ship.moving_left = True
    elif event.key == pygame.K_q:
      sys.exit()
    elif event.key == pygame.K_SPACE:
      self._fire_bullet()

  def _check_keyup_events(self, event):
    if event.key == pygame.K_RIGHT:
      self.ship.moving_right = False
    elif event.key ==pygame.K_LEFT:
      self.ship.moving_left = False

  def _fire_bullet(self):
    if len(self.bullets) < self.settings.bullets_allowed:
      new_bullet = Bullet(self)
      self.bullets.add(new_bullet)

  def _update_bullets(self):
    self.bullets.update()
    for bullet in self.bullets.copy():
      if bullet.rect.bottom <=0:
        self.bullets.remove(bullet)
    self._check_bullet_alien_collisions()

  def _check_bullet_alien_collisions(self):
    collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,True)
    if len(collisions) > 0:
      self.aliensK += 1
    if not self.aliens:
      self.bullets.empty()
      self._create_fleet()

  def _update_aliens(self):
    self._check_fleet_edges()
    self.aliens.update()
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
      print ("SHIP HIT!!!")
      self._ship_hit()
      self.livesL = self.livesL - 1
      print(self.livesL)
    self._check_aliens_bottom()

  def _create_fleet(self):
    aliens = Alien(self)
    alien_width, alien_height = aliens.rect.size
    available_space_x = self.settings.screen_width - (2*alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)
    ship_height = self.ship.rect.height
    available_space_y = (self.settings.screen_height -
    (3 * alien_height) - ship_height)
    number_rows = available_space_y // (2 * alien_height)
    for row_number in range (number_rows):
      for alien_number in range (number_aliens_x):
        self._create_alien(alien_number, row_number)

  def _create_alien(self, alien_number, row_number):
    aliens = Alien(self)
    alien_width, alien_height = aliens.rect.size
    alien_width = aliens.rect.width
    aliens.x = alien_width + 2 * alien_width * alien_number
    aliens.rect.x = aliens.x
    aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
    self.aliens.add(aliens)

  def _check_fleet_edges(self):
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break

  def _change_fleet_direction(self):
    for alien in self.aliens.sprites():
      alien.rect.y += self.settings.fleet_drop_speed
    self.settings.fleet_direction *= -1

  def _ship_hit(self):
    if self.stats.ships_left >0:
      self.stats.ships_left -= 1
      self.aliens.empty()
      self.bullets.empty()
      self._create_fleet()
      self.ship.center_ship()
      sleep (0.5)
    else:
      self.stats.game_active = False

  def _check_aliens_bottom(self):
    screen_rect = self.screen.get_rect()
    for alien in self.aliens.sprites():
      if alien.rect.bottom >= screen_rect.bottom:
        self._ship_hit()
        break

  def _update_screen(self):
    self.screen.fill(self.settings.bg_color)
    self.ship.blitme()
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    self.aliens.draw(self.screen)
    if(self.livesL >= 0):
      test_txt = FONT.render(f"Lives Left: {self.livesL}      Aliens Killed: {self.aliensK}", 1,"white")
    else:
      test_txt = FONT.render(f"Game Over          Aliens Killed: {self.aliensK}", 1,"red")
    self.screen.blit(test_txt, (0,0))
    pygame.display.flip()


if __name__ == '__main__':
  ai = AlienInvasion()
  ai.run_game()
quit()