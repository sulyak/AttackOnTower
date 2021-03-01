import pygame
from enemies.enemy import Enemy

imgs = []
srfc = pygame.Surface((50, 50))
srfc.fill((0, 0, 0))
imgs.append(srfc)


class Square(Enemy):

    def __init__(self, path):
        super().__init__(path)

        self.width = 50
        self.height = 50
        self.max_health = 15
        self.health = self.max_health
        self.gold = 25

        self.imgs = imgs
