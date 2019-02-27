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

class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1
    END = 2
    START = 3

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.state = GameStates.START
        # Set constant for bird
        self.bird = Bird.Bird(X_BIRD, SCREEN_HEIGHT//2, R_BIRD, SPRITE_SCALING_BIRD)
        
        self.pipes = None

        # score
        self.score = int()

        self.i = 0
        #arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("sprites/background.png")#"sprites/ShowMeWhatYouGot.jpg")

        self.sprite_list_birds = arcade.SpriteList()

        self.sprite_list_birds.append(self.bird.sprite)

        self.sprite_list_ground = arcade.SpriteList()
        print(ceil(SCREEN_WIDTH/80)+1)
        for k in range(ceil(SCREEN_WIDTH/80)+1):
            self.sprite_list_ground.append(arcade.Sprite("sprites/city2.png", 4))
            self.sprite_list_ground[-1].center_x = GROUND_HEIGHT*k
            self.sprite_list_ground[-1].center_y = GROUND_HEIGHT//2

        

    def setup(self):
        # Set up your game here
        self.state = GameStates.RUNNING
        # Set constant for bird
        self.bird = Bird.Bird(X_BIRD, SCREEN_HEIGHT//2, R_BIRD, SPRITE_SCALING_BIRD)
        self.sprite_list_birds = arcade.SpriteList()

        self.sprite_list_birds.append(self.bird.sprite)

        # Set constant for pipe

        

        # count frames
        self.score = 0

        


        pass



    def levelScreen(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 2560*SCREEN_HEIGHT//1440, SCREEN_HEIGHT, self.background)
        self.sprite_list_pipes.draw()
        self.sprite_list_ground.draw()
        self.sprite_list_birds.draw()

        # Draw score
        arcade.draw_text('score\n' + str(self.score), SCREEN_WIDTH//2, SCREEN_HEIGHT - 25, arcade.color.BLACK, 11, width=50, align="center",
                        anchor_x="center", anchor_y="center")




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
            self.bird.v = 12
        if(key == arcade.key.SPACE and (self.state == GameStates.START or self.state == GameStates.GAME_OVER)):
            self.setup()
            self.bird.v = 12

    def endAnimation(self):
        bird = self.bird
        bird.v -= GRAVITY
        bird.y += bird.v
        bird.dead_sprite.center_x = bird.x
        bird.dead_sprite.center_y = bird.y
        if(bird.y <= 0):
            self.state = GameStates.GAME_OVER
    
    def startEndAnimation(self):
        bird = self.bird
        bird.v = 12
        self.sprite = bird.dead_sprite
        bird.dead_sprite.center_x = bird.x
        bird.dead_sprite.center_y = bird.y
        self.sprite_list_birds.append(self.bird.dead_sprite)
        self.state = GameStates.END

    def startAnimation(self, i):

        k=2*((i//50)%2)-1
        self.bird.y += k
        self.bird.sprite.center_y = self.bird.y

    def updateScore(self):
        if(abs(X_BIRD - self.list_pipes[0].x)<PIPE_SPEED):
                self.score += 1
                return True
        return False

    def updatePipes(self):
        if(abs(self.list_pipes[-1].x -PIPE_WIDTH//2 - SCREEN_WIDTH//2)<PIPE_SPEED):
                self.list_pipes.append(Pipe.Pipe(SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_WIDTH, PIPE_SPEED, GAP_HEIGHT, SPRITE_SCALING_PIPE))
                self.sprite_list_pipes.append(self.list_pipes[-1].sprite_up)
                self.sprite_list_pipes.append(self.list_pipes[-1].sprite_down)
        
        if(self.list_pipes[0].x <= -PIPE_WIDTH//2):
            #self.sprite_list_pipes[0].kill()
            self.list_pipes.pop(0)

    def updateGround(self):
        
        if(self.sprite_list_ground[0].center_x<=-GROUND_HEIGHT//2):
            for s in self.sprite_list_ground:
                s.center_x += GROUND_HEIGHT
    
    def moveGround(self):
        for s in self.sprite_list_ground:
            s.center_x -= PIPE_SPEED
        self.updateGround()

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
            
            bird = self.bird
            if(bird.dead):
                self.startEndAnimation()
                pass
            self.updateScore()
            
            bird.move(self.list_pipes, 0, JUMP_SPEED, GRAVITY, GAP_HEIGHT, SCREEN_HEIGHT)
            # manage pipes
            self.moveGround()
            self.updatePipes()
            for pipe in self.list_pipes:
                pipe.move()   

        pass


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()