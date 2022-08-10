import random
import pygame.sprite
import resources


class Level:
    def __init__(self):
        self.sublevels = []
        pygame.mixer.music.load('music/' + self.music + '.mp3')
        pygame.mixer.music.play(-1)
        self.current_sublevel = None

    def prevsublevel(self):
        self.current_sublevel = self.sublevels[self.sublevels.index(self.current_sublevel) - 1]

    def nextsublevel(self):
        self.current_sublevel = self.sublevels[self.sublevels.index(self.current_sublevel) + 1]


class SubLevel:
    def __init__(self, image):
        self.walls = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.decors = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.background = image
        self.gate = None

    def addParticle(self, particle):
        self.particles.add(particle)

    def addDecor(self, decor):
        self.decors.add(decor)

    def addPlatform(self, platform):
        self.platforms.add(platform)

    def addItem(self, item):
        self.items.add(item)

    def addEnemy(self, enemy):
        self.enemies.add(enemy)

    def display(self, surf, game):
        surf.blit(self.background, (0, 0))

        if self.gate is not None:
            surf.blit(self.gate.image, self.gate.rect)

        for x in self.decors:
            surf.blit(x.image, x.rect)

        for x in self.platforms:
            surf.blit(x.image, x.rect)

        for x in self.items:
            if not game.is_paused:
                x.animate()
            surf.blit(x.image, x.rect)

        for x in self.enemies:
            x.draw(surf, game.is_paused)

        for x in self.particles:
            if not game.is_paused:
                colliding_enemies = pygame.sprite.spritecollide(x, self.enemies, False)
                for enemy in colliding_enemies:
                    enemy.takedamage(x.damage)
                    x.kill()
            x.draw(surf, game.is_paused)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, life):
        super().__init__()
        self.last_update = 0
        self.last_update_attack = 0
        self.isreversing = False
        self.image = image
        self.turnright = False
        self.rect = self.image.get_rect()
        self.life = life
        self.attack = False
        self.count = 0

    def update(self):
        if not self.attack:
            if self.turnright:
                self.rect.x += self.movement
            else:
                self.rect.x -= self.movement

        if self.rect.x <= self.left:
            self.turnright = True
        elif self.rect.x >= self.right:
            self.turnright = False

    def draw(self, surface, paused):
        if not paused:
            self.update()

            if self.attack:
                if self.turnright:
                    self.animate(resources.images['ogre']['attack']['right'], self.attackspeed, False, False)
                else:
                    self.animate(resources.images['ogre']['attack']['left'], self.attackspeed, False, False)
            else:
                if self.turnright:
                    self.animate(resources.images['ogre']['walk']['right'], self.walkspeed, False, False)
                else:
                    self.animate(resources.images['ogre']['walk']['left'], self.walkspeed, False, False)

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
                if self.count == len(animation) - 1:
                    self.count = 0
                else:
                    self.count += 1

            self.last_update = pygame.time.get_ticks()

    def takedamage(self, damage):
        if self.life - damage <= 0:
            self.kill()
        else:
            self.life -= damage


class Decor(pygame.sprite.Sprite):
    def __init__(self, asset, x, y, flipped=False):
        super().__init__()
        if flipped:
            self.image = pygame.transform.flip(resources.images['decor'][asset]['normal'], True, False)
        else:
            self.image = resources.images['decor'][asset]['normal']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ogre(Enemy):
    def __init__(self, x, y, life, left, right):
        super().__init__(resources.images['ogre']['walk']['left']['0'], life)
        self.rect.x = x
        self.rect.y = y
        self.movement = 2
        self.sound = pygame.mixer.Sound('music/club.ogg')
        self.damage = 10
        self.left = left
        self.right = right
        self.walkspeed = 100
        self.attackspeed = 100
        self.attackframe = 6
        self.points = 500


