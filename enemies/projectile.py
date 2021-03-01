import math

import pygame


class Projectile:

    def __init__(self, origin, enemy, dmg):
        self.x, self.y = origin
        self.origin = origin
        self.enemy = enemy
        self.dead = False
        self.speed = 10
        self.dmg = dmg

    def draw(self, surface):
        rect_2d = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(surface, (100, 0, 0), rect_2d)
        self.move()

    def move(self):
        """
        Move enemy
        :return: None
        """

        x1, y1 = self.origin
        x2, y2 = self.enemy.x + self.enemy.width / 2, self.enemy.y + self.enemy.height / 2

        dirn = ((x2 - x1), (y2 - y1))
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length * self.speed, dirn[1] / length * self.speed)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.x, self.y = move_x, move_y

        if self.enemy.collide(self.x, self.y):
            self.dead = True
            self.enemy.hit(self.dmg)
