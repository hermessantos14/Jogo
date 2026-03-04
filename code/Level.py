import pygame
from code.Background import Background
from code.Const import WIN_HEIGHT


class Level:

    def __init__(self, window, name):
        self.window = window
        self.name = name

        from code.Const import WIN_WIDTH

        self.bg1 = Background('/pista1', (0, 0), 5)
        self.bg2 = Background('/pista2', (WIN_WIDTH, 0), 5)

    def run(self):

        clock = pygame.time.Clock()

        while True:

            clock.tick(60)

            # mover pista
            self.bg1.move()
            self.bg2.move()

            # reset infinito
            if self.bg1.rect.right <= 0:
                self.bg1.rect.left = self.bg2.rect.right

            if self.bg2.rect.right <= 0:
                self.bg2.rect.left = self.bg1.rect.right

            # desenhar
            self.window.blit(self.bg1.surf, self.bg1.rect)
            self.window.blit(self.bg2.surf, self.bg2.rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
