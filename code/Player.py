from code.Const import ROAD_TOP, ROAD_BOTTOM
from code.Entity import Entity

import pygame


class Player(Entity):

    def __init__(self, position):
        super().__init__('/truck', position)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # limitar truck na tela
        if self.rect.top < ROAD_TOP:
            self.rect.top = ROAD_TOP

        if self.rect.bottom > ROAD_BOTTOM:
            self.rect.bottom = ROAD_BOTTOM