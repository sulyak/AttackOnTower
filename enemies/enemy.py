import pygame


class Enemy:
    imgs = []

    def __init__(self, path):
        self.width = 0
        self.height = 0
        self.health = 0
        self.max_health = 0
        self.gold = 0

        self.img = None
        self.animation_count = 0
        self.path = path

        new_path = []
        for tile in self.path:
            new_position = ()
            for position in tile:
                new_position += tuple([position * 60])
            new_path += [new_position]
        self.path = new_path

        self.path_count = 0
        self.x, self.y = self.path[0]

    def draw(self, surface):
        """
        Draw an enemy to a surface
        :param surface: Surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]
        self.animation_count = (self.animation_count + 1) % len(self.imgs)

        x_diff = 60 - self.img.get_width()
        y_diff = 60 - self.img.get_height()
        surface.blit(self.img, (self.x + x_diff // 2, self.y + y_diff // 2))

        self.draw_health_bar(surface)

    def move(self):
        """
        Move enemy
        :return: None
        """

        """ ao inves de teletransportar quadrado a quadrado, reduzo o espaco entre os quadrados 
        (nesse caso a 1) dividindo o tamanho dele por ele
        """
        # todo fix this mess

        if self.path_count == len(self.path) - 1: return
        x1, y1 = self.path[self.path_count]
        x2, y2 = self.path[self.path_count + 1]

        dirn = (x2 - x1) * 2, (y2 - y1) * 2  # speed *2 *3 *4 etc
        # length = self.width
        length = 60
        dirn = (dirn[0] / length, dirn[1] / length)

        move_x, move_y = self.x + dirn[0], self.y + dirn[1]

        self.x, self.y = move_x, move_y

        # indo ao proximo ponto
        # Go to next point
        if dirn[0] >= 0:  # moving right
            if dirn[1] >= 0:  # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_count += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_count += 1
        else:  # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_count += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_count += 1

        if self.path_count >= len(self.path):
            pass

    def draw_health_bar(self, surface):
        length = 60
        move = round(length / self.max_health)
        health_bar = move * self.health

        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y - 15, length, 10), 0)
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y - 15, health_bar, 10), 0)

        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y - 15, length, 10), width=1)
        x = self.x
        for i in range(self.health):
            pygame.draw.rect(surface, (0, 0, 0), (x, self.y - 15, move, 10), width=1)
            x += move

    def collide(self, x, y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y: int
        :return:  bool
        """

        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                return True

        return False

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False
