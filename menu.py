import level
import resources
import pygame
import player

SCREEN_W = 800
SCREEN_H = 600


class Menu:
    def __init__(self, game):
        self.loop = True
        self.game = game
        self.show_cursor = True
        self.type = 'vertical'
        self.cursor_type = 'right'
        self.item = 0
        self.menu_elements = []
        self.cursor_count = 0
        self.last_update = 0
        self.previous_menu = self

    def draw_cursor(self, type, surf, pos, delay):
        surf.blit(resources.images['arrow'][type][str(self.cursor_count)], pos)
        if pygame.time.get_ticks() - self.last_update > delay:
            self.cursor_count = (self.cursor_count + 1) % len(resources.images['arrow'][type])
            self.last_update = pygame.time.get_ticks()

    def add_option(self, text, action=None, state=''):
        self.menu_elements.append({'state': state, 'text': text, 'action': action})

    def do_action(self):
        if self.menu_elements[self.item]['action'] is not None:
            self.menu_elements[self.item]['action']()

    def menu_previous(self):
        if self.item == 0 and self.loop is True:
            self.item = len(self.menu_elements) - 1
        elif self.item > 0:
            self.item = self.item - 1

    def menu_next(self):
        if self.item == len(self.menu_elements) - 1 and self.loop is True:
            self.item = 0
        elif self.item < len(self.menu_elements) - 1:
            self.item = self.item + 1