class Item(pygame.sprite.Sprite):
    def __init__(self, asset, x, y, delay, reverse):
        super().__init__()
        self.image = resources.images['item'][asset]['0']
        self.sound = pygame.mixer.Sound('music/item_' + asset + '.ogg')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.worth = 0
        self.last_update = 0
        self.height = 20
        self.heightchanged = 0
        self.heightreverse = False
        self.count = 0
        self.type = 'money'
        self.animation = resources.images['item'][asset]
        self.delay = delay
        self.reverse = reverse
        self.isreversing = False

    def animate(self):
        self.image = self.animation[str(self.count)]
        if pygame.time.get_ticks() - self.last_update > self.delay:

            if self.heightreverse:
                self.rect.y += 1
                self.heightchanged -= 1
            else:
                self.rect.y -= 1
                self.heightchanged += 1
            if self.heightchanged == self.height:
                self.heightreverse = True
            elif self.heightchanged == 0:
                self.heightreverse = False

            if self.reverse:
                if self.count == len(self.animation) - 1:
                    self.isreversing = True
                elif self.count == 0:
                    self.isreversing = False

                if self.isreversing:
                    self.count -= 1
                else:
                    self.count += 1
            else:
                if self.count == len(self.animation) - 1:
                    self.count = 0
                else:
                    self.count += 1

            self.last_update = pygame.time.get_ticks()

    def pickup(self, game):

        def do():
            game.current_level.current_sublevel.items.remove(self)
            channel = pygame.mixer.find_channel()
            channel.set_volume(game.settings.getSetting('effects_volume') / 100)
            channel.play(self.sound)

        if self.type == 'money':
            game.player_points += self.worth
            do()
        elif self.type == 'heal':
            if game.player_life != 100:
                if game.player_life + self.worth > 100:
                    game.player_life = 100
                else:
                    game.player_life += self.worth
                do()
        elif self.type == 'key':
            game.player_gotkey = True
            do()



class Sapphire(Item):
    def __init__(self, x, y):
        super().__init__('saphire', x, y, 30, False)
        self.worth = 100

class Potion(Item):
    def __init__(self, x, y):
        super().__init__('potion', x, y, 30, False)
        self.type = 'heal'
        self.worth = 50

class Topaz(Item):
    def __init__(self, x, y):
        super().__init__('topaz', x, y, 30, False)
        self.worth = 200

class Diamond(Item):
    def __init__(self, x, y):
        super().__init__('diamond', x, y, 30, False)
        self.worth = 350

class Key(Item):
    def __init__(self, x, y):
        super().__init__('key', x, y, 30, False)
        self.type = 'key'


class Platform(pygame.sprite.Sprite):
    def __init__(self, type, sizex, sizey, x, y, block=False):
        super().__init__()
        if sizex == 1:
            self.basesize = resources.images['platform']['wall'][type].get_size()
            self.image = pygame.surface.Surface((self.basesize[0], self.basesize[1] * sizey), pygame.SRCALPHA)
            for i in range(0, sizey):
                self.image.blit(resources.images['platform']['wall'][type], (0, self.basesize[1] * i))
        else:
            self.basesize = resources.images['platform'][type]['1']['l']['normal'].get_size()
            self.image = pygame.surface.Surface((self.basesize[0] * sizex, self.basesize[1] * sizey), pygame.SRCALPHA)
            self.image.blit(resources.images['platform'][type]['1']['l']['normal'], (0, 0))
            for i in range(1, sizex - 1):
                self.image.blit(resources.images['platform'][type]['1']['m']['normal'], (self.basesize[0] * i, 0))
            self.image.blit(resources.images['platform'][type]['1']['r']['normal'], (self.basesize[0] * (sizex - 1), 0))
            for i in range(1, sizey - 1):
                self.image.blit(resources.images['platform'][type]['1']['lm']['normal'], (0, self.basesize[1] * i))
                for k in range(1, sizex - 1):
                    self.image.blit(resources.images['platform'][type]['1']['mm']['normal'],
                                    (self.basesize[0] * k, self.basesize[1] * i))
                self.image.blit(resources.images['platform'][type]['1']['rm']['normal'],
                                (self.basesize[0] * (sizex - 1), self.basesize[1] * i))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.block = block

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = resources.images['gate']['winter']['close']['normal']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def open(self):
        self.image = resources.images['gate']['winter']['open']['normal']

