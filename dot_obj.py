
# import stuff
import random
import numpy as np
import math
import copy

# the BRAIN OF THE MACHINE
class Brain:
    def __init__(self):
        self.gen = 0
        self.directions = self.random_brain()

    def random_brain(self):
        directions = np.random.randint(low=[0, -9], high=[5, 10], size=(700, 2))
        return directions.tolist()

# what these guys strive for in life
class goal:
    def __init__(self):
        self.pos = [1100,400]
        
    def dist(self, dotx, doty):
        dist = math.sqrt((self.pos[0]-dotx)**2+(self.pos[1]-doty)**2)
        return dist

# the guys
class Dot:
    def __init__(self, pos, vel, acc):
        self.brain = Brain()
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.fitness = 0
        self.dead = False
        self.step = 0
        self.reachedgoal = False

    # how they know where to go
    def update(self):
        new_pos = self.pos
        new_pos += self.vel
        if 0 <= new_pos[0] < 1200 and 0 <= new_pos[1] < 800:
            self.pos = new_pos
        else:
            self.dead = True
        self.vel = self.acc
        if self.vel[0] > 5:
            self.vel[0] = 5
        if self.vel[1] > 5:
            self.vel[1] = 5
        if self.vel[0] > -5:
            self.vel[0] = -5
        if self.vel[1] > -5:
            self.vel[1] = -5
        if self.step < len(self.brain.directions):
            self.acc[0] = self.brain.directions[self.step][0]
            self.acc[1] = self.brain.directions[self.step][1]
            self.step += 1
        else:
            self.dead = True

    # whos the best
    def fitnesscalc(self, goal):
        if self.reachedgoal == False:
            self.fitness = 1/(goal.dist(self.pos[0],self.pos[1])**2)
        else:
            self.fitness = 1/64 + (self.step)/75000
    
    # copy a guy
    def clone(self):
        pos = np.array([25, 400])
        vel = np.array([0, 0])
        acc = np.array([0, 0])
        clone = Dot(pos,vel,acc)
        clone.brain = copy.deepcopy(self.brain)
        return clone
    
    # makin babies
    def crossover(self, parent2): 
        pos = np.array([25, 400]) 
        vel = np.array([0, 0]) 
        acc = np.array([0, 0]) 
        child_brain = Brain()
        
        crossover_point = random.randint(0, len(self.brain.directions))
        child_brain.directions = copy.deepcopy(self.brain.directions[:crossover_point]) + copy.deepcopy(parent2.brain.directions[crossover_point:])
        
        if len(child_brain.directions) != len(self.brain.directions):
            raise ValueError("Error in crossover: child brain directions length mismatch.")
        
        child_dot = Dot(pos, vel, acc) 
        child_dot.brain = child_brain 
        return child_dot


    # random mutations
    def mutate(self):
        mutation_rate = .005
        for instruction in self.brain.directions:
            rand = random.random()
            if rand <= mutation_rate:
                instruction[0] = random.randint(0,5)
                instruction[1] = random.randint(-9,10)


    