from boid import Boid
import random
import pygame
import math

class Predator(Boid):
    MAX_SPEED = .5
    PERCEPTION_RADIUS = 70
    SEPARATION_DISTANCE = 25

    def __init__(self, x, y):
        self.flag = random.uniform(0, 10) < 3
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(self.MAX_SPEED)

    def update(self, flock, WIDTH, HEIGHT):
        newVelocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        self.velocity += newVelocity * 0.01
        self.velocity.scale_to_length(self.MAX_SPEED)

        self.position += self.velocity
        self.wrap_edges(WIDTH, HEIGHT)

    def draw(self, screen):
        if self.flag:
            pygame.draw.circle(screen, 'blue', (int(self.position.x), int(self.position.y)), self.PERCEPTION_RADIUS, width=1)
            pygame.draw.circle(screen, 'red', (int(self.position.x), int(self.position.y)), self.SEPARATION_DISTANCE, width=1)

        angle = math.atan2(self.velocity.y, self.velocity.x)
        length = 10
        end_x = self.position.x - length * math.cos(angle)
        end_y = self.position.y - length * math.sin(angle)
        pygame.draw.line(screen, (255, 255, 255), (self.position.x, self.position.y), (end_x, end_y), 2)
        pygame.draw.circle(screen, "red", (int(self.position.x), int(self.position.y)), 3)