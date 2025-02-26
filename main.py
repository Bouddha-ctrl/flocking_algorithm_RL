import pygame
import random
import math
import copy
from prey import Prey
from predator import Predator

PREY_NUM = 100
PREDATOR_NUM = 10
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1500, 1100

def main(iterationNumber):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking Simulation")
    preys = [Prey(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(PREY_NUM)]
    predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(PREDATOR_NUM)]
    noMorePredators = False
    flock = predators + preys

    iteration = 0
    intercepted = False
    clock = pygame.time.Clock()

    while iteration < iterationNumber and not intercepted and not noMorePredators:
        if iteration%100 == 0:
            log(iteration, flock)
        iteration+=1
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intercepted = True

        # Update entities and draw them on the screen
        screen.fill(BLACK)
        copied_flock = list(map(lambda x: copy.deepcopy(x), flock))
        for entity in copied_flock:
            entity.update(flock, WIDTH, HEIGHT)
            if entity.isAlive():
                entity.draw(screen)
            
        flock = [x for x in copied_flock if x.isAlive()]
        noMorePredators = len([x for x in flock if type(x) == Predator]) == 0
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def fitness(flock):
    predators = [x for x in flock if type(x) == Predator]
    killedPrey = [predator.killedPreyCount for predator in predators]
    print("### PREDATOR ###")
    print("Alive : ", len(predators))
    print("Dead : ", PREDATOR_NUM - len(killedPrey))
    print("### PREY ###")
    print("hunted : {}".format(sum(killedPrey)))

def log(iteration, flock):
    print("___________________________________________________________")
    print("Iteration : {}".format(iteration))
    fitness(flock)

if __name__ == "__main__":
    iterationNumber = 10_000
    main(iterationNumber)