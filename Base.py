import arcade
from enum import Enum
import random
import numpy as np
from math import ceil

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
GRAVITY = 0.7
PIPE_SPEED = 3
PIPE_WIDTH = 70
GAP_HEIGHT = 200
JUMP_SPEED = 8
X_BIRD = 100
R_BIRD = 30
GROUND_HEIGHT = 80

SPRITE_SCALING_PIPE = PIPE_WIDTH/26
SPRITE_SCALING_BIRD = 1

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH + PIPE_WIDTH//2
        self.y = random.randint(SCREEN_HEIGHT//6, 2*SCREEN_HEIGHT//6) - GAP_HEIGHT//4
        self.w = PIPE_WIDTH
        self.h = 2*self.y
        self.v = PIPE_SPEED
        self.sprite_down = arcade.Sprite("sprites/pipe_down.png", SPRITE_SCALING_PIPE)
        self.sprite_down.center_x = self.x
        self.sprite_down.center_y = -SPRITE_SCALING_PIPE*400 + self.h

        self.sprite_up = arcade.Sprite("sprites/pipe_up.png", SPRITE_SCALING_PIPE)
        self.sprite_up.center_x = self.x
        self.sprite_up.center_y = GAP_HEIGHT + self.h + SPRITE_SCALING_PIPE*400


    def move(self):
        self.x -= self.v
        self.sprite_up.center_x = self.x
        self.sprite_down.center_x = self.x

class Bird:
    def __init__(self):
        self.x = X_BIRD
        self.y = SCREEN_HEIGHT//2
        self.v = 0
        self.r = R_BIRD
        self.fitness = 0
        self.dead = False
        self.key = None
        self.nnet = None
        self.sprite = arcade.Sprite("sprites/pixel_bird.png", SPRITE_SCALING_BIRD)
        self.dead_sprite = arcade.Sprite("sprites/pixel_dead.png", SPRITE_SCALING_BIRD)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def collision(self, pipe):#, gap_height, screen_height):
        
        DeltaX = self.x - max(pipe.x -pipe.w//2, min(self.x, pipe.x + pipe.w//2))
        DeltaY1 = self.y - max(0, min(self.y, pipe.h))
        DeltaY2 = self.y - max(pipe.h+GAP_HEIGHT, min(self.y, SCREEN_HEIGHT))

        return DeltaX**2 + DeltaY1**2 < self.r**2 or DeltaX**2 + DeltaY2**2 < self.r**2
    
    def move(self, pipes, key):#, jump_speed, gravity, gap_height, screen_height):
        if(self.dead):
            pass
        if(key == 1):
            self.v = JUMP_SPEED
        self.v -= GRAVITY
        self.y += round(self.v)
        self.sprite.center_y = self.y
        self.sprite.angle = 0
        if(self.v<0):
            self.sprite.angle = 2*self.v
        if(self.y - self.r <= 80 or self.y +self.r >= SCREEN_HEIGHT or self.collision(pipes[0])):#, gap_height, screen_height)):
            #self.fitness-=int(abs(pipes[0].h - self.y))
            self.dead = True
            self.sprite.kill()


class Base(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, n_bird):
        super().__init__(width, height)
        
        # score
        self.score = 0

        self.background = arcade.load_texture("sprites/background.png")


        self.list_birds = [Bird() for k in range(n_bird)]
        self.sprite_list_birds = arcade.SpriteList(use_spatial_hash=False)
        for bird in self.list_birds:
            self.sprite_list_birds.append(bird.sprite)

        self.sprite_list_ground = arcade.SpriteList(use_spatial_hash=False)
        for k in range(ceil(SCREEN_WIDTH/80)+1):
            self.sprite_list_ground.append(arcade.Sprite("sprites/city2.png", 4))
            self.sprite_list_ground[-1].center_x = GROUND_HEIGHT*k
            self.sprite_list_ground[-1].center_y = GROUND_HEIGHT//2

        self.list_pipes = [Pipe()]
        self.sprite_list_pipes = arcade.SpriteList(use_spatial_hash=False)
        for p in self.list_pipes:
            self.sprite_list_pipes.append(p.sprite_up)
            self.sprite_list_pipes.append(p.sprite_down)

        

    def levelScreen(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 2560*SCREEN_HEIGHT//1440, SCREEN_HEIGHT, self.background)
        self.sprite_list_pipes.draw()
        self.sprite_list_ground.draw()
        self.sprite_list_birds.draw()

        # Draw score
        arcade.draw_text('score\n' + str(self.score), SCREEN_WIDTH//2, SCREEN_HEIGHT - 25, arcade.color.BLACK, 11, width=50, align="center",
                        anchor_x="center", anchor_y="center")

    def updatePipes(self):
        if(abs(self.list_pipes[-1].x -PIPE_WIDTH//2 - SCREEN_WIDTH//2)<PIPE_SPEED):
                self.list_pipes.append(Pipe())
                self.sprite_list_pipes.append(self.list_pipes[-1].sprite_up)
                self.sprite_list_pipes.append(self.list_pipes[-1].sprite_down)
        
        if(self.list_pipes[0].x <= -PIPE_WIDTH//2):
            self.list_pipes.pop(0)

    def updateScore(self):
        if(abs(X_BIRD - self.list_pipes[0].x)<PIPE_SPEED):
                self.score += 1
                return True
        return False

    def updateGround(self):
        if(self.sprite_list_ground[0].center_x<=-GROUND_HEIGHT//2):
            for s in self.sprite_list_ground:
                s.center_x += GROUND_HEIGHT

    def moveGround(self):
        for s in self.sprite_list_ground:
            s.center_x -= PIPE_SPEED
        self.updateGround()

    def restart(self, n_bird):
        self.list_birds = [Bird() for k in range(n_bird)]
        self.sprite_list_birds = arcade.SpriteList(use_spatial_hash=False)
        for bird in self.list_birds:
            self.sprite_list_birds.append(bird.sprite)
        
        self.list_pipes = [Pipe()]
        self.sprite_list_pipes = arcade.SpriteList(use_spatial_hash=False)
        for p in self.list_pipes:
            self.sprite_list_pipes.append(p.sprite_up)
            self.sprite_list_pipes.append(p.sprite_down)
        self.score = 0