import os
import pygame
from menu.menu import TowerMenu

upgrade_button = pygame.image.load(os.path.join('assets', 'upgrade.png'))
upgrade_button = pygame.transform.scale(upgrade_button, (20, 20))
sell_button = pygame.image.load(os.path.join('assets', 'sell.png'))
sell_button = pygame.transform.scale(sell_button, (20, 20))


class Tower:
    """
    Abstract class for tower
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0

        self.base_damage = self.damage = 1
        self.sell_price = []
        self.price = []
        self.level = 0
        self.max_level = 0

        self.selected = False

        # menu stuff
        self.moving = False
        self.tower_imgs = []
        self.menu = TowerMenu(self)
        self.menu.add_item_button(upgrade_button, 'upgrade')
        self.menu.add_item_button(sell_button, 'sell')

    def draw(self, surface):
        # img = self.tower_imgs[self.level] # todo multiple tower images for diff levels
        img = self.tower_imgs[0]
        surface.blit(img, (self.x - img.get_width() / 2, self.y - img.get_height() / 2))

        if self.selected:
            self.menu.draw(surface)

    def draw_radius(self, surface):
        # draw range
        if self.selected or self.moving:
            circle_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(circle_surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)
            surface.blit(circle_surface, (self.x - self.range, self.y - self.range))

    def click(self, x, y):
        """
        returns if tower has been clicked on
        and select tower if it was clicked
        :param x: int
        :param y: int
        :return: bool
        """
        if self.x - self.width // 2 <= x <= self.x + self.width // 2:
            if self.y - self.height // 2 <= y <= self.y + self.height // 2:
                return True

        return False

    def sell(self):
        """
        sell the tower, return sell price
        :return: int
        """
        return self.sell_price[self.level]

    def upgrade(self):
        """
        upgrade the tower for a given cost
        :return:
        """
        if self.level < self.max_level:
            self.level += 1
            self.base_damage += 1

    def get_upgrade_cost(self):
        """
        returns the upgrade cost if 0 can't upgrade anymore
        """
        return self.sell_price[self.level]

    def move(self, x, y):
        """
        move the tower to the mouse position
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
