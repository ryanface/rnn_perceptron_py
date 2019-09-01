import arcade
import os
from numpy import exp, array, random, dot
import numpy as np
import network as rnn

SPRITE_SCALING = 0.5
GRAVITY = 0.1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "RNN + Genetic algorithm"

MOVEMENT_SPEED = 5
MAX = 200

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.score = 0
        self.score_timeout = 0
        self.generations = 0

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None

        # Create layer 1/2 (3 neurons, each with 3 inputs)
        self.layer1 = rnn.NeuronLayer(3, 4)
        self.layer2 = rnn.NeuronLayer(4, 4)
        self.perceptron = rnn.NeuralNetwork(self.layer1, self.layer2)
        self.genoma_list = []
        self.better = None

    def get_better(self):
        self.genoma_list = []
        if self.better == None:
            self.better = self.player_list[0]

        #get better 
        for i in range( len(self.player_list) ):
            if( self.better.position[1] < self.player_list[i].position[1]):
                print('better',self.better.position[1], self.player_list[i].position[1] )
                self.better = self.player_list[i]

    def mutate(self, player):
        count = 0
        for i in range( len(player.weights1) ): 
            for x in range( len(player.weights1[i]) ):
                if random.uniform(0, 1) < 0.3 or self.better == None:
                        player.weights1[i][x] = random.uniform(0, 1) if random.uniform(0, 1) < 0.5 else random.uniform(0, 1) -1
                        count += 1
                else:
                        player.weights2[i] = self.better.weights2[i]    

        for i in range( len(player.weights2) ): 
            for x in range( len(player.weights2[i]) ):
                #print(player.weights2[i][x])
                if random.uniform(0, 1) < 0.3  or self.better == None:
                        player.weights2[i][x] = random.uniform(0, 1) if random.uniform(0, 1) < 0.5 else random.uniform(0, 1) -1                    
                        count += 1
                else:
                        player.weights2[i] = self.better.weights2[i]  
        print('mutations',self.generations, count)
        return  player.weights1, player.weights2

    def genoma(self, player):
        self.genoma_list = []
        #for i in range( len(self.player_list) ):
        #    weights1, weights2 = self.better.weights1, self.better.weights2          
        if random.uniform(0, 1) < 0.8:
            weights1, weights2 = self.mutate( player ) 
            return weights1, weights2, True
        else:
            if(self.better == None):
                return 0, 0, False
            else:    
                return self.better.weights1, self.better.weights2, True 


    def startnewgame(self):
        print('------------------startnewgame----------------') 
        self.generations += 1
        for x in range( MAX ):
            self.player_sprite = arcade.Sprite("images/ballon3.png",SPRITE_SCALING)
            self.player_sprite.center_x = 150 + random.uniform(1,50)
            self.player_sprite.center_y = 100
            self.player_sprite.weights1 = 2 * random.random((3, 4)) - 1
            self.player_sprite.weights2 = 2 * random.random((4, 4)) - 1                    
            mutation1, mutation2, mutate = self.genoma(self.player_sprite)
            if( mutate ):
                self.player_sprite.weights1 = mutation1
                self.player_sprite.weights2 = mutation2            

            self.player_list.append(self.player_sprite)

        for player in self.player_list:
            player.physics = arcade.PhysicsEnginePlatformer(player, self.wall_list, GRAVITY)    

    def action_reliase(self, player, action):
        if action == 0:
            player.change_y = MOVEMENT_SPEED
        elif action == 1:
            player.change_y = -MOVEMENT_SPEED
        elif action == 2:
            player.change_x = -MOVEMENT_SPEED
        elif action == 3:
            player.change_x = MOVEMENT_SPEED        
        else:
            player.change_x = 0
            player.change_y = 0

    def setup(self):

        self.score = 0
        self.score_timeout = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # -- Set up the walls
        for x in range(10):
            wall = arcade.Sprite("images/platform.png", SPRITE_SCALING)
            wall.center_x = x*200
            wall.center_y = 2
            self.wall_list.append(wall)

        for x in range(2):
            wall = arcade.Sprite("images/platform.png", SPRITE_SCALING)
            wall.center_x = x*200
            wall.center_y = 200
            self.wall_list.append(wall)

        for x in range(4):
            wall = arcade.Sprite("images/platform.png", SPRITE_SCALING)
            wall.center_x = 200+(x*200)
            wall.center_y = 500
            self.wall_list.append(wall)

        for x in range(2):
            wall = arcade.Sprite("images/platform.png", SPRITE_SCALING)
            wall.center_x = 200+(x*200)
            wall.center_y = 400
            self.wall_list.append(wall)

        for x in range(40):
            wall = arcade.Sprite("images/platform.png", SPRITE_SCALING)
            wall.center_x = 880
            wall.center_y = 15*(x)
            self.wall_list.append(wall)    

        for x in range(40):
            wall = arcade.Sprite("images/platform.png", SPRITE_SCALING)
            wall.center_x = -80
            wall.center_y = 15*(x)
            self.wall_list.append(wall)                      

        # Set up the player
        self.startnewgame()

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

        # score
        score_text = f"Time: {self.score}"
        arcade.draw_text(score_text, 50, 570,arcade.csscolor.WHITE, 10)
        generations_text = f"Generations: {self.generations}"
        arcade.draw_text(generations_text, 50, 560,arcade.csscolor.WHITE, 10)        


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        self.score_timeout += delta_time
        self.score = int(self.score_timeout) % 60
        
        # See if we hit any coins
        for player in self.player_list:    
            player.physics.update() 
            
            if(player.position[1] > 200):
                plataform = 200
            elif(player.position[1] > 400):
                plataform = 400   
            else:    
                plataform = 698   

            hidden_state, output = self.perceptron.run([player.position[0], player.position[1], plataform], player.weights1, player.weights2) 
            A = np.array(output)
            #H = np.array(hidden_state)
            #hidden = np.where(H==max(hidden_state))[0][0]
            action = np.where(A==max(output))[0][0]
            #print(action , hidden_state, output)

            self.action_reliase(player,action)           
            

        if(self.score > 30) :
            self.score_timeout = 0

            print('start genoma')
            self.get_better()            
            print('end genoma')
            
            while len(self.player_list) > 0:
                for player in self.player_list:      
                    player.kill()  

            print('startnewgame')  
            self.startnewgame()                       


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()