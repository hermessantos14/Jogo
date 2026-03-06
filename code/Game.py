import pygame

from code.Const import WIN_WIDTH, MENU_OPTIONS
from code.Const import WIN_HEIGHT
from code.Level import Level
from code.Menu import Menu
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):

        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTIONS[0]:
                level = Level(self.window, 'Nível 1')
                level.run()


            elif menu_return == MENU_OPTIONS[1]:
                pygame.quit()
                sys.exit()
            else:
                pass
