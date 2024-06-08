import pygame, time
from sys import exit
from player import Player
from laser import Laser
from enemies import Enemies
from random import randint, choice

class Game:

    def __init__(self):
        # Player
        player_sprite = Player((screen_width / 2, screen_height), 5,
                               screen_width, screen_height)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 5
        self.live_surf = pygame.image.load(
            '../assets/lives.png').convert_alpha()
        self.live_x_start_pos = screen_width - (
            self.live_surf.get_size()[0] * 5 + 20)
        self.score = 0
        self.font = pygame.font.Font('../font/Pixeled.ttf', 20)

        # CRT
        self.tv = pygame.image.load('../assets/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

        # Setup Aliens
        self.enemies = pygame.sprite.Group()
        self.enemies_lasers = pygame.sprite.Group()
        self.enemies_speed = 4

        # Audio
        self.music = pygame.mixer.Sound('../audio/music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops = -1)
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)
        
    def enemies_setup(self):
        offset, x_coordinate, y_coordinate = randint(40, 60), randint(70, 330), randint(-50, -30)
        for index in range(0,randint(4,5)):
            x_paramter = x_coordinate * index + offset
            y_parameter = y_coordinate * index
            enemy_sprite = Enemies(x_paramter, y_parameter, screen_height)
            self.enemies.add(enemy_sprite)
        self.enemies_speed += 0.01

    def enemies_shoot(self):
        if self.enemies.sprites():
            random_enemies = choice(self.enemies.sprites())
            laser_sprite = Laser(random_enemies.rect.center,7,screen_height)
            self.enemies_lasers.add(laser_sprite)
            # self.laser_sound.play()
            
    def player_hit(self):
        # player lasers 
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                enemies_hit = pygame.sprite.spritecollide(laser,self.enemies,True) # <- Detect colisions
                if enemies_hit:
                    for enemy in enemies_hit:
                        self.score += 100
                    laser.kill()
                    self.explosion_sound.play()

    def enemies_hit(self):        
        # Enemies Laser
        if self.enemies_lasers:
            for enemy_laser in self.enemies_lasers:
                if pygame.sprite.spritecollide(enemy_laser, self.player, False):
                    enemy_laser.kill()
                
                if pygame.sprite.spritecollide(enemy_laser,self.player,False):
                    enemy_laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.enemies_lasers.empty()
                        # pygame.QUIT()
                        return False
        return True

    def create_crt_lines(self):
        line_height = 4
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)

    def draw_crt(self):
        self.tv.set_alpha(randint(75,90))
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live *
                                         (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def run(self):
        # Player
        self.player.update()
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.player_hit()

        # Enemies
        self.enemies.update(self.enemies_speed)
        self.enemies_lasers.update()
        self.enemies.draw(screen)
        self.enemies_lasers.draw(screen)
        # self.enemies_hit()

        # Tools
        self.create_crt_lines()
        self.draw_crt()
        self.display_lives()
        self.display_score()        
        

if __name__ == "__main__":
    # Setup Pygame
    pygame.init()
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    display = pygame.image.load('../assets/SpaceBg.png').convert_alpha()
    game_active = False
    setting_status = False

    # Setting FPS
    clock = pygame.time.Clock()
    FPS = 60

    # Running Game Class
    game = Game()

    # Custom Event for Spawning Enemies
    ENEMIESSPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMIESSPAWN, 2000)

    ENEMIESSHOOT = pygame.USEREVENT + 2
    pygame.time.set_timer(ENEMIESSHOOT, 600)

    # Intro Screen
    font_type = pygame.font.Font('../font/Pixeled.ttf', 70)
    intro_game = font_type.render('Space Invader', False, ('White'))
    intro_rect = intro_game.get_rect(center=(screen_width/2, screen_height/2 - 35)) 

    font_type = pygame.font.Font('../font/Pixeled.ttf', 35)
    start_game = font_type.render('Mulai Permainan (ENTER)', False, ('White'))
    start_rect = start_game.get_rect(center=(screen_width/2, screen_height/2 + 65)) 

    setting_game = font_type.render('Settings (TAB)', False, ('White'))
    setting_rect = setting_game.get_rect(center=(screen_width/2, screen_height/2 + 120)) 

    font_type = pygame.font.Font('../font/Pixeled.ttf', 20)
    Kelompok_nama = font_type.render('Dibuat Oleh Kelompok 3 [068] | [052] | [042]', False, ('White'))
    kelompok_rect = start_game.get_rect(midbottom=(screen_width/2, screen_height)) 


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                if event.key == pygame.K_TAB:
                    setting_status = True
                if event.key == pygame.K_ESCAPE:
                    setting_status = False
                
                # Setting the Volume
                if event.key == pygame.K_LEFTBRACKET:
                    volume = game.music.get_volume()
                    game.music.set_volume(volume - 0.1)
                if event.key == pygame.K_RIGHTBRACKET:
                    volume = game.music.get_volume()
                    game.music.set_volume(volume + 0.1)


        screen.blit(display, (0, 0))
        if game_active:
            if event.type == ENEMIESSPAWN:
                game.enemies_setup()

            if event.type == ENEMIESSHOOT:
                game.enemies_shoot()
                
            game.run()
            game_active = game.enemies_hit()
        elif setting_status:
            menu_surface = pygame.Surface((800, 600))
            menu_rect = menu_surface.get_rect(center = (screen_width / 2, screen_height / 2))
            pygame.draw.rect(screen, "White", menu_rect, 0, 20)
            
            # Message Control
            setting_message = font_type.render('Kembali (ESC)', False, ('Black'))
            message_rect = setting_message.get_rect(center=(screen_width/2, screen_height/2 - 250)) 
            screen.blit(setting_message, message_rect)
            setting_message = font_type.render('Untuk mengatur volume, Gunakan', False, ('Black'))
            message_rect = setting_message.get_rect(center=(screen_width/2, screen_height/2)) 
            screen.blit(setting_message, message_rect)
            setting_message = font_type.render('Tanda Kiri Kurung Siku ( [ ) atau Kanan ( ] )', False, ('Black'))
            message_rect = setting_message.get_rect(center=(screen_width/2, screen_height/2 + 70)) 
            screen.blit(setting_message, message_rect)

        else :
            # High Score:
            score_message = font_type.render(f'High score: {game.score}', False, ('White'))
            score_rect = score_message.get_rect(center=(screen_width/2, screen_height/2 - 250)) 

            if game.score > 0: screen.blit(score_message, score_rect)
            
            screen.blit(intro_game, intro_rect)
            screen.blit(start_game, start_rect)
            screen.blit(setting_game, setting_rect)
            screen.blit(Kelompok_nama, kelompok_rect)

        # Check the game state
        if game_active:
            if game.lives == 0:
                game.lives = 5
                game.enemies.empty()
                game.enemies_lasers.empty()
                game.score = 0

        pygame.display.flip()
        clock.tick(FPS)

        
