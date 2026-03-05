import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface
from code.Const import MENU_OPTIONS, C_WHITE, MENU_INFO, MENU_GOALS, C_GREEN


class Menu():
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/background_menu2.png').convert_alpha()
        self.rect = self.surf.get_rect(left = 0, top = 0)

    def run(self):
        #carrega musica intro
        pygame.mixer.music.load('./asset/Intro.wav')
        pygame.mixer.music.play(-1)
        menu_option = 0
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            # fundo semi-transparente para o menu
            menu_bg = pygame.Surface((320, 140))
            menu_bg.set_alpha(130)  # transparência
            menu_bg.fill((0, 0, 0))

            bg_rect = menu_bg.get_rect(center=(560, 225))
            self.window.blit(menu_bg, bg_rect)


            for i in range(len(MENU_OPTIONS)):
                if i == menu_option:
                    self.menu_text(text_size=40, text=MENU_OPTIONS[i], text_color=C_GREEN,text_center_pos=(560, 200 + 50 * i))
                else:
                    self.menu_text(text_size=40,  text=MENU_OPTIONS[i],  text_color=C_WHITE, text_center_pos=(560, 200 + 50*i))

            for i in range(len(MENU_INFO)):
                self.menu_text(text_size=20, text=MENU_INFO[i], text_color=C_WHITE, text_center_pos=(560, 350 + 28 * i))

            for i in range(len(MENU_GOALS)):
                self.menu_text(text_size=20, text=MENU_GOALS[i], text_color=C_WHITE, text_center_pos=(450, 530 + 25 * i))



            # check for all events
            # close event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # fecha a janela do jogo
                    quit()  # encerra o pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: #check down key
                        if menu_option < len(MENU_OPTIONS) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP: #check up key
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTIONS) - 1
                    if event.key == pygame.K_RETURN:  # check enter key
                        return MENU_OPTIONS[menu_option]


            pygame.display.flip()
    # para texto do menu
    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

