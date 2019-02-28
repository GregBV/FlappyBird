from enum import Enum
import random
import numpy as np
from math import ceil
from Base import *



class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1
    END = 2
    START = 3

class Game(Base):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, 1)
        self.state = GameStates.START
        # Set constant for bird
        

        # score

        self.i = 0

        

    def setup(self):
        # Set up your game here
        self.state = GameStates.RUNNING
        pass


    def gameOverScreen(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 2560*SCREEN_HEIGHT//1440, SCREEN_HEIGHT, self.background)
        arcade.draw_text('GAME OVER', SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.RED, 50, width=200, align="center",
                         anchor_x="center", anchor_y="center")
        arcade.draw_text('score\n' + str(self.score), SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, arcade.color.BLACK, 11, width=50, align="center",
                        anchor_x="center", anchor_y="center")
        arcade.draw_text('PRESS SPACE TO RESTART', SCREEN_WIDTH//2, 100, arcade.color.WHITE, 20, width=200, align="center",
                        anchor_x="center", anchor_y="center")
    
    def startScreen(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 2560*SCREEN_HEIGHT//1440, SCREEN_HEIGHT, self.background)

        self.sprite_list_birds.draw()
        self.sprite_list_ground.draw()
        arcade.draw_text('FLAPPY BIRD', SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.RED, 50, width=200, align="center",
                         anchor_x="center", anchor_y="center")

        arcade.draw_text('PRESS SPACE TO START', SCREEN_WIDTH//2, 150, arcade.color.WHITE, 20, width=200, align="center",
                        anchor_x="center", anchor_y="center")


    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        if(self.state == GameStates.START):
                self.startScreen()
        else:
            self.levelScreen()
            if(self.state == GameStates.GAME_OVER) :
                self.gameOverScreen()



        
    def on_key_press(self, key, modifiers):
        if(key == arcade.key.SPACE and self.state == GameStates.RUNNING):
            self.list_birds[0].v = 12
        if(key == arcade.key.SPACE and (self.state == GameStates.START or self.state == GameStates.GAME_OVER)):
            self.restart()
            

    def endAnimation(self):
        bird = self.list_birds[0]
        bird.v -= GRAVITY
        bird.y += bird.v
        bird.dead_sprite.center_x = bird.x
        bird.dead_sprite.center_y = bird.y
        if(bird.y <= 0):
            self.state = GameStates.GAME_OVER
    
    def startEndAnimation(self):
        bird = self.list_birds[0]
        bird.v = 12
        self.sprite = bird.dead_sprite
        bird.dead_sprite.center_x = bird.x
        bird.dead_sprite.center_y = bird.y
        self.sprite_list_birds.append(self.list_birds[0].dead_sprite)
        self.state = GameStates.END

    def startAnimation(self, i):
        bird = self.list_birds[0]
        k=2*((i//50)%2)-1
        bird.y += k
        bird.sprite.center_y = bird.y

    def restart(self):
        super().restart(1)
        self.list_birds[0].v = 12
        self.state = GameStates.RUNNING

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if(self.state == GameStates.START):
            self.moveGround()
            self.startAnimation(self.i)
            self.i+=1
            pass
        if(self.state == GameStates.END):
            self.endAnimation()
            pass
        if(self.state == GameStates.RUNNING):
            
            bird = self.list_birds[0]
            if(bird.dead):
                self.startEndAnimation()
                pass
            self.updateScore()
            
            bird.move(self.list_pipes, 0)
            # manage pipes
            self.moveGround()
            self.updatePipes()
            for pipe in self.list_pipes:
                pipe.move()   

        pass


def main():
    Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()