class SelectLevel(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.show_cursor = False
        self.add_option('Śnieżna kraina', lambda: self.save_level(level.Snowland()), 'snowland')
        self.add_option('Podziemia zamku', lambda: self.save_level(level.Dungeon()), 'dungeon')
        self.previous_menu = SelectHero(self.game)

    def save_level(self, level):
        self.game.current_level = level
        self.game.current_hero.rect.x = level.startpoint[0]
        self.game.current_hero.rect.y = level.startpoint[1]
        self.game.main_menu = False
        self.game.in_game = True

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = SCREEN_W / 2
        starty = SCREEN_H / 2 - 75
        stepy = 50
        self.game.draw_text(surf, 'Wybierz poziom', 40, startx, starty + 300, self.game.WHITE, False)
        screen.blit(resources.images['menu']['level'][self.menu_elements[self.item]['state']], (116, starty + 32))
        screen.blit(resources.images['menu']['level']['frame'], (100, starty + 16))
        for el in self.menu_elements:
            if self.item == self.menu_elements.index(el):
                self.game.draw_text(surf, el['text'], 30, startx, starty + 50 + (self.menu_elements.index(el) * stepy),
                                    self.game.RED)
            else:
                self.game.draw_text(surf, el['text'], 30, startx, starty + 50 + (self.menu_elements.index(el) * stepy),
                                    self.game.YELLOW)
        screen.blit(surf, (0, 0))


class SelectHero(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.type = 'horizontal'
        self.add_option('', lambda: self.save_hero(player.Wizard(self.game)))
        self.add_option('', lambda: self.save_hero(player.Viking(self.game)))
        self.previous_menu = MainMenu(self.game)

    def save_hero(self, hero):
        self.game.current_hero = hero

        self.game.change_menu(SelectLevel(self.game))

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = SCREEN_W / 2
        starty = SCREEN_H / 2 - 75
        stepx = 250
        self.game.draw_text(surf, 'Wybierz bohatera', 40, startx, starty + 300, self.game.WHITE, False)
        for el in self.menu_elements:
            if self.item == self.menu_elements.index(el):
                if self.show_cursor is True:
                    self.draw_cursor('up', surf,
                                     (startx + (self.menu_elements.index(el) * stepx) - 170, starty + 150), 70)
                    screen.blit(resources.images['menu']['wizard'], (startx - 200, starty))
                    screen.blit(resources.images['menu']['viking'], (startx + 50, starty))
        screen.blit(surf, (0, 0))


class Options(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.add_option('Głośność muzyki', lambda: self.game.change_menu(MusicVolume(self.game, 'music_volume')))
        self.add_option('Głośność efektów', lambda: self.game.change_menu(MusicVolume(self.game, 'effects_volume')))
        self.previous_menu = MainMenu(self.game)

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = 350
        starty = 250
        stepy = 50
        for el in self.menu_elements:
            if self.item == self.menu_elements.index(el):
                self.game.draw_text(surf, el['text'], 40, startx, starty + (self.menu_elements.index(el) * stepy),
                                    self.game.RED)
                if self.show_cursor is True:
                    self.draw_cursor('right', surf, (startx - 80, starty + (self.menu_elements.index(el) * stepy) - 30),
                                     70)
            else:
                self.game.draw_text(surf, el['text'], 40, startx, starty + (self.menu_elements.index(el) * stepy),
                                    self.game.YELLOW)
        screen.blit(surf, (0, 0))


class MusicVolume(Menu):
    def __init__(self, game, menu_type):
        Menu.__init__(self, game)
        self.type = 'horizontal'
        self.menu_type = menu_type
        self.item = int(self.game.settings.getSetting(menu_type) / 10)
        self.loop = False
        self.add_option('', lambda: self.update_volume(0))
        self.add_option('*', lambda: self.update_volume(10))
        self.add_option('*', lambda: self.update_volume(20))
        self.add_option('*', lambda: self.update_volume(30))
        self.add_option('*', lambda: self.update_volume(40))
        self.add_option('*', lambda: self.update_volume(50))
        self.add_option('*', lambda: self.update_volume(60))
        self.add_option('*', lambda: self.update_volume(70))
        self.add_option('*', lambda: self.update_volume(80))
        self.add_option('*', lambda: self.update_volume(90))
        self.add_option('*', lambda: self.update_volume(100))
        self.previous_menu = Options(self.game)

    def update_volume(self, volume):
        self.game.settings.setSetting(self.menu_type, volume)
        if self.menu_type == 'music_volume':
            pygame.mixer.music.set_volume(volume / 100)

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = 350
        starty = 250
        stepx = 20
        self.game.draw_text(surf, str(self.game.settings.getSetting(self.menu_type)) + '%', 40,
                            startx + (len(self.menu_elements) * stepx) + 20, starty - 10, self.game.WHITE)
        for el in self.menu_elements:
            if self.item >= self.menu_elements.index(el):
                self.game.draw_text(surf, el['text'], 40, startx + (self.menu_elements.index(el) * stepx), starty,
                                    self.game.RED)
            else:
                self.game.draw_text(surf, el['text'], 40, startx + (self.menu_elements.index(el) * stepx), starty,
                                    self.game.YELLOW)
        screen.blit(surf, (0, 0))


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.add_option('Rozpocznij grę', lambda: self.game.change_menu(SelectHero(self.game)))
        self.add_option('Wyniki', lambda: self.game.change_menu(Scores(self.game)))
        self.add_option('Opcje', lambda: self.game.change_menu(Options(self.game)))
        self.add_option('Wyjdź z gry', lambda: pygame.quit())

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = 350
        starty = 300
        stepy = 50
        self.game.draw_text(surf, 'Witaj ' + self.game.account + '!', 40, 500, 50, self.game.WHITE)
        for el in self.menu_elements:
            if self.item == self.menu_elements.index(el):
                self.game.draw_text(surf, el['text'], 40, startx, starty + (self.menu_elements.index(el) * stepy),
                                    self.game.RED)
                if self.show_cursor is True:
                    self.draw_cursor('right', surf, (startx - 80, starty + (self.menu_elements.index(el) * stepy) - 30),
                                     70)
            else:
                self.game.draw_text(surf, el['text'], 40, startx, starty + (self.menu_elements.index(el) * stepy),
                                    self.game.YELLOW)
        screen.blit(surf, (0, 0))


class Scores(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.previous_menu = MainMenu(self.game)
        cnt = 1
        for x in self.game.scores.scores:
            self.add_option(str(cnt) + '. ' + x[0] + ': ' + str(x[1]), None, cnt)
            cnt += 1
            if cnt == 9:
                break

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = 500
        starty = 100
        stepy = 40
        for el in self.menu_elements:
            self.game.draw_text(surf, el['text'], 30, startx, starty + (self.menu_elements.index(el) * stepy),
                                self.game.YELLOW)
        screen.blit(surf, (0, 0))


class GamePause(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.add_option('Kontynuuj grę', lambda: self.game.resume_game())
        # self.add_option('Zapisz grę', lambda: self.game.save_game())
        self.add_option('Zakończ grę', lambda: self.game.game_over())

    def draw_menu(self, screen):
        surf = pygame.surface.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        startx = 300
        starty = 200
        stepy = 50
        half_transparent = pygame.Surface((800, 600))
        half_transparent.set_alpha(127)
        screen.blit(half_transparent, (0, 0))
        screen.blit(resources.images['game']['menu']['bg'], (222, 52))
        for el in self.menu_elements:
            if self.item == self.menu_elements.index(el):
                self.game.draw_text(surf, el['text'], 40, startx, starty + (self.menu_elements.index(el) * stepy),
                                    self.game.RED)
                if self.show_cursor is True:
                    self.draw_cursor('right', surf, (startx - 80, starty + (self.menu_elements.index(el) * stepy) - 30),
                                     70)
            else:
                self.game.draw_text(surf, el['text'], 40, startx, starty + (self.menu_elements.index(el) * stepy),
                                    self.game.YELLOW)
        screen.blit(surf, (0, 0))
