import numpy as np
import arcade



class Bird:
    def __init__(self, x, y, r, SPRITE_SCALING_BIRD):
        self.x = x
        self.y = y
        self.v = 0
        self.r = r
        self.fitness = 0
        self.dead = False
        self.key = None
        self.nnet = None
        self.sprite = arcade.Sprite("sprites/pixel_bird.png", SPRITE_SCALING_BIRD)
        self.dead_sprite = arcade.Sprite("sprites/pixel_dead.png", SPRITE_SCALING_BIRD)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def collision(self, pipe, gap_height, screen_height):
        
        DeltaX = self.x - max(pipe.x -pipe.w//2, min(self.x, pipe.x + pipe.w//2))
        DeltaY1 = self.y - max(0, min(self.y, pipe.h))
        DeltaY2 = self.y - max(pipe.h+gap_height, min(self.y, screen_height))

        return DeltaX**2 + DeltaY1**2 < self.r**2 or DeltaX**2 + DeltaY2**2 < self.r**2
    
    def move(self, pipes, key, jump_speed, gravity, gap_height, screen_height):
        if(self.dead):
            pass
        if(key == 1):
            self.v = jump_speed
        self.v -= gravity
        self.y += round(self.v)
        self.sprite.center_y = self.y
        self.sprite.angle = 0
        if(self.v<0):
            
            self.sprite.angle = 2*self.v
        if(self.y - self.r <= 80 or self.y +self.r >= screen_height or self.collision(pipes[0], gap_height, screen_height)):
            #self.fitness-=int(abs(pipes[0].h - self.y))
            self.dead = True
            self.sprite.kill()