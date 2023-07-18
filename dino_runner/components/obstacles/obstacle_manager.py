from typing import Self
import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.number = 1

    def update(self, game):
        cactus_choice = random.choice([SMALL_CACTUS, LARGE_CACTUS])

        if len(self.obstacles) == 0:
            if self.number:
                self.obstacles.append(Cactus(cactus_choice))
            else:
                self.obstacles.append(Bird(BIRD))

        self.number = random.randint(0, 1)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
