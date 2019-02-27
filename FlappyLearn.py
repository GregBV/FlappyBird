import arcade
from enum import Enum
import random
import NeuralNetwork
import Bird
import Pipe
import numpy as np
import time
from math import ceil

'''SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRAVITY = 0.7
PIPE_SPEED = 3
PIPE_WIDTH = 50
GAP_HEIGHT = 165
JUMP_SPEED = 10
X_BIRD = 100
R_BIRD = 20
SPRITE_SCALING_PIPE = PIPE_WIDTH/26
SPRITE_SCALING_BIRD = (2*R_BIRD)/1024
'''
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
GRAVITY = 0.7
PIPE_SPEED = 3
PIPE_WIDTH = 70
GAP_HEIGHT = 200
JUMP_SPEED = 8
X_BIRD = 100
R_BIRD = 30

SPRITE_SCALING_PIPE = PIPE_WIDTH/26
SPRITE_SCALING_BIRD = (2*R_BIRD)/1024

N_BIRD = 50
MUTATION_RATE = 1
BEST1_PROP = 0.3
BEST2_PROP = 0.1
BREED1_RATE = 0.3
BREED2_RATE = 0.4/2
KEEP_RATE = 0.3



class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1
    END = 2
        

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.state = None
        # Set constant for bird
        
        self.list_pipes = None
        self.current_pipe = None
        # score
        self.score = int()
        self.gen = 0
        self.liveBirds = int()
        self.list_birds = None

        self.background = arcade.load_texture("sprites/minecraft.jpg")
        self.sprite_list_ground = arcade.SpriteList()
        for k in range(ceil(SCREEN_WIDTH/64)+1):
            self.sprite_list_ground.append(arcade.Sprite("sprites/ground.jpg", 0.25))
            self.sprite_list_ground[-1].center_x = (k+1//2)*64
            self.sprite_list_ground[-1].center_y = 64//2

    def setup(self):
        # Set up your game here
        

        # Set constant for pipe
        self.list_pipes = [Pipe.Pipe(SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, PIPE_SPEED, GAP_HEIGHT, SPRITE_SCALING_PIPE)]

        # Set constant for bird
        self.lastBirds = None
        self.fitness = 0
        self.list_birds = [Bird.Bird(X_BIRD, SCREEN_HEIGHT/2, R_BIRD, SPRITE_SCALING_BIRD) for k in range(N_BIRD)]
        self.current_pipe = self.list_pipes[0]
        for bird in self.list_birds:  
            input = np.matrix([1, bird.y, self.current_pipe.x, self.current_pipe.h])
            bird.nnet = NeuralNetwork.NeuralNetwork(input)
        # score
        self.score = 0
        self.liveBirds = N_BIRD
        self.state = GameStates.RUNNING
        self.sprite_list_birds = arcade.SpriteList()
        for b in self.list_birds:
            self.sprite_list_birds.append(b.sprite)
        self.sprite_list_pipes = arcade.SpriteList()
        for p in self.list_pipes:
            self.sprite_list_pipes.append(p.sprite_up)
            self.sprite_list_pipes.append(p.sprite_down)

        pass

    


    def levelScreen(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 1192*SCREEN_HEIGHT//670, SCREEN_HEIGHT, self.background)
        self.sprite_list_pipes.draw()
        self.sprite_list_ground.draw()
        self.sprite_list_birds.draw()

        # Draw score
        arcade.draw_text('score\n' + str(self.score), SCREEN_WIDTH//2, SCREEN_HEIGHT - 25, arcade.color.BLACK, 11, width=50, align="center",
                        anchor_x="center", anchor_y="center")
        arcade.draw_text('gen : ' + str(self.gen), 10, SCREEN_HEIGHT - 25, arcade.color.BLACK, 11, width=1000, align="left")
        arcade.draw_text('Left alive : ' + str(self.liveBirds), 10, SCREEN_HEIGHT - 50, arcade.color.BLACK, 11, width=100, align="left")



    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        if(self.state == GameStates.RUNNING):
            self.levelScreen()
    
    def updateScore(self):
        if(abs(X_BIRD - self.list_pipes[0].x - PIPE_WIDTH//2)<PIPE_SPEED):
            self.current_pipe = self.list_pipes[1]
            self.score+=1
            
    def updatePipes(self):
        if(abs(self.list_pipes[-1].x -PIPE_WIDTH//2 - SCREEN_WIDTH//2)<PIPE_SPEED):#abs(self.list_pipes[-1].x - 2*SCREEN_WIDTH//3)<PIPE_SPEED):
                self.list_pipes.append(Pipe.Pipe(SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, PIPE_SPEED, GAP_HEIGHT, SPRITE_SCALING_PIPE))
                self.sprite_list_pipes.append(self.list_pipes[-1].sprite_up)
                self.sprite_list_pipes.append(self.list_pipes[-1].sprite_down)
        
        if(self.list_pipes[0].x <= -PIPE_WIDTH//2):
            #self.sprite_list_pipes[0].kill()
            self.list_pipes.pop(0)

    def updateGround(self):
        
        if(self.sprite_list_ground[0].center_x<=-64//2):
            for s in self.sprite_list_ground:
                s.center_x += 64//2

    def moveGround(self):
        for s in self.sprite_list_ground:
            s.center_x -= PIPE_SPEED
        self.updateGround()
                

    def updateBirds(self):
        for bird in self.list_birds:
            if(not bird.dead):
                bird.fitness += 1
                bird.nnet.input = np.matrix([1, bird.y, self.current_pipe.x, self.current_pipe.h])#np.matrix([bird.xdist, bird.yddist, bird.yudist, bird.v])
                bird.nnet.feedforward()
                key = bird.nnet.output
                bird.move(self.list_pipes, key, JUMP_SPEED, GRAVITY, GAP_HEIGHT, SCREEN_HEIGHT)
                if(bird.dead):
                    self.liveBirds-=1
        
        if(self.liveBirds == 0):
           
            self.new_generation()
            

    def draw_new_generation(self):
        sortedBirds = sorted(self.list_birds, key=lambda x: x.fitness, reverse=True)
        best1Birds = sortedBirds[:int(BEST1_PROP*N_BIRD)]
        best2Birds = sortedBirds[:int(BEST2_PROP*N_BIRD)]
        self.setup()
        i=0
        for k in range(N_BIRD):
            if(k<N_BIRD*BREED1_RATE):
                birds = np.random.choice(best1Birds, 2, replace = True)
                #weights1 = (birds[0].nnet.weights1 + birds[1].nnet.weights1)/2
                #weights2 = (birds[0].nnet.weights2 + birds[1].nnet.weights2)/2
                mat1 = np.random.randint(2, size = birds[0].nnet.weights1.shape)
                mat2 = np.random.randint(2, size = birds[0].nnet.weights2.shape)
                weights1 = np.multiply(birds[0].nnet.weights1, mat1) + np.multiply(birds[1].nnet.weights1, 1 - mat1)
                weights2 = np.multiply(birds[0].nnet.weights2, mat2) + np.multiply(birds[1].nnet.weights2, 1 - mat2)
                mutation = np.random.random()<MUTATION_RATE
                if(mutation):
                    weights1 += np.random.normal(0, np.std(weights1)/10, weights1.shape)
                    weights2 += np.random.normal(0, np.std(weights2)/10, weights2.shape)
                self.list_birds[k].nnet.weights1 = weights1
                self.list_birds[k].nnet.weights2 = weights2
            elif(k<N_BIRD*(BREED1_RATE+2*BREED2_RATE)):
                birds = np.random.choice(best2Birds, 2, replace = True)
                #weights1 = (birds[0].nnet.weights1 + birds[1].nnet.weights1)/2
                #weights2 = (birds[0].nnet.weights2 + birds[1].nnet.weights2)/2
                for child in range(2):
                    mat1 = np.random.randint(2, size = birds[0].nnet.weights1.shape)
                    mat2 = np.random.randint(2, size = birds[0].nnet.weights2.shape)
                    weights1 = np.multiply(birds[0].nnet.weights1, mat1) + np.multiply(birds[1].nnet.weights1, 1 - mat1)
                    weights2 = np.multiply(birds[0].nnet.weights2, mat2) + np.multiply(birds[1].nnet.weights2, 1 - mat2)
                    mutation = np.random.random()<MUTATION_RATE
                    if(mutation):
                        weights1 += np.random.normal(0, np.std(weights1)/10, weights1.shape)
                        weights2 += np.random.normal(0, np.std(weights2)/10, weights2.shape)
                    self.list_birds[k].nnet.weights1 = weights1
                    self.list_birds[k].nnet.weights2 = weights2
                    k+=1
            else:
                bird = sortedBirds[0]#np.random.choice(best2Birds, 1, replace = True)[0]
                mutation = np.random.random()<MUTATION_RATE
                weights1 = bird.nnet.weights1
                weights2 = bird.nnet.weights2
                if(mutation):
                    weights1 += np.random.normal(0, np.std(weights1)/10, weights1.shape)
                    weights2 += np.random.normal(0, np.std(weights2)/10, weights2.shape)
                self.list_birds[k].nnet.weights1 = weights1
                self.list_birds[k].nnet.weights2 = weights2

    def new_generation(self):
        self.gen += 1
        self.draw_new_generation()
       


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if(self.state == GameStates.RUNNING):
            self.updateScore()   
            self.updateBirds()
            self.updatePipes()
            self.moveGround()
            for pipe in self.list_pipes:
                pipe.move()          
        pass

def main():
    
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

