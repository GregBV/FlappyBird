import arcade
from enum import Enum
import random
import Bird
import Pipe
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


class Base(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, n_bird):
        super().__init__(width, height)
        
        # score
        self.score = 0

        self.background = arcade.load_texture("sprites/background.png")


        self.list_birds = [Bird.Bird() for k in range(n_bird)]
        self.sprite_list_birds = arcade.SpriteList(use_spatial_hash=False)
        for bird in self.list_birds:
            self.sprite_list_birds.append(bird.sprite)

        self.sprite_list_ground = arcade.SpriteList(use_spatial_hash=False)
        for k in range(ceil(SCREEN_WIDTH/80)+1):
            self.sprite_list_ground.append(arcade.Sprite("sprites/city2.png", 4))
            self.sprite_list_ground[-1].center_x = GROUND_HEIGHT*k
            self.sprite_list_ground[-1].center_y = GROUND_HEIGHT//2

        self.list_pipes = [Pipe.Pipe()]
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
                self.list_pipes.append(Pipe.Pipe())
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
        self.list_birds = [Bird.Bird() for k in range(n_bird)]
        self.sprite_list_birds = arcade.SpriteList(use_spatial_hash=False)
        for bird in self.list_birds:
            self.sprite_list_birds.append(bird.sprite)
        
        self.list_pipes = [Pipe.Pipe()]
        self.sprite_list_pipes = arcade.SpriteList(use_spatial_hash=False)
        for p in self.list_pipes:
            self.sprite_list_pipes.append(p.sprite_up)
            self.sprite_list_pipes.append(p.sprite_down)
        self.score = 0