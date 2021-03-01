import math
import time
import pygame

from enemies.projectile import Projectile
from towers.tower import Tower


class STDTower(Tower):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.width = self.height = 60
        self.range = self.base_range = 200
        self.damage, self.base_damage = 1, 1
        self.price = [100, 200, 500]
        self.sell_price = [80, 160, 400]
        self.max_level = 3
        self.archer_delay = 12
        self.name = 'std::tower'

        self.tower_imgs = []
        self.archer_imgs = []
        self.projectiles = []
        self.archer_count = 0
        self.in_range = False

        archer_img = pygame.Surface((30, 30))
        archer_img.fill((255, 0, 0))
        self.archer_imgs += [archer_img]
        archer_img = pygame.Surface((25, 25))
        archer_img.fill((255, 0, 0))
        self.archer_imgs += [archer_img]

        tower_img = pygame.Surface((60, 60))
        tower_img.fill((0, 255, 0))
        self.tower_imgs += [tower_img]

    def draw(self, surface):
        # draw range
        super().draw_radius(surface)
        super().draw(surface)

        # animation steps
        if self.in_range and not self.moving:
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * self.archer_delay:
                self.archer_count = 0
        else:
            self.archer_count = 0

        # draw the archer on top of tower
        archer = self.archer_imgs[self.archer_count // self.archer_delay]
        surface.blit(archer, (self.x - archer.get_width() / 2, self.y - archer.get_height() / 2))

        # draw projectiles
        for projectile in self.projectiles:
            projectile.draw(surface)

    def change_range(self, range):
        """
        changes the range
        :param range: int
        :return: None
        """
        self.range = range

    def attack(self, enemies):
        """
        attack enemies on enemy list
        :param enemies: list of Enemy
        :return: None
        """
        money_earned = 0

        self.in_range = False
        enemy_closest = []
        for enemy in enemies:
            x, y = enemy.x, enemy.y

            # distance between tower and center of enemy
            dis = math.sqrt((self.x - enemy.width / 2 - x) ** 2 + (self.y - enemy.height / 2 - y) ** 2)
            if dis < self.range:
                self.in_range = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda en: en.path_count)

        if len(enemy_closest):
            first_enemy = enemy_closest[-1]
            if self.archer_count == (len(self.archer_imgs) * self.archer_delay) / 2:
                self.projectiles.append(Projectile((self.x, self.y), first_enemy, self.damage))

        for enemy in enemies:
            if enemy.health <= 0:
                money_earned += enemy.gold
                enemies.remove(enemy)

        for projectile in self.projectiles:
            if projectile.dead:
                self.projectiles.remove(projectile)

        return money_earned


class STDCalloc(STDTower):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = self.base_range = 100
        self.damage = self.base_damage = 2
        self.archer_delay = 20
        self.name = 'std::calloc'

        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = 0
        self.in_range = False
        self.timer = time.time()

        archer_img = pygame.Surface((30, 30))
        archer_img.fill((0, 255, 0))
        pygame.draw.circle(archer_img, (255, 128, 128), (15, 15), 15)
        self.archer_imgs += [archer_img]
        archer_img = pygame.Surface((30, 30))
        archer_img.fill((0, 255, 0))
        pygame.draw.circle(archer_img, (255, 128, 128), (15, 15), 10)
        self.archer_imgs += [archer_img]

        tower_img = pygame.Surface((60, 60))
        tower_img.fill((0, 255, 0))
        self.tower_imgs += [tower_img]
