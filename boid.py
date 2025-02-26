from abc import ABC, abstractmethod
import math
import uuid

class Boid(ABC):

    def __init__(self):
        self.id = uuid.uuid4()
        self.alive = True

    def isAlive(self):
        return self.alive
    
    def setToDeath(self):
        self.alive = False

    def isSame(self, other):
        return self.id == other.id
    
    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def update(self, flock, WIDTH, HEIGHT):
        pass

    def wrap_edges(self, WIDTH, HEIGHT):
    # Check and update the entity's position to wrap around the screen edges
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y < 0:
            self.position.y = HEIGHT
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y > HEIGHT:
            self.position.y = 0

    def distance_to(self, other): # vector 2 dimensions
        return math.sqrt((self.position.x - other.position.x)**2 + (self.position.y - other.position.y)**2)

    

    