class Snowland(Level):
    def __init__(self):
        self.music = 'winter'
        super().__init__()
        self.sublevels.append(SubLevel(resources.images['snowland']['bg']['2']))

        self.sublevels[-1].addPlatform(Platform('snow', 1, 15, -30, 0, True))
        self.sublevels[-1].addPlatform(Platform('snow', 13, 5, -10, 450, True))
        self.sublevels[-1].gate = Gate(250, 114)
        self.sublevels[-1].addEnemy(Ogre(50, 340, 100, 10, 650))
        self.sublevels[-1].addEnemy(Ogre(400, 340, 100, 10, 650))
        self.sublevels[-1].addEnemy(Ogre(750, 340, 100, 10, 650))
        self.sublevels[-1].addDecor(Decor('icepillar1', 50, 420))
        self.sublevels[-1].addDecor(Decor('icepillar3', 50, 388))
        self.sublevels[-1].addItem(Diamond(80, 348))
        self.sublevels[-1].addDecor(Decor('icepillar1', 150, 420))
        self.sublevels[-1].addDecor(Decor('icepillar2', 150, 388))
        self.sublevels[-1].addDecor(Decor('icepillar2', 150, 356))
        self.sublevels[-1].addDecor(Decor('icepillar2', 150, 324))
        self.sublevels[-1].addDecor(Decor('icepillar3', 150, 292))
        self.sublevels[-1].addItem(Diamond(180, 252))
        self.sublevels[-1].addDecor(Decor('icepillar1', 600, 420))
        self.sublevels[-1].addDecor(Decor('icepillar3', 600, 388))
        self.sublevels[-1].addItem(Diamond(630, 348))
        self.sublevels[-1].addDecor(Decor('icepillar1', 500, 420))
        self.sublevels[-1].addDecor(Decor('icepillar2', 500, 388))
        self.sublevels[-1].addDecor(Decor('icepillar2', 500, 356))
        self.sublevels[-1].addDecor(Decor('icepillar2', 500, 324))
        self.sublevels[-1].addDecor(Decor('icepillar3', 500, 292))
        self.sublevels[-1].addItem(Diamond(530, 252))
        self.sublevels[-1].addDecor(Decor('snow1', 0, 434))
        self.sublevels[-1].addDecor(Decor('snow2', 90, 418))
        self.sublevels[-1].addDecor(Decor('snow3', 250, 418))
        self.sublevels[-1].addDecor(Decor('snow1', 400, 434))
        self.sublevels[-1].addDecor(Decor('snow2', 490, 418))
        self.sublevels[-1].addDecor(Decor('snow3', 650, 418))

        self.sublevels.append(SubLevel(resources.images['snowland']['bg']['2']))
        self.sublevels[-1].addPlatform(Platform('snow', 8, 7, 350, 350, True))
        self.sublevels[-1].addPlatform(Platform('snow', 6, 5, -10, 450, True))
        self.sublevels[-1].addEnemy(Ogre(650, 240, 100, 350, 700))
        self.sublevels[-1].addItem(Sapphire(400, 300))
        self.sublevels[-1].addItem(Topaz(700, 300))
        self.sublevels[-1].addDecor(Decor('wintertree1', -50, 230))
        self.sublevels[-1].addDecor(Decor('wintertree1', -20, 150))
        self.sublevels[-1].addDecor(Decor('wintertree1', 10, 230))
        self.sublevels[-1].addDecor(Decor('house', 50, 230))
        self.sublevels[-1].addDecor(Decor('house', 450, 130, True))
        self.sublevels[-1].addDecor(Decor('snowman', 370, 230, True))
        self.sublevels[-1].addDecor(Decor('winterfence1', 0, 400))
        self.sublevels[-1].addDecor(Decor('winterfence4', 64, 400))
        self.sublevels[-1].addDecor(Decor('winterfence2', 300, 400))
        self.sublevels[-1].addDecor(Decor('winterfence2', 360, 300))
        self.sublevels[-1].addDecor(Decor('winterfence4', 424, 300))
        self.sublevels[-1].addDecor(Decor('winterfence1', 600, 300))
        self.sublevels[-1].addDecor(Decor('winterfence4', 664, 300))
        self.sublevels[-1].addDecor(Decor('winterfence3', 728, 300))
        self.sublevels[-1].addDecor(Decor('snow1', 0, 434))
        self.sublevels[-1].addDecor(Decor('snow2', 90, 418))
        self.sublevels[-1].addDecor(Decor('snow3', 250, 418))
        self.sublevels[-1].addDecor(Decor('snow2', 360, 318))
        self.sublevels[-1].addDecor(Decor('snow3', 450, 318))
        self.sublevels[-1].addDecor(Decor('snow1', 600, 334))
        self.sublevels[-1].addDecor(Decor('snow3', 700, 318))

        self.sublevels.append(SubLevel(resources.images['snowland']['bg']['2']))
        self.sublevels[-1].addPlatform(Platform('snow', 6, 7, -10, 350, True))
        self.sublevels[-1].addPlatform(Platform('snow', 8, 5, 350, 450, True))
        self.sublevels[-1].addPlatform(Platform('snow', 4, 1, 450, 250, True))
        self.sublevels[-1].addDecor(Decor('house', 50, 130))
        self.sublevels[-1].addDecor(Decor('barrels', 0, 290))
        self.sublevels[-1].addDecor(Decor('winterfence2', 0, 300))
        self.sublevels[-1].addDecor(Decor('winterfence4', 64, 300))
        self.sublevels[-1].addDecor(Decor('winterfence3', 300, 300))
        self.sublevels[-1].addDecor(Decor('icerod2', 450, 280))
        self.sublevels[-1].addDecor(Decor('icerod2', 578, 280))
        self.sublevels[-1].addDecor(Decor('stump1', 600, 420))
        self.sublevels[-1].addDecor(Decor('stump3', 600, 406))
        self.sublevels[-1].addDecor(Decor('snowman', 450, 330, True))
        self.sublevels[-1].addItem(Potion(615, 370))
        self.sublevels[-1].addDecor(Decor('wintertree2', 350, 0))
        self.sublevels[-1].addItem(Sapphire(500, 200))
        self.sublevels[-1].addItem(Topaz(600, 200))
        self.sublevels[-1].addItem(Diamond(550, 150))
        self.sublevels[-1].addDecor(Decor('wintertotem1', 550, 140))
        self.sublevels[-1].addEnemy(Ogre(250, 240, 100, 10, 300))
        self.sublevels[-1].addEnemy(Ogre(650, 340, 100, 400, 700))
        self.sublevels[-1].addDecor(Decor('snow1', 400, 434))
        self.sublevels[-1].addDecor(Decor('snow2', 490, 418))
        self.sublevels[-1].addDecor(Decor('snow3', 650, 418))

        self.sublevels.append(SubLevel(resources.images['snowland']['bg']['2']))
        self.sublevels[-1].addPlatform(Platform('snow', 1, 15, 770, 0, True))
        self.sublevels[-1].addPlatform(Platform('snow', 13, 5, -10, 450, True))
        self.sublevels[-1].addPlatform(Platform('snow', 2, 1, 600, 150, True))
        self.sublevels[-1].addPlatform(Platform('snow', 2, 1, 600, 350, True))
        self.sublevels[-1].addPlatform(Platform('snow', 1, 6, 130, 70, True))
        self.sublevels[-1].addPlatform(Platform('snow', 5, 1, 150, 250, True))
        self.sublevels[-1].addItem(Key(650, 100))
        self.sublevels[-1].addEnemy(Ogre(50, 340, 100, 10, 650))
        self.sublevels[-1].addEnemy(Ogre(400, 340, 100, 10, 650))
        self.sublevels[-1].addEnemy(Ogre(750, 340, 100, 10, 650))
        self.sublevels[-1].addEnemy(Ogre(250, 140, 100, 200, 350))
        self.sublevels[-1].addDecor(Decor('snow1', 0, 434))
        self.sublevels[-1].addDecor(Decor('snow2', 90, 418))
        self.sublevels[-1].addDecor(Decor('snow3', 250, 418))
        self.sublevels[-1].addDecor(Decor('snow1', 400, 434))
        self.sublevels[-1].addDecor(Decor('snow2', 490, 418))
        self.sublevels[-1].addDecor(Decor('snow3', 650, 418))

        self.current_sublevel = self.sublevels[1]
        self.startpoint = (180, 371)


class Dungeon(Level):
    def __init__(self):
        self.music = 'castle'
        super().__init__()
        self.sublevels.append(SubLevel(resources.images['snowland']['bg']['2']))
        self.current_sublevel = self.sublevels[0]
