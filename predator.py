from boid import Boid
import random
import pygame
import math
from prey import Prey

class Predator(Boid):
    MAX_SPEED = .5
    PERCEPTION_RADIUS = 85
    SEPARATION_DISTANCE = 30
    killedPreyCount = 0
    prey_indicator = 0
    predator_indicator = 1

    def __init__(self, x, y):
        super().__init__()
        self.flag = random.uniform(0, 10) < 5
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(self.MAX_SPEED)

    def colision(self, flock):
        for other in flock:
            if super().isSame(other) or type(other) != Predator:
                continue

            if self.distance_to(other) < self.SEPARATION_DISTANCE:
                return True
        return False
    
    def checkForPrey(self, flock):
        for other in flock:
            if super().isSame(other) or type(other) != Prey:
                continue

            if self.distance_to(other) < self.SEPARATION_DISTANCE:
                self.killedPreyCount += 1

    def update(self, flock, WIDTH, HEIGHT):
        if self.colision(flock):
            return super().setToDeath()
        
        self.checkForPrey(flock)
        
        newVelocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        self.velocity += newVelocity * 0.01

        self.velocity.scale_to_length(self.MAX_SPEED)
        self.position += self.velocity
        self.wrap_edges(WIDTH, HEIGHT)

    def turn(self, level): # for the RL
        if level == 0:
            return
        
        angle_degrees = level * 30
        angle_rad = math.radians(angle_degrees)
        new_vx = self.velocity.x * math.cos(angle_rad) - self.velocity.y * math.sin(angle_rad)
        new_vy = self.velocity.x * math.sin(angle_rad) + self.velocity.y * math.cos(angle_rad)
        self.velocity = pygame.Vector2(new_vx, new_vy)

    def getPredatorsInVision(self, flock):
        observation = []
        for predator in flock:
            if self != predator:
                continue
            if super().distance_to(predator) < self.PERCEPTION_RADIUS and type(predator) != Predator:
                rel_velocity = predator.velocity - self.velocity
                observation += rel_velocity.x, rel_velocity.y, self.prey_indicator
        return observation
    
    def getPreyInVision(self, flock):
        observation = []
        for prey in flock:
            if super().distance_to(prey) < self.PERCEPTION_RADIUS and type(prey) != Prey:
                rel_velocity = prey.velocity - self.velocity
                observation += rel_velocity.x, rel_velocity.y, self.prey_indicator
        return observation
    
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