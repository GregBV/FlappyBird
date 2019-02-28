import Base
import random
import arcade



class Pipe:
    def __init__(self):
        self.x = Base.SCREEN_WIDTH + Base.PIPE_WIDTH//2
        self.y = random.randint(Base.SCREEN_HEIGHT//6, 2*Base.SCREEN_HEIGHT//6) - Base.GAP_HEIGHT//4
        self.w = Base.PIPE_WIDTH
        self.h = 2*self.y
        self.v = Base.PIPE_SPEED
        self.sprite_down = arcade.Sprite("sprites/pipe_down.png", Base.SPRITE_SCALING_PIPE)
        self.sprite_down.center_x = self.x
        self.sprite_down.center_y = -Base.SPRITE_SCALING_PIPE*400 + self.h

        self.sprite_up = arcade.Sprite("sprites/pipe_up.png", Base.SPRITE_SCALING_PIPE)
        self.sprite_up.center_x = self.x
        self.sprite_up.center_y = Base.GAP_HEIGHT + self.h + Base.SPRITE_SCALING_PIPE*400


    def move(self):
        self.x -= self.v
        self.sprite_up.center_x = self.x
        self.sprite_down.center_x = self.x