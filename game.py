import resources
import pygame
import menu
from data import Scores
import level

FONT = 'fonts/zepplin.ttf'

class Game():
    def __init__(self, screen, settings):
        self.account = 'Kamil'
        self.scores = Scores()
        self.main_menu = False
        self.in_game = False
        self.is_paused = False
        self.current_menu = menu.MainMenu(self)
        self.current_level = None
        self.you_won = False
        self.you_lost = False
        self.screen = screen
        self.settings = settings
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.current_hero = None
        self.player_life = 100
        self.player_gotkey = False
        self.player_points = 0
        self.player_life_count = 1
        self.go_to_menu()

    def draw_text(self, surf, text, size, x, y, color, to_left = True):
        font = pygame.font.Font(FONT, size)
        text_surface = font.render(text, True, color)
        text_surface_shadow = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect_shadow = text_surface_shadow.get_rect()
        if to_left:
            text_rect.center = (x + (text_rect.width / 2), y)
            text_rect_shadow.center = ((x + (text_rect_shadow.width / 2)) + (size / 20), y + (size / 20))
        else:
            text_rect.center = (x, y)
            text_rect_shadow.center = (x + (size / 20), y + (size / 20))
        surf.blit(text_surface_shadow, text_rect_shadow)
        surf.blit(text_surface, text_rect)

    def pause_game(self):
        self.current_menu = menu.GamePause(self)
        self.is_paused = True

    def resume_game(self):
        self.is_paused = False

    def change_menu(self, menu):
        self.current_menu = menu

    def game_over(self):
        self.scores.addScore(['Kamil', self.player_points])
        self.scores.saveScores()
        self.player_life = 100
        self.player_points = 0
        self.player_gotkey = False
        self.you_won = False
        self.you_lost = False
        self.player_life_count = 1
        self.go_to_menu()
        self.current_menu = menu.Scores(self)

    def go_to_menu(self):
        self.is_paused = False
        self.main_menu = True
        self.in_game = False
        self.current_menu = menu.MainMenu(self)
        pygame.mixer.music.load('music/main_menu.mp3')
        pygame.mixer.music.play(-1)

    def draw_ui(self):
        self.screen.blit(resources.images['game']['panel']['main'], (0, 486))
        heart = pygame.surface.Surface((51, 0.4 * self.player_life), pygame.SRCALPHA)
        heart.blit(resources.images['game']['panel']['heart'], (0, -40 + (0.4 * self.player_life)))
        self.draw_text(self.screen, str(self.player_points), 20, 654, 568, self.WHITE, False)
        self.draw_text(self.screen, '*Mini Mapa*', 20, 208, 568, self.WHITE, False)
        self.screen.blit(heart, (90, 550 + (40 - (0.4 * self.player_life))))
        self.draw_text(self.screen, str(self.player_life_count), 20, 115, 575, self.WHITE, False)
        for weapon in self.current_hero.eq:
            self.screen.blit(weapon.image, (276.5 + self.current_hero.eq.index(weapon) * 54.5, 545))
            if self.current_hero.currentweapon == weapon:
                self.screen.blit(resources.images['game']['panel']['weapon'],
                                 (276.5 + self.current_hero.eq.index(weapon) * 54.5, 545))
        if self.is_paused:
            if self.you_won:
                self.draw_text(self.screen, 'Wygrałeś!!!', 60, 400, 300, self.YELLOW, False)
            elif self.you_lost:
                self.draw_text(self.screen, 'Przegrałeś!!!', 60, 400, 300, self.RED, False)
            else:
                self.current_menu.draw_menu(self.screen)


    def game_loop(self):
        if self.main_menu is True:
            self.screen.blit(resources.images['menu']['bg'], (0,0))
            self.current_menu.draw_menu(self.screen)
        if self.in_game is True:
            self.screen.fill(self.BLACK)
            self.current_level.current_sublevel.display(self.screen, self)
            self.current_hero.draw(self.screen)
            self.draw_ui()
