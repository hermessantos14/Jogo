import pygame
import random
from code.Background import Background
from code.Player import Player
from code.Dumpster import Dumpster
from code.Spike import Spike
from code.Radioactive import Radioactive
from code.Const import WIN_HEIGHT, WIN_WIDTH


class Level:

    def __init__(self, window, name):

        self.window = window
        self.name = name

        self.game_over = False
        self.slowdown = False
        self.gameover_alpha = 0

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

        self.gameover_img = pygame.image.load('./asset/Game_over.png').convert_alpha()

    def spawn_obstacle(self):

        if len(self.spikes) + len(self.barrels) >= self.max_obstacles:
            return

        lanes = [140, 240, 340, 440]

        spawn_x = WIN_WIDTH + 120

        # evitar spawn perto de dumpsters que estão entrando na tela
        for dumpster in self.dumpsters:
            if WIN_WIDTH - 150 < dumpster.rect.x < WIN_WIDTH + 150:
                return

        occupied_lanes = []

        for spike in self.spikes:
            occupied_lanes.append(spike.rect.y)

        for barrel in self.barrels:
            occupied_lanes.append(barrel.rect.y)

        free_lanes = [lane for lane in lanes if lane not in occupied_lanes]

        if not free_lanes:
            return

        y = random.choice(free_lanes)

        if self.last_obstacle == "spike":

            self.barrels.append(Radioactive((spawn_x, y)))
            self.last_obstacle = "barrel"

        else:

            self.spikes.append(Spike((spawn_x, y)))
            self.last_obstacle = "spike"

        # evitar obstáculo perto de caçamba
        for dumpster in self.dumpsters:
            if abs(dumpster.rect.x - spawn_x) < 250:
                return

        occupied_lanes = []

        for spike in self.spikes:
            occupied_lanes.append(spike.rect.y)

        for barrel in self.barrels:
            occupied_lanes.append(barrel.rect.y)

        free_lanes = [lane for lane in lanes if lane not in occupied_lanes]

        if not free_lanes:
            return

        y = random.choice(free_lanes)

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
        self.engine_sound.play(-1)

        while True:

            clock.tick(60)

            if not self.game_over:

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

                for dumpster in self.dumpsters[:]:
                    dumpster.move()

                    if dumpster.rect.right < 0:
                        self.dumpsters.remove(dumpster)

                for spike in self.spikes[:]:
                    spike.move()

                    if spike.rect.right < 0:
                        self.spikes.remove(spike)

                for barrel in self.barrels[:]:
                    barrel.move()

                    if barrel.rect.right < 0:
                        self.barrels.remove(barrel)

                for dumpster in self.dumpsters[:]:
                    if self.player.rect.colliderect(dumpster.rect):
                        self.collect_sound.play()
                        self.dumpsters.remove(dumpster)

                for spike in self.spikes:
                    if self.player.rect.colliderect(spike.rect):
                        if not self.slowdown:
                            self.blowout_sound.play()
                            self.slowdown = True

                for barrel in self.barrels:
                    if self.player.rect.colliderect(barrel.rect):
                        if not self.game_over:
                            self.explosion_sound.play()
                            self.game_over = True

                self.player.move()

                if self.bg1.rect.right <= 0:
                    self.bg1.rect.left = self.bg2.rect.right

                if self.bg2.rect.right <= 0:
                    self.bg2.rect.left = self.bg1.rect.right

            self.window.blit(self.bg1.surf, self.bg1.rect)
            self.window.blit(self.bg2.surf, self.bg2.rect)

            for dumpster in self.dumpsters:
                self.window.blit(dumpster.surf, dumpster.rect)

            for spike in self.spikes:
                self.window.blit(spike.surf, spike.rect)

            for barrel in self.barrels:
                self.window.blit(barrel.surf, barrel.rect)

            self.window.blit(self.player.surf, self.player.rect)

            if self.game_over:

                self.engine_sound.stop()

                if self.gameover_alpha == 0:
                    self.gameover_sound.play()

                if self.gameover_alpha < 255:
                    self.gameover_alpha += 3

                self.gameover_img.set_alpha(self.gameover_alpha)

                rect = self.gameover_img.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))

                self.window.blit(self.gameover_img, rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()