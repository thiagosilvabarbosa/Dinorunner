import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.number = 1

    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]
        
        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0, 1)])

        self.number = random.randint(0, 1)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacle.rect):

                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    
                    game.playing = False
                    game.death_count += 1
                    break                
                elif game.player.type == "hammer":
                    self.obstacles.remove(obstacle)  
                elif game.player.type == "shield":
                    pass
                elif game.player.type == "star":
                    game.score += 150

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
