import menu
import resources
from game import Game
import pygame
from data import Settings

settings = Settings()
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(settings.getSetting('music_volume') / 100)

clock = pygame.time.Clock()
SCREEN_W = 800
SCREEN_H = 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

resources.loadresources()
pygame.display.set_caption('Brave Dwarves 2')
pygame.display.set_icon(resources.images['game']['icon'])

running = True

bd2 = Game(screen, settings)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            settings.writeSettings()
            running = False
        if bd2.main_menu or bd2.is_paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if bd2.current_menu.type == 'vertical':
                        bd2.current_menu.menu_next()
                if event.key == pygame.K_UP:
                    if bd2.current_menu.type == 'vertical':
                        bd2.current_menu.menu_previous()
                if event.key == pygame.K_RETURN:
                    bd2.current_menu.do_action()
                if event.key == pygame.K_LEFT:
                    if bd2.current_menu.type == 'horizontal':
                        bd2.current_menu.menu_previous()
                if event.key == pygame.K_RIGHT:
                    if bd2.current_menu.type == 'horizontal':
                        bd2.current_menu.menu_next()
                if event.key == pygame.K_ESCAPE:
                    bd2.current_menu = bd2.current_menu.previous_menu
        if bd2.in_game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not bd2.is_paused:
                        bd2.pause_game()
                    else:
                        if bd2.you_won or bd2.you_lost:
                            bd2.game_over()
                        else:
                            bd2.resume_game()
                if not bd2.is_paused:
                    if event.key == pygame.K_z:
                        bd2.current_hero.previousweapon()
                    if event.key == pygame.K_p:
                        print(bd2.current_hero.rect)
                    if event.key == pygame.K_x:
                        bd2.current_hero.nextweapon()
                    if event.key == pygame.K_LEFT:
                        bd2.current_hero.go_left = True
                        bd2.current_hero.turn_left = True
                    if event.key == pygame.K_RIGHT:
                        bd2.current_hero.go_right = True
                        bd2.current_hero.turn_left = False
                    if event.key == pygame.K_SPACE:
                        bd2.current_hero.do_jump = True
                    if event.key == pygame.K_a:
                        bd2.current_hero.resetcount()
                        bd2.current_hero.isfiring = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    bd2.current_hero.resetcount()
                    bd2.current_hero.movementx = 0
                if event.key == pygame.K_RIGHT:
                    bd2.current_hero.resetcount()
                    bd2.current_hero.movementx = 0
                if event.key == pygame.K_LEFT:
                    bd2.current_hero.go_left = False
                if event.key == pygame.K_RIGHT:
                    bd2.current_hero.go_right = False
                if event.key == pygame.K_SPACE:
                    bd2.current_hero.do_jump = False
                if event.key == pygame.K_a:
                    bd2.current_hero.isfiring = False
                if not bd2.is_paused:
                    if event.key == pygame.K_LEFT:
                        if bd2.current_hero.go_right is True:
                            bd2.current_hero.turn_left = False
                    if event.key == pygame.K_RIGHT:
                        if bd2.current_hero.go_left is True:
                            bd2.current_hero.turn_left = True

    bd2.game_loop()
    pygame.display.update()

pygame.quit()
quit()
