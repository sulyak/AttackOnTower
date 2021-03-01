import os
import time

import pygame as pygame

pygame.font.init()

from enemies.square import Square
from towers.archertower import STDTower, STDCalloc
from towers.supporttower import SUPDmg, SUPRange
from menu.menu import VerticalMenu

lives_img = pygame.image.load(os.path.join('assets', 'heart.png'))
lives_img = pygame.transform.scale(lives_img, (60, 60))

coin_img = pygame.image.load(os.path.join('assets', 'money.png'))
coin_img = pygame.transform.scale(coin_img, (45, 45))

# menu imgs
vmenu_bg = pygame.Surface((100, 600))
vmenu_bg.fill((151, 111, 85))
pygame.draw.rect(vmenu_bg, (0, 0, 0), (0, 0, 101, 600), 2)

# menu img
buy_std_tower = pygame.image.load(os.path.join('assets', 'buy_std_tower.png'))
buy_std_calloc = pygame.image.load(os.path.join('assets', 'buy_std_calloc.png'))
buy_sup_range = pygame.image.load(os.path.join('assets', 'buy_sup_range.png'))
buy_sup_dmg = pygame.image.load(os.path.join('assets', 'buy_sup_dmg.png'))

# attack towers names
attack_towers_names = ['std::tower', 'std::calloc']
support_towers_names = ['sup::range', 'sup::dmg']


