import pygame

# We define laser (based on player pos when got shot) which has speed and boundry so we can remove it later

# pygame.sprite.Group.draw
# blit the Sprite images

class Laser(pygame.sprite.Sprite):

  def __init__(self, pos, speed, constraint):
    super().__init__()
    self.image = pygame.Surface((4, 20))
    self.image.fill('white')
    self.rect = self.image.get_rect(center=pos)
    self.speed = speed
    self.constraint = constraint

  def set_constraint(self):
    if self.rect.y <= 0 or self.rect.y >= self.constraint + 50:
      self.kill()

  def update(self):
    self.rect.y += self.speed
    self.set_constraint()
