import pygame

pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 16)


class ItemButton:
    def __init__(self, img, name):
        self.img = img
        self.name = name

        self.x = self.y = None
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self, x, y):
        """
        returns if the position has collided with the menu
        :param x: int
        :param y: int
        :return: bool
        """
        if self.x - self.width // 2 <= x <= self.x + self.width // 2:
            if self.y - self.height // 2 <= y <= self.y + self.height // 2:
                return True
        return False

    def draw(self, pos, surface):
        self.x, self.y = pos
        surface.blit(self.img, (self.x - self.width // 2, self.y - self.height // 2))


menu_bg = pygame.Surface((80, 30))
menu_bg.fill((90, 100, 126))
pygame.draw.rect(menu_bg, (0, 0, 0), (0, 0, 80, 30), 1)


class TowerMenu:
    def __init__(self, tower):
        self.tower = tower

        self.background_img = menu_bg
        self.width = self.background_img.get_width()
        self.height = self.background_img.get_height()

        self.item_names = []
        self.items = 0
        self.buttons = []

    def add_item_button(self, img, name):
        """
        adds buttons to menu
        :param img:
        :param name:
        :return:
        """
        self.buttons.append(ItemButton(img, name))

    def draw(self, surface):
        tower = self.tower
        x, y = tower.x, tower.y - tower.height // 2 - self.height // 2 - 5

        surface.blit(self.background_img, (x - self.width // 2, y - self.height // 2))

        step = self.width // len(self.buttons)
        btn_x = x - self.width // 2 + step // 2
        for item in self.buttons:
            item.draw((btn_x, y), surface)
            if item.name == 'upgrade':
                if self.tower.level < self.tower.max_level:
                    text = FONT.render((str(self.tower.price[self.tower.level])), True, (255, 255, 255))
                else:
                    text = FONT.render('max', True, (255, 255, 255))
                surface.blit(text, (btn_x - text.get_width() // 2, y + 3))

            btn_x += step

    def get_clicked(self, x, y):
        """
        return the clicked item from the menu
        :param x: int
        :param y: int
        :return: str
        """
        for item in self.buttons:
            if item.click(x, y):
                return item.name
        return None


class VerticalButton(ItemButton):
    def __init__(self, img, name, cost):
        super().__init__(img, name)
        self.cost = cost


class VerticalMenu:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.buttons = []
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont('comicsans', 25)

    def get_clicked(self, x, y):
        for button in self.buttons:
            if button.click(x, y):
                return button.name
        return None

    def add_item_button(self, img, name, cost):
        """
        adds buttons to menu
        :param img:
        :param name:
        :return:
        """
        self.buttons.append(VerticalButton(img, name, cost))

    def draw(self, surface):
        surface.blit(self.bg, (self.x, self.y))

        x = self.x + self.width // 2 + 2
        y = self.y + 60

        step_y = 75

        for button in self.buttons:
            button.draw((x, y), surface)

            text = FONT.render(button.name + ' ' + str(button.cost) + 'g', True, (0, 0, 0))
            surface.blit(text, (x - text.get_width() // 2, y + button.img.get_height() // 2))
            y += step_y
