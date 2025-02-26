import pygame
import random
import math
import pygame
from boid import Boid
from predator import Predator

class Prey(Boid):
    MAX_SPEED = .5
    PERCEPTION_RADIUS = 50
    SEPARATION_DISTANCE = 30

    SEPERATION_COEFFICIENT = 0.6
    ESCAPE_COEFFICIENT = 0.8
    ALIGNMENT_COEFFICIENT = 0.01
    COHESION_COEFFICIENT = 0.0005

    def __init__(self, x, y):
        self.flag = random.uniform(0, 10) < .5
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(self.MAX_SPEED)
    
    def escapePredators(self, flock):
        average_separation = pygame.Vector2(0, 0)
        for other in flock:
            if other == self:
                continue

            if not self.isSafe(other):
                distance = super().distance_to(other)
                if distance < self.PERCEPTION_RADIUS:
                    average_separation += other.velocity
        return - average_separation * self.ESCAPE_COEFFICIENT


    def separation(self, flock):
        average_separation = pygame.Vector2(0, 0)
        for other in flock:
            if other == self or not self.isSafe(other):
                continue

            distance = super().distance_to(other)
            if distance < self.SEPARATION_DISTANCE and distance > 0:
                diff = self.position - other.position
                diff.scale_to_length(1 / distance)
                average_separation += diff
        return average_separation * self.SEPERATION_COEFFICIENT
    
    def alignment(self, flock):
        average_velocity = pygame.Vector2(0, 0)
        num_neighbors = 0
        for other in flock:
            if other == self or not self.isSafe(other):
                continue

            if super().distance_to(other) < self.PERCEPTION_RADIUS:
                average_velocity += other.velocity
                num_neighbors += 1
        if num_neighbors > 0:
            average_velocity /= num_neighbors
        return (average_velocity - self.velocity) * self.ALIGNMENT_COEFFICIENT
    
    def cohesion(self, flock):
        average_position = pygame.Vector2(0, 0)
        num_neighbors = 0
        for other in flock:
            if other == self or not self.isSafe(other):
                continue

            if super().distance_to(other) < self.PERCEPTION_RADIUS:
                average_position += other.position
                num_neighbors += 1
        if num_neighbors > 0:
            average_position /= num_neighbors
        return (average_position - self.position) * self.COHESION_COEFFICIENT

    def draw(self, screen):
        if self.flag:
            pygame.draw.circle(screen, (68, 68, 68), (int(self.position.x), int(self.position.y)), self.PERCEPTION_RADIUS, width=1)
            pygame.draw.circle(screen, 'red', (int(self.position.x), int(self.position.y)), self.SEPARATION_DISTANCE, width=1)

        angle = math.atan2(self.velocity.y, self.velocity.x)
        length = 10
        end_x = self.position.x - length * math.cos(angle)
        end_y = self.position.y - length * math.sin(angle)
        pygame.draw.line(screen, (255, 255, 255), (self.position.x, self.position.y), (end_x, end_y), 2)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 3)

    def isSafe(self, boid):
        return type(boid) == self.__class__
    
    def update(self, flock, WIDTH, HEIGHT):
        separation = self.separation(flock)
        alignment = self.alignment(flock)
        cohesion = self.cohesion(flock)
        escape = self.escapePredators(flock)

        self.velocity += alignment + cohesion + separation + escape
        self.velocity.scale_to_length(self.MAX_SPEED)

        self.position += self.velocity
        super().wrap_edges(WIDTH, HEIGHT)

    