class Game:

    def __init__(self):
        # system
        self.width = 1310
        self.height = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Attack on Tower')
        self.timer = time.time()
        self.font = pygame.font.SysFont('comicsans', 65)

        # towers
        self.towers_attack = []
        self.towers_support = []
        self.towers_selected = None

        # enemies
        self.enemies = []

        # world
        self.path = [(-1, 4), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 3), (5, 2), (5, 1), (4, 1), (3, 1),
                     (2, 1),
                     (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (3, 11), (4, 11),
                     (5, 11), (5, 10), (5, 9), (5, 8), (6, 8), (7, 8), (8, 8), (8, 9), (8, 10), (8, 11), (9, 11),
                     (10, 11), (11, 11), (11, 10), (11, 9), (11, 8), (12, 8), (13, 8), (14, 8), (14, 9), (14, 10),
                     (14, 11), (15, 11), (16, 11), (17, 11), (17, 10), (17, 9), (17, 8), (17, 7), (17, 6), (17, 5),
                     (17, 4), (17, 3), (16, 3), (15, 3), (14, 3), (13, 3), (12, 3), (11, 3), (10, 3), (9, 3), (8, 3),
                     (8, 4), (8, 5), (8, 6), (9, 6), (10, 6), (11, 6), (11, 5), (11, 4), (11, 3), (11, 2), (11, 1),
                     (11, 0)]
        self.lives = 3
        self.money = 20000

        # menu
        self.moving_object = None
        self.menu = VerticalMenu(self.width - vmenu_bg.get_width(), 200, vmenu_bg)
        self.menu.add_item_button(buy_std_tower, 'std::tower', 100)
        self.menu.add_item_button(buy_std_calloc, 'std::calloc', 150)
        self.menu.add_item_button(buy_sup_dmg, 'sup::dmg', 200)
        self.menu.add_item_button(buy_sup_range, 'sup::range', 250)

    def run(self):
        """
        game loop
        :return: None
        """

        running = True
        clock = pygame.time.Clock()
        while running:

            # generate enemies
            if time.time() - self.timer >= 1.5:
                self.timer = time.time()
                self.enemies.append(Square(self.path))

            # main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # hack
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    self.enemies.append(Square(self.path))

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos

                    # if you are moving an object and click
                    if self.moving_object:
                        if self.moving_object.name in attack_towers_names:
                            self.towers_attack.append(self.moving_object)
                        elif self.moving_object.name in support_towers_names:
                            self.towers_support.append(self.moving_object)
                        self.moving_object.moving = False
                        self.moving_object = None
                    else:
                        # look if you clicked on side menu
                        side_menu_button = self.menu.get_clicked(x, y)
                        if side_menu_button:
                            self.add_tower(side_menu_button)

                        # look if you clicked on attack tower or support tower
                        button_clicked = None
                        if self.towers_selected:
                            button_clicked = self.towers_selected.menu.get_clicked(x, y)
                            if button_clicked:
                                if button_clicked == 'upgrade':
                                    tw = self.towers_selected
                                    if tw.level < tw.max_level and tw.price[tw.level] <= self.money:
                                        self.money -= tw.price[tw.level]
                                        self.towers_selected.upgrade()

                                if button_clicked == 'sell':
                                    if self.towers_selected in self.towers_attack:
                                        self.towers_attack.remove(self.towers_selected)
                                    if self.towers_selected in self.towers_support:
                                        self.towers_support.remove(self.towers_selected)
                                    self.money += self.towers_selected.sell()

                        if not button_clicked:
                            for tower in self.towers_attack:
                                if tower.click(x, y):
                                    tower.selected = True
                                    self.towers_selected = tower
                                else:
                                    tower.selected = False
                            for tower in self.towers_support:
                                if tower.click(x, y):
                                    tower.selected = True
                                    self.towers_selected = tower
                                else:
                                    tower.selected = False

            # check for moving object (menu selected)
            pos = pygame.mouse.get_pos()
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])

            # loop through enemies
            for enemy in self.enemies:
                enemy.move()
                if enemy.path_count == len(enemy.path) - 1:
                    self.enemies.remove(enemy)
                    self.lives -= 1

            # loop through towers
            for tower in self.towers_attack:
                self.money += tower.attack(self.enemies)
            for tower in self.towers_support:
                tower.support(self.towers_attack)

            # if you loose
            if self.lives <= 0:
                print('vc perdeu')
                running = False

            self.draw()
            clock.tick(60)

        pygame.quit()

    def draw(self):
        """
        draw the grid + path
        :return:
        """
        tile_size = 60

        self.window.fill((98, 98, 200))

        # draw the tiles
        for tile_coord in self.path:
            x, y = tile_coord
            xx = x * tile_size
            yy = y * tile_size

            rect_2d = pygame.Rect(xx, yy, tile_size, tile_size)
            pygame.draw.rect(self.window, (90, 80, 72), rect_2d)

            if (x + 1, y) not in self.path:
                pygame.draw.line(self.window, (0, 0, 0), (xx + 60, yy + 60), (xx + 60, yy), 3)
            if (x - 1, y) not in self.path:
                pygame.draw.line(self.window, (0, 0, 0), (xx, yy), (xx, yy + 60), 3)
            if (x, y + 1) not in self.path:
                pygame.draw.line(self.window, (0, 0, 0), (xx, yy + 60), (xx + 60, yy + 60), 3)
            if (x, y - 1) not in self.path:
                pygame.draw.line(self.window, (0, 0, 0), (xx, yy), (xx + 60, yy), 3)

        # draw enemies
        for enemy in self.enemies:
            enemy.draw(self.window)

        # draw attack towers
        for tower in self.towers_attack:
            tower.draw(self.window)
        # draw support towers
        for tower in self.towers_support:
            tower.draw(self.window)

        # draw lives
        text = self.font.render(str(self.lives), True, (0, 0, 0))
        start_x = self.width - lives_img.get_width()

        self.window.blit(text, (start_x - text.get_width() - 10, 15))
        self.window.blit(lives_img, (start_x, 10))

        # draw currency
        text = self.font.render(str(self.money), True, (0, 0, 0))
        start_x = self.width - coin_img.get_width() - 3

        self.window.blit(text, (start_x - text.get_width() - 10, 82))
        self.window.blit(coin_img, (start_x, 80))

        # draw menu
        self.menu.draw(self.window)

        # draw moving object
        if self.moving_object:
            self.moving_object.draw(self.window)

        pygame.display.flip()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ['std::tower', 'std::calloc', 'sup::range', 'sup::dmg']
        object_list = [STDTower(x, y), STDCalloc(x, y), SUPRange(x, y), SUPDmg(x, y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + " not valid name.")


game = Game()
game.run()
