import sys
import pygame
from pygame.sprite import Sprite
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets, aliens): # Verifica evento para tecla pressionada
    """Responde ao pressionamento de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = True
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit(0)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, aliens, bullets, ship)

def check_keyup_events(event, ship): # Verifica evento para a tecla solta
    """Responde a soltura de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False 
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clicar em Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(stats, sb, aliens, bullets, ai_settings, screen, ship)

def start_game(ai_settings, screen, stats, sb, aliens, bullets, ship):
    #Oculta o cursor do mouse
        if not stats.game_active:
            # Reinicia as configura????es do jogo
            ai_settings.initialize_dynamic_settings()

            pygame.mouse.set_visible(False)

            # Reinicia os dados estat??sticos do jogo
            stats.reset_stats()
            stats.game_active = True

            # Reinicia as imagens do painel de pontua????o
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # Esvazia a lista de alien??genas e de proj??teis
            aliens.empty()
            bullets.empty()

            # Cria uma nova frota e centraliza a espa??onave
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """
    Atualiza as imagens na tela e altera para a nova tela
    """
    # Redesenha a tela a cada passagem pelo la??o
    screen.fill(ai_settings.bg_color)

    # Redesenha todos os proj??teis/ atr??s da espa??onave e dos aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    # alien.blitme() <- no caso de desenhar individualmente 
    aliens.draw(screen) # desenha a frota de aliens

    # Desenha a informa????o sobre pontua????o
    sb.show_score()

    # Desenha o bot??o Play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    # Deixa a tela mais recente vis??vel
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza a posi????o dos proj??teis e se livra dos proj??teis antigos"""
    # Atualiza a posi????o dos proj??teis
    #bullets.update()

    # Livra-se dos proj??teis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    
    check_bullet_allien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_allien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde a colis??es entre proj??teis e alien??genas."""
    # Verifica se algum proj??til atingiu algum alien??gena
    # Em caso afirmativo, livra-se do proj??til e do alien??gena
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) 
    # Essa fun????o retorna um dicion??rio em que a chave seria o proj??til que acertou o 
    # alien e o valor da chave seria o alien??gena atingido
    # O primeiro valor booleano determina se o proj??til some
    # e o segundo se o alien some

    if collisions:
        for aliens in collisions.values():    
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destr??i os proj??teis existentes e cria uma nova frota
        # se a frota for totalmente destru??da, inicia um novo n??vel
        bullets.empty()
        ai_settings.increase_speed()
        
        # Aumenta o n??vel
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara um proj??til se o limite ainda n??o foi alcan??ado"""
    # Cria um novo proj??til e o adiciona ao grupo de proj??teis
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determina o n??mero de alien??genas que cabem em uma liha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o n??mero de linhas com alien??genas que cabem na tela."""
    avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Cria um alien??gena e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width 
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de alien??genas."""
    # Cria um alien??gena e calcula o n??mero de alien??genas em uma linha
    # O espa??amento entre os alien??genas ?? igual ?? largura de um alien??gena
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Cria a primeira linha de alien??genas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alien??gena alcan??ou uma borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e muda a sua dire????o."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se algum alien??gena atingiu a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # trata esse caso do mesmo modo que ?? feito quando a espa??onave ?? atingida
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Verifica se a frota est?? em uma das bordas e ent??o atualiza
    as posi????es de todos os alien??genas da frota.
    """
    check_fleet_edges(ai_settings, aliens)
    
    aliens.update()

    # Verifica se houve colis??es entre alien??genas e a espa??onave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Verifica se algum alien??gena atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde ao fato de a espa??onave ter sido atingida por um alien??gena."""
    if stats.ships_left > 0:
        # decrementa ship_left
        stats.ships_left -= 1

        #Atualiza o painel de pontua????es
        sb.prep_ships()

        # Esvazia a lista de alien??genas e de proj??teis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a Espa??onave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma pausa
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    """Verifica se h?? uma nova pontua????o m??xima."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()