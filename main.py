import pygame
import random
import math
import copy
from prey import Prey
from predator import Predator

PREY_NUM = 10
PREDATOR_NUM = 1
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1500, 1100

def main(iterationNumber):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking Simulation")
    
    noMorePredators = False
    flock = init_population()

    iteration = 0
    intercepted = False
    clock = pygame.time.Clock()

    while iteration < iterationNumber and not intercepted and not noMorePredators:
        iteration+=1

        if iteration%1_000 == 0:
            log(iteration, flock)

        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intercepted = True

        # reset the screen
        screen.fill(BLACK)
        
        # Update entities and draw them on the screen
        
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

def init_population():
    preys = [Prey(WIDTH, HEIGHT) for _ in range(PREY_NUM)]
    predators = [Predator(WIDTH,HEIGHT) for _ in range(PREDATOR_NUM)]
    return predators + preys


def fitness(flock):
    huntedPreyValue = 10
    deadPredatorValue = -30
    predators = [x for x in flock if type(x) == Predator]
    deadPredator = len([1 for predator in predators if not predator.isAlive()])
    huntedPrey = len([predator.killedPreyCount for predator in predators])
    return huntedPreyValue * huntedPrey + deadPredatorValue * deadPredator


def log(iteration, flock):
    print("___________________________________________________________")
    print("Iteration : {}".format(iteration))
    predators = [x for x in flock if type(x) == Predator]
    killedPrey = [predator.killedPreyCount for predator in predators]
    value = fitness(flock)
    print("### PREDATOR ###")
    print("Alive : ", len(predators))
    print("Dead : ", PREDATOR_NUM - len(killedPrey))
    print("### PREY ###")
    print("hunted : {}".format(sum(killedPrey)))
    print("### FITNESS ###")
    print("fitness : {}".format(value))

if __name__ == "__main__":
    iterationNumber = 10_000
    main(iterationNumber)