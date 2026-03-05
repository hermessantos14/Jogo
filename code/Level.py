import pygame
import random
from code.Background import Background
from code.Player import Player
from code.Dumpster import Dumpster
from code.Const import WIN_HEIGHT, WIN_WIDTH


class Level:

    def __init__(self, window, name):
        self.window = window
        self.name = name

        self.dumpsters = [
            Dumpster('/dumpster1', (950, 150)),
            Dumpster('/dumpster2', (1200, 350)),
            Dumpster('/dumpster3', (1500, 250)),
            Dumpster('/dumpster4', (1800, 450))
        ]

        # cria pistas do parallax
        self.bg1 = Background('/pista1', (0, 0), 5)
        self.bg2 = Background('/pista2', (WIN_WIDTH, 0), 5)

        self.player = Player((120, 300))

        # som do motor
        self.engine_sound = pygame.mixer.Sound('./asset/truck_engine.wav')

        # som coleta dumpster
        self.collect_sound = pygame.mixer.Sound('./asset/garbage_collection.wav')



    # função para criar caçambas
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
        distance = random.randint(250, 400)
        last_x = self.dumpsters[-1].rect.x
        dumpster = Dumpster(name, (last_x + distance, y_position))
        self.dumpsters.append(dumpster)

    def run(self):

        clock = pygame.time.Clock()

        # música de fundo
        pygame.mixer.music.load('./asset/Intro.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # som do motor
        self.engine_sound.set_volume(0.6)
        self.engine_sound.play(-1)

        while True:

            clock.tick(60)

            # controle de spawn
            last_dumpster = self.dumpsters[-1]

            if last_dumpster.rect.x < WIN_WIDTH:
                self.spawn_dumpster()


            # mover pista
            self.bg1.move()
            self.bg2.move()

            # mover dumpsters
            for dumpster in self.dumpsters[:]:
                dumpster.move()

                if dumpster.rect.right < 0:
                    self.dumpsters.remove(dumpster)

            # coleta
            for dumpster in self.dumpsters[:]:
                if self.player.rect.colliderect(dumpster.rect):
                    self.collect_sound.play()
                    self.dumpsters.remove(dumpster)

            # mover caminhão
            self.player.move()

            # reset infinito da pista
            if self.bg1.rect.right <= 0:
                self.bg1.rect.left = self.bg2.rect.right

            if self.bg2.rect.right <= 0:
                self.bg2.rect.left = self.bg1.rect.right

            # desenhar pista
            self.window.blit(self.bg1.surf, self.bg1.rect)
            self.window.blit(self.bg2.surf, self.bg2.rect)

            # desenhar dumpsters
            for dumpster in self.dumpsters:
                self.window.blit(dumpster.surf, dumpster.rect)

            # desenhar caminhão
            self.window.blit(self.player.surf, self.player.rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
