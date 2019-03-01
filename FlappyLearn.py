from enum import Enum
import random
import NeuralNetwork
import numpy as np
import time
from math import ceil
from Base import *
from copy import deepcopy


SPRITE_SCALING_PIPE = PIPE_WIDTH/26
SPRITE_SCALING_BIRD = (2*R_BIRD)/1024

N_BIRD = 50
MUTATION_RATE = 1
BEST1_PROP = 0.3
BEST2_PROP = 0.1
BREED1_RATE = 0.3
BREED2_RATE = 0.4/2
KEEP_RATE = 0.3




        

class Learn(Base):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, N_BIRD)
        # Set constant for bird
        self.current_pipe = None
        # score
        self.gen = 0
        self.liveBirds = N_BIRD


    def setup(self):
        # Set up your game here
        


        # Set constant for bird
        self.fitness = 0
        self.current_pipe = self.list_pipes[0]
        for bird in self.list_birds:  
            input = np.matrix([1, bird.y, self.current_pipe.x, self.current_pipe.h])
            bird.nnet = NeuralNetwork.NeuralNetwork(input)
        # score
        self.score = 0
        self.liveBirds = N_BIRD
        pass

    
    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.levelScreen()
        arcade.draw_text('gen : ' + str(self.gen), 10, SCREEN_HEIGHT - 25, arcade.color.BLACK, 11, width=1000, align="left")
        arcade.draw_text('Left alive : ' + str(self.liveBirds), 10, SCREEN_HEIGHT - 50, arcade.color.BLACK, 11, width=100, align="left")
    

                

    def updateBirds(self):
        if(self.liveBirds == 0):
            self.new_generation()
        else:
            for bird in self.list_birds:
                if(not bird.dead):
                    bird.fitness += 1
                    bird.nnet.input = np.matrix([1, bird.y, self.current_pipe.x, self.current_pipe.h])#np.matrix([bird.xdist, bird.yddist, bird.yudist, bird.v])
                    bird.nnet.feedforward()
                    key = bird.nnet.output

                    bird.move(self.list_pipes, key)
                    if(bird.dead):
                        self.liveBirds-=1
        
        
    def restart(self):
        super().restart(N_BIRD)
        for bird in self.list_birds:
            input = np.matrix([0, 0, 0, 0])
            bird.nnet = NeuralNetwork.NeuralNetwork(input)
        self.liveBirds = N_BIRD
        self.current_pipe = self.list_pipes[0]

    def crossover(self, bird1, bird2):
                mat1 = np.random.randint(2, size = bird1.nnet.weights1.shape)
                mat2 = np.random.randint(2, size = bird1.nnet.weights2.shape)
                weights1 = np.multiply(bird1.nnet.weights1, mat1) + np.multiply(bird2.nnet.weights1, 1 - mat1)
                weights2 = np.multiply(bird1.nnet.weights2, mat2) + np.multiply(bird2.nnet.weights2, 1 - mat2)
                mutation = np.random.random()<MUTATION_RATE
                if(mutation):
                    weights1 += np.random.normal(0, np.std(weights1)/10, weights1.shape)
                    weights2 += np.random.normal(0, np.std(weights2)/10, weights2.shape)
                return weights1, weights2
    
    def clone (self, bird):
        mutation = np.random.random()<MUTATION_RATE
        weights1 = bird.nnet.weights1
        weights2 = bird.nnet.weights2
        if(mutation):
            weights1 += np.random.normal(0, np.std(weights1)/10, weights1.shape)
            weights2 += np.random.normal(0, np.std(weights2)/10, weights2.shape)
        return weights1, weights2

    def draw_new_generation(self):
        list_birds = deepcopy(self.list_birds)
        sortedBirds = sorted(list_birds, key=lambda x: x.fitness, reverse=True)
        best1Birds = sortedBirds[:int(BEST1_PROP*N_BIRD)]
        best2Birds = sortedBirds[:int(BEST2_PROP*N_BIRD)]
        i=0
        self.restart()
        for k in range(N_BIRD):
            if(k<N_BIRD*BREED1_RATE):
                birds = np.random.choice(best1Birds, 2, replace = True)
                #weights1 = (birds[0].nnet.weights1 + birds[1].nnet.weights1)/2
                #weights2 = (birds[0].nnet.weights2 + birds[1].nnet.weights2)/2
                weights1, weights2 = self.crossover(birds[0], birds[1])
                self.list_birds[k].nnet.weights1 = weights1
                self.list_birds[k].nnet.weights2 = weights2
            elif(k<N_BIRD*(BREED1_RATE+2*BREED2_RATE)):
                birds = np.random.choice(best2Birds, 2, replace = True)
                #weights1 = (birds[0].nnet.weights1 + birds[1].nnet.weights1)/2
                #weights2 = (birds[0].nnet.weights2 + birds[1].nnet.weights2)/2
                for child in range(2):
                    weights1, weights2 = self.crossover(birds[0], birds[1])
                    self.list_birds[k].nnet.weights1 = weights1
                    self.list_birds[k].nnet.weights2 = weights2
                    k+=1
            else:
                bird = sortedBirds[0]#np.random.choice(best2Birds, 1, replace = True)[0]
                weights1, weights2 = self.clone(bird)
                self.list_birds[k].nnet.weights1 = weights1
                self.list_birds[k].nnet.weights2 = weights2


    def new_generation(self):
        self.gen += 1
        self.draw_new_generation()
        
    def updateScore(self):
        if(abs(X_BIRD - self.list_pipes[0].x - PIPE_WIDTH//2)<PIPE_SPEED):
            self.current_pipe = self.list_pipes[1]
            self.score+=1

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.updateScore()   
        self.updateBirds()
        self.updatePipes()
        self.moveGround()         
        pass

def main():
    
    game = Learn(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

