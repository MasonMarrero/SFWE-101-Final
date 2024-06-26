class Settings:
  def __init__(self) -> None:
    self.screen_width = 1200
    self.screen_height = 800
    self.bg_color = (70,60,255)

    self.ship_speed = 1.5
    self.ship_limit = 3
    self.bullet_speed = 1.5
    self.bullet_width = 3
    self.bullet_height = 15
    self.bullet_color = (60, 60, 60)
    self.bullets_allowed = 3
# alien settings
    self.alien_speed = 1.0
    self.fleet_drop_speed = 10
    #self.alien_width = 3
# fleet direction of 1 represents right; -1 represents left.
    self.fleet_direction = 1

    self.lives = 3
    self.aliensKilled = 0