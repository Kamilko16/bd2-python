import pygame

import resources


class WeaponParticle(pygame.sprite.Sprite):
    def __init__(self, anim, damage, x, y, movementx, movementy, life, delay, flip=False):
        super().__init__()
        self.delay = delay
        self.last_update = 0
        self.animation = anim
        self.alive = pygame.time.get_ticks()
        self.count = 0
        self.image = anim['0']
        self.damage = damage
        self.rect = self.image.get_rect()
        self.spawned = pygame.time.get_ticks()
        self.life = life
        self.flip = flip
        self.rect.x = x
        self.rect.y = y
        self.movementx = movementx
        self.movementy = movementy

    def animate(self):
        if self.flip:
            self.image = pygame.transform.flip(self.animation[str(self.count)], True, False)
        else:
            self.image = self.animation[str(self.count)]
        if pygame.time.get_ticks() - self.last_update > self.delay:

            if self.count == len(self.animation) - 1:
                self.count = 0
            else:
                self.count += 1

            self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.movementx
        self.alive += 20
        self.rect.y += self.movementy

    def draw(self, surf, paused):
        if not paused:
            if self.alive - self.spawned > self.life:
                self.kill()
            self.update()
            self.animate()
        surf.blit(self.image, self.rect)


class Weapon:
    def __init__(self, name, usages, damage, delay):
        self.image = resources.images['weapon'][name]['icon']
        self.name = name
        self.usages = usages
        self.delay = delay
        self.sound = pygame.mixer.Sound('music/' + name + '.ogg')
        self.damage = damage
        self.last_update = 0

    def fire(self, player, level):
        if pygame.time.get_ticks() - self.last_update > self.delay:
            if player.turn_left:
                level.addParticle(WeaponParticle(resources.images['weapon'][self.name]['particle'], self.damage,
                                                 player.rect.centerx - 100, player.rect.centery - 10, -3, 0, 3000, 50))
            else:
                level.addParticle(WeaponParticle(resources.images['weapon'][self.name]['particle'], self.damage,
                                                 player.rect.centerx + 30, player.rect.centery - 10, 3, 0, 3000, 50, True))

            channel = pygame.mixer.find_channel()
            channel.set_volume(player.game.settings.getSetting('effects_volume') / 100)
            channel.play(self.sound)
            self.last_update = pygame.time.get_ticks()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, game):
        super().__init__()
        self.resources = ''
        self.go_left = False
        self.currentweapon = None
        self.go_right = False
        self.do_jump = False
        self.closest_left = None
        self.closest_right = None
        self.closest_top = None
        self.closest_bottom = None
        self.game = game
        self.blockright = False
        self.blockleft = False
        self.isonground = True
        self.isfiring = False
        self.turn_left = False
        self.last_update = 0
        self.isattacking = False
        self.image = image
        self.movementx = 0
        self.movementy = 0
        self.maxgravity = 5
        self.isreversing = False
        self.rect = self.image.get_rect()
        self.count = 0
        self.eq = []

    def gravitation(self):
        if self.movementy < self.maxgravity and not self.isonground and not self.game.is_paused:
            self.movementy += 0.2

    def resetcount(self):
        if not self.isfiring:
            self.count = 0
            self.isreversing = False

    def takedamage(self, damage):
        if self.game.player_life - damage <= 0:
            if self.game.player_life_count - 1 < 0:
                self.game.you_lost = True
                self.game.pause_game()
            else:
                self.game.player_life_count -= 1
                self.game.player_life = 100
        else:
            self.game.player_life -= damage

    def jump(self):
        if self.isonground:
            self.movementy = -7
            self.isonground = False

    def nextweapon(self):
        if self.eq.index(self.currentweapon) < len(self.eq) - 1:
            self.currentweapon = self.eq[self.eq.index(self.currentweapon) + 1]

    def previousweapon(self):
        if self.eq.index(self.currentweapon) > 0:
            self.currentweapon = self.eq[self.eq.index(self.currentweapon) - 1]

    def addtoeq(self, weapon):
        self.eq.append(weapon)

    def draw(self, surface):
        self.gravitation()
        self.update()
        if not self.game.is_paused:
            if self.isfiring:
                self.animate(resources.images[self.resources]['fire'], 25, self.turn_left, False)
            else:
                if self.movementy != 0:
                    if self.movementy < 0:
                        if self.turn_left:
                            self.image = pygame.transform.flip(resources.images[self.resources]['jump'], True, False)
                        else:
                            self.image = resources.images[self.resources]['jump']

                    elif self.movementy > 0:
                        if self.turn_left:
                            self.image = pygame.transform.flip(resources.images[self.resources]['fall'], True, False)
                        else:
                            self.image = resources.images[self.resources]['fall']
                else:
                    if self.movementx != 0:
                        self.animate(resources.images[self.resources]['walk'], 30, self.turn_left, False)
                    if self.movementx == 0:
                        self.animate(resources.images[self.resources]['idle'], 100, self.turn_left, True)

        surface.blit(self.image, self.rect)

    def animate(self, animation, delay, flip, reverse):

        if self.count + 1 > len(animation):
            self.count = 0

        if flip:
            self.image = pygame.transform.flip(animation[str(self.count)], True, False)
        else:
            self.image = animation[str(self.count)]
        if pygame.time.get_ticks() - self.last_update > delay:
            if reverse:
                if self.count == len(animation) - 1:
                    self.isreversing = True
                elif self.count == 0:
                    self.isreversing = False

                if self.isreversing:
                    self.count -= 1
                else:
                    self.count += 1
            else:
                if self.resources != 'wizard' or self.count != len(animation) - 1 or not self.isfiring:
                    if self.count == len(animation) - 1:
                        self.count = 0
                    else:
                        self.count += 1

            self.last_update = pygame.time.get_ticks()

    def update(self):
        if not self.game.is_paused:

            if self.isfiring:
                self.currentweapon.fire(self, self.game.current_level.current_sublevel)

            coliding_items = pygame.sprite.spritecollide(self, self.game.current_level.current_sublevel.items, False)

            for item in coliding_items:
                item.pickup(self.game)

            coliding_enemies = pygame.sprite.spritecollide(self, self.game.current_level.current_sublevel.enemies,
                                                           False)

            if self.game.current_level.current_sublevel.gate is not None:
                if pygame.sprite.collide_rect(self, self.game.current_level.current_sublevel.gate) and self.game.player_gotkey:
                    if abs(self.rect.centerx - self.game.current_level.current_sublevel.gate.rect.centerx) < 20:
                        self.game.current_level.current_sublevel.gate.open()
                        self.game.you_won = True
                        self.game.pause_game()

            for enemy in self.game.current_level.current_sublevel.enemies:
                if coliding_enemies.count(enemy) == 0:
                    enemy.attack = False

            for enemy in coliding_enemies:
                if not enemy.attack:
                    enemy.last_update_attack = pygame.time.get_ticks()
                    enemy.attack = True
                if pygame.time.get_ticks() - enemy.last_update_attack >= enemy.attackspeed * enemy.attackframe:
                    self.takedamage(enemy.damage)
                    channel = pygame.mixer.find_channel()
                    channel.set_volume(self.game.settings.getSetting('effects_volume') / 100)
                    channel.play(enemy.sound)
                    enemy.last_update_attack = pygame.time.get_ticks()
                if enemy.rect.centerx < self.rect.centerx:
                    enemy.turnright = True
                else:
                    enemy.turnright = False

            coliding_platforms = pygame.sprite.spritecollide(self, self.game.current_level.current_sublevel.platforms,
                                                             False)

            self.closest_left = None
            self.closest_right = None
            self.closest_top = None
            self.closest_bottom = None

            if len(coliding_platforms) == 0:
                self.isonground = False
                self.blockright = False
                self.blockleft = False

            for platf in coliding_platforms:
                if self.closest_left is None:
                    self.closest_left = platf
                else:
                    if abs(platf.rect.right - self.rect.left) < abs(self.closest_left.rect.right - self.rect.left):
                        self.closest_left = platf

                if self.closest_bottom is None:
                    self.closest_bottom = platf
                else:
                    if abs(platf.rect.top - self.rect.bottom) < abs(self.closest_bottom.rect.top - self.rect.bottom):
                        self.closest_bottom = platf

                if self.closest_right is None:
                    self.closest_right = platf
                else:
                    if abs(platf.rect.left - self.rect.right) < abs(self.closest_right.rect.left - self.rect.right):
                        self.closest_right = platf

                if self.closest_top is None:
                    self.closest_top = platf
                else:
                    if abs(platf.rect.bottom - self.rect.top) < abs(self.closest_top.rect.bottom - self.rect.top):
                        self.closest_top = platf

            if self.closest_bottom is not None:
                if (self.movementy > 0 and self.rect.bottom - 5 <= self.closest_bottom.rect.top) and not (
                        self.rect.left + 25 > self.closest_bottom.rect.right) and not (
                        self.rect.right - 25 < self.closest_bottom.rect.left):
                    self.rect.bottom = self.closest_bottom.rect.top + 1
                    self.isonground = True
                    self.movementy = 0

            if self.closest_left is not None:
                if self.rect.left + 25 > self.closest_left.rect.right:
                    self.isonground = False
                if self.closest_left.block:
                    if self.rect.left + 25 < self.closest_left.rect.right < self.rect.right and self.rect.bottom > self.closest_left.rect.top + 1:
                        self.blockleft = True

            if self.closest_right is not None:
                if self.rect.right - 25 < self.closest_right.rect.left:
                    self.isonground = False
                if self.closest_right.block:
                    if self.rect.right - 25 > self.closest_right.rect.left > self.rect.left and self.rect.bottom > self.closest_right.rect.top + 1:
                        self.blockright = True

            if self.closest_top is not None:
                if self.closest_top.block:
                    if self.rect.top <= self.closest_top.rect.bottom <= self.rect.top + 5 and self.rect.bottom >= self.closest_top.rect.bottom and self.movementy < 0:
                        self.movementy = -self.movementy

            if self.do_jump:
                self.jump()

            if not (self.isfiring and self.isonground):
                if self.go_left and self.go_right:
                    self.movementx = 0
                elif self.go_left and not self.blockleft:
                    self.movementx = -5
                    self.blockright = False
                elif self.go_right and not self.blockright:
                    self.movementx = 5
                    self.blockleft = False
                else:
                    self.movementx = 0
            else:
                self.movementx = 0

            self.rect.x += self.movementx
            self.rect.y += self.movementy

            if self.rect.left + 75 <= 0:
                self.game.current_level.prevsublevel()
                self.rect.left = self.game.screen.get_width() - 75

            if self.rect.right - 75 >= self.game.screen.get_width():
                self.game.current_level.nextsublevel()
                self.rect.left = -25


class Wizard(Player):
    def __init__(self, game):
        super().__init__(resources.images['wizard']['idle']['0'], game)
        self.resources = 'wizard'
        self.addtoeq(Weapon('charge', 0, 20, 250))
        self.currentweapon = self.eq[0]


class Viking(Player):
    def __init__(self, game):
        super().__init__(resources.images['viking']['idle']['0'], game)
        self.resources = 'viking'
        self.addtoeq(Weapon('axe', 0, 50, 1000))
        self.currentweapon = self.eq[0]
