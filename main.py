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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking Simulation")
    preys = [Prey(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(PREY_NUM)]
    predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(PREDATOR_NUM)]

    flock = preys + predators

    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update entities and draw them on the screen
        screen.fill(BLACK)
        copied_flock = list(map(lambda x: copy.deepcopy(x), flock))
        for entity in copied_flock:
            entity.update(preys, WIDTH, HEIGHT)
            entity.draw(screen)

        flock = copied_flock
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()