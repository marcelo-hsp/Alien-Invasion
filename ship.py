import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Espaçonave"""
    
    def __init__(self, ai_settings, screen):
        """Inicializa a espaçonave e define sua posição inicial."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a imagem da espaçonave e obtém seu rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() # delimita um retângulo na imagem carregada
        self.screen_rect = screen.get_rect() # delimita um retângulo na imagem da janela

        # Inicia cada nova espaçonave na parte inferior central da tela
        self.rect.centerx = self.screen_rect.centerx # primeira coordenada do retângulo que contém a imagem
        self.rect.bottom = self.screen_rect.bottom # segunda coordenada do retângulo que contém a imagem
        #self.rect.top = self.screen_rect.top # coordenada de topo
        
        # Armazena um valor decimal para o centro da espaçonave
        self.center_x = float(self.rect.centerx)
        # self.center_y = float(self.rect.centery)
        
        # Gerenciamento de coordenadas
        # self.x_position = self.rect.left
        # self.y_position = self.rect.top

        # Flag de movimento
        self.moving_right = False
        self.moving_left = False
        # self.moving_up = False
        # self.moving_down = False

    def update(self):
        """Atualiza a posição da espaçonave de acordo com a flag de movimento."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center_x -= self.ai_settings.ship_speed_factor
        
        # Esse Trecho de código possibilita o deslocamento da nave no eixo Y
        # if self.moving_up and self.rect.top > self.screen_rect.top:
        #     self.center_y -= self.ai_settings.ship_speed_factor
        # if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
        #     self.center_y += self.ai_settings.ship_speed_factor
        
        # Atualiza o objeto rect de acordo com self.center
        self.rect.centerx = self.center_x # desloca em x
        #self.rect.centery = self.center_y # desloca em y

    def blitme(self):
        """Desenha a espaçonave em sua posição atual."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Centraliza a espaçonave na tela."""
        self.center_x = self.screen_rect.centerx