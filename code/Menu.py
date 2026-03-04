import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from code.Const import MENU_OPTIONS, C_WHITE, MENU_INFO, MENU_GOALS


class Menu():
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/background_menu2.png')
        self.rect = self.surf.get_rect(left = 0, top = 0)

    def run(self):

        pygame.mixer.music.load('./asset/Intro.wav')
        pygame.mixer.music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            for i in range(len(MENU_OPTIONS)):
                self.menu_text(text_size=40,  text=MENU_OPTIONS[i],  text_color=C_WHITE, text_center_pos=(580, 200 + 50*i))

            for i in range(len(MENU_INFO)):
                self.menu_text(text_size=20, text=MENU_INFO[i], text_color=C_WHITE, text_center_pos=(580, 310 + 28 * i))

            for i in range(len(MENU_GOALS)):
                self.menu_text(text_size=20, text=MENU_GOALS[i], text_color=C_WHITE, text_center_pos=(450, 530 + 25 * i))

            pygame.display.flip()

            # check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # fecha a janela do jogo
                    quit()  # encerra o pygame

    # para texto do menu
    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

