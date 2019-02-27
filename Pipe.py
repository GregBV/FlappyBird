import FlappyLearn
import Game
import random
import arcade



class Pipe:
    def __init__(self, screen_width, screen_height, pipe_width, pipe_speed, gap_height, SPRITE_SCALING_PIPE):
        self.x = screen_width + pipe_width//2
        self.y = random.randint(screen_height//6, 2*screen_height//6) - gap_height//4
        self.w = pipe_width
        self.h = 2*self.y
        self.v = pipe_speed
        self.sprite_down = arcade.Sprite("sprites/pipe_down.png", SPRITE_SCALING_PIPE)
        self.sprite_down.center_x = self.x
        self.sprite_down.center_y = -SPRITE_SCALING_PIPE*400 + self.h

        self.sprite_up = arcade.Sprite("sprites/pipe_up.png", SPRITE_SCALING_PIPE)
        self.sprite_up.center_x = self.x
        self.sprite_up.center_y = gap_height + self.h + SPRITE_SCALING_PIPE*400


    def move(self):
        self.x -= self.v
        self.sprite_up.center_x = self.x
        self.sprite_down.center_x = self.x