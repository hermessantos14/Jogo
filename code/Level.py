import pygame
import random
from code.Background import Background
from code.Player import Player
from code.Dumpster import Dumpster
from code.Spike import Spike
from code.Radioactive import Radioactive
from code.Const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTIONS, C_GREEN, C_WHITE, NUM_DUMPSTER


class Level:

    def __init__(self, window, name):

        self.window = window
        self.name = name

        self.game_over = False
        self.slowdown = False
        self.gameover_alpha = 0

        self.win = False
        self.win_alpha = 0

        self.dumpsters_collected = 0
        self.dumpsters_target = NUM_DUMPSTER

        self.spikes = []
        self.barrels = []

        self.max_obstacles = 3
        self.last_obstacle = "spike"

        self.dumpsters = [
            Dumpster('/dumpster1', (950, 150)),
            Dumpster('/dumpster2', (1200, 350)),
            Dumpster('/dumpster3', (1500, 250)),
            Dumpster('/dumpster4', (1800, 450))
        ]

        self.bg1 = Background('/pista1', (0, 0), 5)
        self.bg2 = Background('/pista2', (WIN_WIDTH, 0), 5)

        self.player = Player((120, 300))

        self.engine_sound = pygame.mixer.Sound('./asset/truck_engine.wav')
        self.collect_sound = pygame.mixer.Sound('./asset/garbage_collection.wav')
        self.blowout_sound = pygame.mixer.Sound('./asset/blowout.wav')
        self.explosion_sound = pygame.mixer.Sound('./asset/explosion.wav')
        self.gameover_sound = pygame.mixer.Sound('./asset/game_over.wav')
        self.win_sound = pygame.mixer.Sound('./asset/winning.wav')

        # som do contador
        self.counter_sound = pygame.mixer.Sound('./asset/bip_counter.wav')

        self.gameover_img = pygame.image.load('./asset/Game_over.png').convert_alpha()
        self.win_img = pygame.image.load('./asset/You_Win.png').convert_alpha()

        # controle do menu final
        self.end_menu_timer = None
        self.show_end_menu = False
        self.menu_option = 0

        # countdown inicial
        self.countdown_value = 3
        self.last_count_update = pygame.time.get_ticks()
        self.game_started = False


    def spawn_obstacle(self):

        if len(self.spikes) + len(self.barrels) >= self.max_obstacles:
            return

        lanes = [140, 240, 340, 440]
        spawn_x = WIN_WIDTH + 120

        y = random.choice(lanes)

        if self.last_obstacle == "spike":
            self.barrels.append(Radioactive((spawn_x, y)))
            self.last_obstacle = "barrel"
        else:
            self.spikes.append(Spike((spawn_x, y)))
            self.last_obstacle = "spike"


    def spawn_dumpster(self):

        dumpster_types = [
            '/dumpster1',
            '/dumpster2',
            '/dumpster3',
            '/dumpster4'
        ]

        name = random.choice(dumpster_types)

        lanes = [140, 240, 340, 440]
        y_position = random.choice(lanes)

        distance = random.randint(320, 480)

        last_x = self.dumpsters[-1].rect.x

        dumpster = Dumpster(name, (last_x + distance, y_position))

        self.dumpsters.append(dumpster)


    def run(self):

        clock = pygame.time.Clock()

        pygame.mixer.music.load('./asset/Intro.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.engine_sound.set_volume(0.6)


        font = pygame.font.SysFont("Arial", 28)

        while True:

            clock.tick(60)

            # CONTADOR INICIAL
            if not self.game_started:

                now = pygame.time.get_ticks()

                if now - self.last_count_update >= 1000:

                    if self.countdown_value > 0:
                        self.counter_sound.play()

                    self.countdown_value -= 1
                    self.last_count_update = now

                    if self.countdown_value < 0:
                        self.game_started = True
                        self.engine_sound.play(-1)


            if not self.game_over and not self.win and self.game_started:

                last_dumpster = self.dumpsters[-1]

                if last_dumpster.rect.x < WIN_WIDTH:
                    self.spawn_dumpster()

                if random.random() < 0.03:
                    self.spawn_obstacle()

                if not self.slowdown:
                    self.bg1.move()
                    self.bg2.move()
                else:
                    if self.bg1.speed > 0:
                        self.bg1.speed -= 0.04
                        self.bg2.speed -= 0.04
                    else:
                        self.game_over = True

                for dumpster in self.dumpsters:
                    dumpster.move()

                for dumpster in self.dumpsters[:]:

                    if dumpster.rect.right < 0:
                        self.dumpsters.remove(dumpster)
                        continue

                    if self.player.rect.colliderect(dumpster.rect):

                        self.collect_sound.play()
                        self.dumpsters.remove(dumpster)

                        self.dumpsters_collected += 1

                        if self.dumpsters_collected >= self.dumpsters_target:
                            self.win = True

                for spike in self.spikes[:]:
                    spike.move()

                    if spike.rect.right < 0:
                        self.spikes.remove(spike)

                    if self.player.rect.colliderect(spike.rect):
                        if not self.slowdown:
                            self.blowout_sound.play()
                            self.slowdown = True

                for barrel in self.barrels[:]:
                    barrel.move()

                    if barrel.rect.right < 0:
                        self.barrels.remove(barrel)

                    if self.player.rect.colliderect(barrel.rect):
                        if not self.game_over:
                            self.explosion_sound.play()
                            self.game_over = True

                self.player.move()

                if self.bg1.rect.right <= 0:
                    self.bg1.rect.left = self.bg2.rect.right

                if self.bg2.rect.right <= 0:
                    self.bg2.rect.left = self.bg1.rect.right


            if (self.game_over or self.win) and self.end_menu_timer is None:
                self.end_menu_timer = pygame.time.get_ticks()

            if self.end_menu_timer:
                if pygame.time.get_ticks() - self.end_menu_timer > 1000:
                    self.show_end_menu = True


            self.window.blit(self.bg1.surf, self.bg1.rect)
            self.window.blit(self.bg2.surf, self.bg2.rect)

            for dumpster in self.dumpsters:
                self.window.blit(dumpster.surf, dumpster.rect)

            for spike in self.spikes:
                self.window.blit(spike.surf, spike.rect)

            for barrel in self.barrels:
                self.window.blit(barrel.surf, barrel.rect)

            self.window.blit(self.player.surf, self.player.rect)

            counter_text = f"{self.dumpsters_collected} / {self.dumpsters_target}"
            text_surface = font.render(counter_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topright=(WIN_WIDTH - 20, 20))

            # fundo semi-transparente
            padding_x = 12
            padding_y = 8

            bg_rect = pygame.Rect(
                text_rect.left - padding_x,
                text_rect.top - padding_y,
                text_rect.width + padding_x * 2,
                text_rect.height + padding_y * 2
            )

            counter_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            counter_bg.fill((0, 0, 0, 130))  # preto com transparência

            self.window.blit(counter_bg, (bg_rect.x, bg_rect.y))

            # texto do contador
            self.window.blit(text_surface, text_rect)


            if not self.game_started:

                font_count = pygame.font.SysFont("Lucida Sans Typewriter", 150)

                text = str(self.countdown_value if self.countdown_value > 0 else "")

                text_surface = font_count.render(text, True, (255,255,255))
                rect = text_surface.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))

                self.window.blit(text_surface, rect)


            if self.game_over:

                self.engine_sound.stop()

                if self.gameover_alpha == 0:
                    self.gameover_sound.play()

                if self.gameover_alpha < 255:
                    self.gameover_alpha += 3

                self.gameover_img.set_alpha(self.gameover_alpha)

                rect = self.gameover_img.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))

                self.window.blit(self.gameover_img, rect)


            if self.win:

                self.engine_sound.stop()

                if self.win_alpha == 0:
                    self.win_sound.play()

                if self.win_alpha < 255:
                    self.win_alpha += 3

                self.win_img.set_alpha(self.win_alpha)

                rect = self.win_img.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))

                self.window.blit(self.win_img, rect)

            if self.show_end_menu:

                font_menu = pygame.font.SysFont("Lucida Sans Typewriter", 40)

                # cria retângulo com transparência
                menu_bg = pygame.Surface((420, 140))
                menu_bg.set_alpha(130)  # transparência (0-255)
                menu_bg.fill((0, 0, 0))

                bg_rect = menu_bg.get_rect(center=(WIN_WIDTH // 2, 380))
                self.window.blit(menu_bg, bg_rect)

                for i in range(len(MENU_OPTIONS)):
                    color = C_GREEN if i == self.menu_option else C_WHITE

                    text = font_menu.render(MENU_OPTIONS[i], True, color)

                    rect = text.get_rect(center=(WIN_WIDTH // 2, 350 + i * 60))

                    self.window.blit(text, rect)


            pygame.display.flip()


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if self.show_end_menu:

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_UP:
                            self.menu_option = (self.menu_option - 1) % len(MENU_OPTIONS)

                        if event.key == pygame.K_DOWN:
                            self.menu_option = (self.menu_option + 1) % len(MENU_OPTIONS)

                        if event.key == pygame.K_RETURN:

                            if MENU_OPTIONS[self.menu_option] == "INICIAR JOGO":
                                self.__init__(self.window, self.name)

                            if MENU_OPTIONS[self.menu_option] == "SAIR":
                                pygame.quit()
                                quit()