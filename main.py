
# import stuff
import pygame
from dot_obj import Dot, goal
import numpy as np
import random

# initialization stuff
pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 24)
pygame.display.set_caption("Learnin Dots")

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

# Function to render text
def render_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# function to generate multiple dots
def create_generation_1(num_dots):
    dots = []
    for _ in range(num_dots):
        new_dot = None
        pos = np.array([25, 400])
        vel = np.array([0, 0])
        acc = np.array([0, 0])
        new_dot = Dot(pos, vel, acc)
        dots.append(new_dot)
    return dots

# create the next generation
def next_gen(num_dots, prev_gen):
    # bad globals
    global avg_fit, reachedgoaltotal, global_reachedgoaltotal
    reachedgoaltotal = 0
    
    # this is probably terrible implementation, but it turns fitness into a probablility and chooses the parents based on that
    for dot in prev_gen:
        dot.fitnesscalc(goal)
    
    fitnesses = np.array([dot.fitness for dot in prev_gen])
    total_fitness = np.sum(fitnesses)
    avg_fit = total_fitness / len(prev_gen)

    top_scorer_index = np.argmax(fitnesses)
    top_scorer = prev_gen[top_scorer_index].clone()
    gen = [top_scorer]

    probabilities = fitnesses / total_fitness
    
    parent_indices = np.random.choice(len(prev_gen), size=num_dots - 1, p=probabilities)
    parents = [prev_gen[index] for index in parent_indices]

    # now breed the parents
    new_dots = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[(i+1) % len(parents)]
        child = parent1.crossover(parent2)
        new_dots.append(child)

    while len(new_dots) < num_dots - 1:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = parent1.crossover(parent2)
        new_dots.append(child)
    
    # stuff for the upper left display
    for dot in prev_gen:
        if dot.reachedgoal:
            reachedgoaltotal += 1
            global_reachedgoaltotal += 1

    # mutate those fuckers
    for new_dot in new_dots:
        new_dot.mutate()

    gen.extend(new_dots[:num_dots - 1])

    return gen



# more initializations
dots = create_generation_1(1000)
generation = 1
goal = goal()
global avg_fit, reachedgoaltotal, global_reachedgoaltotal
avg_fit = 0
reachedgoaltotal = 0
global_reachedgoaltotal = 0

# main loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render the goals and the upper left hand display
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, goal.pos, 17)
    render_text(f"Generation: {generation}", 1000, 50)
    render_text(f"avg fitness: {avg_fit}", 1000, 75)
    render_text(f"reached goal: {reachedgoaltotal}", 1000, 100)
    if generation > 1:
        render_text(f"avg reached goal: {(global_reachedgoaltotal/(generation-1)):.2f}", 1000, 125)

    # render the boys
    for dot in dots:
        pygame.draw.circle(screen, WHITE, dot.pos, 5)
        if dot.dead == False and dot.reachedgoal == False:
            dot.update()
        if goal.pos[0]-17 < dot.pos[0] < goal.pos[0]+17 and goal.pos[1]-17 < dot.pos[1] < goal.pos[1]+17:
            dot.reachedgoal = True
            dot.dead = True

    # check if the boys are dead 
    if all(dot.dead == True for dot in dots):
        old_dots = dots
        for guy in dots:
            guy.fitnesscalc(goal)
        dots = next_gen(1000, old_dots)
        generation += 1


    pygame.display.flip()