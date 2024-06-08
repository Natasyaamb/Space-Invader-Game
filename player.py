import pygame
from laser import Laser
from random import choice

  # Define the pos of the player, mov. speed and the limit so the player didn't move to the other side
  # The base class for visible game objects. Derived classes will want to override the Sprite.update() and assign a
  # Sprite.image and Sprite.rect attributes. The initializer can accept any number of Group instances to be added to.
  # When subclassing the Sprite, be sure to call the base initializer before adding the Sprite to Groups. For example:

class Player(pygame.sprite.Sprite):

  def __init__(self, pos, speed, constraint_x, constraint_y):
    super().__init__()
    user_starship = choice(['Kled-Battlecruisers', 'Kled-Dreadnought', 'Nairan-Battlecruiser', 'Nairan-Dreadnought'])
    path_asset = f'../assets/player/{user_starship}.png'
    self.image = pygame.image.load(path_asset).convert_alpha()
    self.rect = self.image.get_rect(midbottom=pos)
    self.speed = speed
    self.constraint_x = constraint_x
    self.constraint_y = constraint_y

    self.ready = True
    self.shoot_time = 0
    self.recharge_time = 600

    self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
    self.laser_sound.set_volume(0.5)

    # We can create a laser by setting laser as group of sprite
    self.lasers = pygame.sprite.Group()

  def get_input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
      self.rect.x -= self.speed 
    if keys[pygame.K_RIGHT]:
      self.rect.x += self.speed 
    if keys[pygame.K_UP]:
      self.rect.y -= self.speed 
    if keys[pygame.K_DOWN]:
      self.rect.y += self.speed 

    if keys[pygame.K_SPACE] and self.ready:
      self.shoot_laser()
      self.ready = False
      # Getting the time interval between shoots
      self.shoot_time = pygame.time.get_ticks()
      self.laser_sound.play()

  def recharge(self):
    if not self.ready:
      # We make a timer interval between time after shot and compare it with the recharge time
      current_time = pygame.time.get_ticks()
      if current_time - self.shoot_time >= self.recharge_time:
        self.ready = True

  def set_constraint(self):
    if self.rect.left <= 0:
      self.rect.left = 0
    if self.rect.right >= self.constraint_x:
      self.rect.right = self.constraint_x
    if self.rect.top <= 0:
      self.rect.top = 0 
    if self.rect.bottom >= self.constraint_y:
      self.rect.bottom = self.constraint_y

  def shoot_laser(self):
    self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

  def update(self):
    self.get_input() 
    self.set_constraint()
    self.recharge()
    self.lasers.update()
