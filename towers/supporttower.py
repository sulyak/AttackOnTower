import math
import pygame
from towers.tower import Tower

range_img = pygame.Surface((60, 60))
range_img.fill((255, 247, 135))
range_imgs = [range_img]


class SUPRange(Tower):
    """
    add extra range to each surrounding tower
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = self.height = 60
        self.range = 150
        self.tower_imgs = range_imgs[:]
        self.effect = [.2, .5]
        self.price = [100, 200, 500]
        self.sell_price = [80, 160, 400]
        self.max_level = 3
        self.archer_delay = 12
        self.name = 'sup::range'

    def draw(self, surface):
        super().draw_radius(surface)
        super().draw(surface)

    def support(self, towers):
        effected = []
        for tower in towers:
            dis = math.sqrt((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2)
            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.base_range * (1 + self.effect[self.level])


dmg_img = pygame.Surface((60, 60))
dmg_img.fill((255, 170, 70))
dmg_imgs = [dmg_img]


class SUPDmg(Tower):
    """
    add dmg to surrounding towers
    """

    def __init__(self, x, y):
        super().__init__(x, y)

        self.width = self.height = 60
        self.range = 150
        self.effect = [1, 2]
        self.price = [100, 500]
        self.sell_price = [80, 400]
        self.max_level = 2
        self.name = 'sup::dmg'
        self.tower_imgs = dmg_imgs[:]

    def draw(self, surface):
        super().draw_radius(surface)
        super().draw(surface)

    def support(self, towers):
        effected = []
        for tower in towers:
            dis = math.sqrt((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2)
            if dis < self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.base_damage * (1 + self.effect[self.level - 1])
