import pygame
from random import choice

class Enemies(pygame.sprite.Sprite):

  def __init__(self, x, y, constraint):
    super().__init__()
    file_path = f'../assets/enemies/{choice([1,2,3,4,5,6,7])}.png'
    self.image = pygame.image.load(file_path).convert_alpha()
    self.rect = self.image.get_rect(topleft=(x, y))
    self.constraint = constraint

  def set_constraint(self):
    if self.rect.y >= self.constraint + 100:
      self.kill()

    # We are adding movement
  def update(self, speed):
    self.rect.y += speed
    self.set_constraint()

