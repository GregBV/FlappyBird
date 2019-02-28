import numpy as np
import arcade
import Base



class Bird:
    def __init__(self):
        self.x = Base.X_BIRD
        self.y = Base.SCREEN_HEIGHT//2
        self.v = 0
        self.r = Base.R_BIRD
        self.fitness = 0
        self.dead = False
        self.key = None
        self.nnet = None
        self.sprite = arcade.Sprite("sprites/pixel_bird.png", Base.SPRITE_SCALING_BIRD)
        self.dead_sprite = arcade.Sprite("sprites/pixel_dead.png", Base.SPRITE_SCALING_BIRD)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def collision(self, pipe):#, gap_height, screen_height):
        
        DeltaX = self.x - max(pipe.x -pipe.w//2, min(self.x, pipe.x + pipe.w//2))
        DeltaY1 = self.y - max(0, min(self.y, pipe.h))
        DeltaY2 = self.y - max(pipe.h+Base.GAP_HEIGHT, min(self.y, Base.SCREEN_HEIGHT))

        return DeltaX**2 + DeltaY1**2 < self.r**2 or DeltaX**2 + DeltaY2**2 < self.r**2
    
    def move(self, pipes, key):#, jump_speed, gravity, gap_height, screen_height):
        if(self.dead):
            pass
        if(key == 1):
            self.v = Base.JUMP_SPEED
        self.v -= Base.GRAVITY
        self.y += round(self.v)
        self.sprite.center_y = self.y
        self.sprite.angle = 0
        if(self.v<0):
            self.sprite.angle = 2*self.v
        if(self.y - self.r <= 80 or self.y +self.r >= Base.SCREEN_HEIGHT or self.collision(pipes[0])):#, gap_height, screen_height)):
            #self.fitness-=int(abs(pipes[0].h - self.y))
            self.dead = True
            self.sprite.kill()