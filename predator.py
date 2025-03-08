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

    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.flag = random.uniform(0, 10) < 5
        self.position = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(self.MAX_SPEED)
    
    def checkForPrey(self, flock):
        for other in flock:
            if super().isSame(other) or type(other) != Prey:
                continue

            if other.isAlive() and self.distance_to(other) < self.SEPARATION_DISTANCE:
                self.killedPreyCount += 1

    def update(self, flock, WIDTH, HEIGHT):
        self.checkForPrey(flock)
        
        newVelocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        self.velocity += newVelocity * 0.01

        self.velocity.scale_to_length(self.MAX_SPEED)
        self.position += self.velocity
        self.wrap_edges(WIDTH, HEIGHT)

    def turn(self, level): # for the RL
        if level not in [-2, -1, 0, 1, 2]:
            print("Invalid action: {}".format(level))
            return
        
        if level == 0:
            return
        
        angle_degrees = level * 30
        angle_rad = math.radians(angle_degrees)
        new_vx = self.velocity.x * math.cos(angle_rad) - self.velocity.y * math.sin(angle_rad)
        new_vy = self.velocity.x * math.sin(angle_rad) + self.velocity.y * math.cos(angle_rad)
        self.velocity = pygame.Vector2(new_vx, new_vy)
    
    def getPreyInVision(self, flock):
        closePreys = []
        for prey in flock:
            if prey.isAlive() and super().distance_to(prey) < self.PERCEPTION_RADIUS:
                closePreys.append(prey)
        return closePreys
    
    def getObservation(self, flock):
        preys = self.getPreyInVision(flock)
        observation = {}
        for prey in preys:
            rel_velocity = prey.velocity - self.velocity
            relativePostion = super().distance_to(prey)
            observation[prey.id] = rel_velocity.x, rel_velocity.y, relativePostion, 1
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

    def fitness(self):
        return self.killedPreyCount * 10