import time
import pygame as pygame
pygame.font.init()


class Game:

    def __init__(self):
        # system
        self.width = 1100
        self.height = 800
        self.window = pygame.display.set_mode((self.width, self.height))
        self.timer = time.time()
        self.font = pygame.font.SysFont('comicsans', 70)

        self.path = []

    def run(self):
        """
        game loop
        :return: None
        """

        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if event.key == pygame.K_F1:
                        print(self.path)
                    if event.key == pygame.K_F2:
                        self.path = []

                    if keys[pygame.K_LCTRL] and keys[pygame.K_z]:
                        self.path.pop()

            pressed = any(pygame.mouse.get_pressed(3))
            if pressed:
                x, y = pygame.mouse.get_pos()
                x //= 60;
                y //= 60
                if not len(self.path) or (x, y) != self.path[-1]:
                    self.path.append((x, y))

            self.draw()
            clock.tick(60)

        pygame.quit()

    def draw(self):
        tile_size = 60

        self.window.fill((98, 98, 200))

        drawn = []
        for tile_coord in self.path:
            x, y = tile_coord
            x *= tile_size
            y *= tile_size

            rect_2d = pygame.Rect(x, y, tile_size, tile_size)
            if (x, y) in drawn:
                pygame.draw.rect(self.window, (110, 100, 92), rect_2d)
            else:
                pygame.draw.rect(self.window, (90, 80, 72), rect_2d)

            drawn += [(x, y)]

        # draw grid
        for x in range(0, self.width, 60):
            pygame.draw.line(self.window, (0, 0, 0), (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 60):
            pygame.draw.line(self.window, (0, 0, 0), (0, y), (self.width, y), 1)

        pygame.display.flip()


print("F1: print path")
print("F2: restart")
print("CTRL Z exists")
game = Game()
game.run()
