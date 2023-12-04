import pathlib
import random
import arcade

# all global variables that the code needs to access in every class/View
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
pipeGapList = []
HIGH_SCORES = [0]
SCROLL_SPEED = 2
HEIGHT_DIFF = 75
SCROLL_INCREASE = 0.05

# creating the bird sprite
class Bird (arcade.Sprite):

    # initializing all variables for bird
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = 100
        self.center_y = 450
        self.angle = 0
        self.veloBird = 0
        self.veloFall = -0.5
        self.maxFall = -7
        self.deadFall = -10
        self.maxJump = 8.5
        self.veloAngle = 0
        self.angleFall = -0.25
        self.jumpAngle = 75
        self.minAngle = -90
        self.maxAngle = 45
        self.is_jumping = False
        self.is_dead = False
        self.is_grounded = False


    # creating the movement for the bird every time the bird is updated in the game View
    def update(self, symbol = None):

        # when the bird is not dead we need to make the bird fall and jump to prevent the bird from falling
        if not self.is_dead:
            self.veloBird += self.veloFall
            self.center_y += self.veloBird
            if self.veloBird < self.maxFall:
                self.veloBird = self.maxFall
            if symbol == arcade.key.SPACE and self.center_y > 0:
                self.is_jumping = True
                self.veloBird = 0
                self.veloBird += self.maxJump
                self.veloAngle = 0
                self.veloAngle += self.jumpAngle
            if self.veloBird < self.maxJump-2.5:
                self.veloAngle += self.angleFall
                self.angle += self.veloAngle // 2
            if self.angle < self.minAngle:
                self.angle = self.minAngle
            if self.angle > self.maxAngle:
                self.angle = self.maxAngle
                self.veloAngle = 0

        # when the bird is dead we need to make the bird fall until they hit the ground then stop
        else:
            if self.is_grounded:
                self.veloAngle = 0
                self.veloBird = 0
            else:
                self.veloAngle = 0
                if self.veloBird > 0:
                    self.veloBird = 0
                if self.angle > self.minAngle:
                    self.veloAngle += self.deadFall
                    self.angle += self.veloAngle // 2
                if self.angle <= self.minAngle:
                    self.angle = self.minAngle
                    self.veloAngle = 0
                self.veloBird += self.veloFall
                self.center_y += self.veloBird
                if self.veloBird < self.deadFall:
                    self.veloBird = self.deadFall


# creating the pipes (both bottom and top go into this class individually but simultaneously)
class Pipe(arcade.Sprite):

    # initializing variables (mostly location of pipes)
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = SCREEN_WIDTH + SCREEN_WIDTH//3
        self.moveSpeed = SCROLL_SPEED
        self.topHeight = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//4
        self.bottomHeight = SCREEN_HEIGHT//2 - SCREEN_HEIGHT//8
        self.offRandomTop = 75
        self.xRemovePipe = -50

        # if the pipe is the top one then set the bottom of the top. if the pipe is the bottom then we need to set the top of the bottom.
        if image == "images/topPipe.png":
            randNumPipe = random.randint(self.bottomHeight, self.topHeight)
            pipeGapList.append(randNumPipe)
            self.bottom = randNumPipe + self.offRandomTop
        else:
            self.top = pipeGapList[-1] - HEIGHT_DIFF
            pipeGapList.pop(0)

    # just need to update location of pipe by moving x left one every update (also removing pipe after it leaves the screen to save memory)
    # need to use SCROLL_SPEED for moveSpeed because later we will increase the scroll speed incrementally to make the game harder as the game continues.
    def update(self):
        self.center_x -= self.moveSpeed
        if self.center_x < self.xRemovePipe:
            self.remove_from_sprite_lists()
        super(Pipe, self).update()


# creating the ground (so it moves with the game)
class Ground(arcade.Sprite):

    # initialize the variables
    def __init__(self, image, scale, centerX):
        super().__init__(image, scale)
        self.center_x = centerX
        self.center_y = 50
        self.moveSpeed = SCROLL_SPEED

    # move the ground sprite left one every update (same speed as pipes using same variable SCROLL_SPEED)
    def update(self):
        self.center_x -= self.moveSpeed
        super(Ground, self).update()


# creating the starting screen View
class StartingScreen(arcade.View):

    # initializing image variables
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture('images/BackGround.png')
        self.flappyWords = arcade.load_texture('images/newStartingScreen.png')
        self.startingFlappyImage = arcade.load_texture('images/bird2.0.png')

    # function used to bring the images to the screen (most numbers used are non-mathematical just eyeballed to my liking)
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_lrwh_rectangle_textured(100-20, 425, 296*0.15, 264*0.15, self.startingFlappyImage)
        arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH//2-125, SCREEN_HEIGHT//2+50, 257, 250, self.flappyWords)
        arcade.draw_text("Press Spacebar ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("to jump ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Press Space to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    # creating function that allows player to move on to the next screen (the game) by pressing Space and only Space
    def on_key_release(self, symbol, modifier):
            if symbol == arcade.key.SPACE:
                game_view = Game()
                game_view.setup()
                self.window.show_view(game_view)


# creating the game View (the View where the game is actually played)
class Game(arcade.View):

    # initializing all variables (lots)
    def __init__(self):
        super().__init__()
        self.background = None
        self.bottom_pipe_image = None
        self.top_pipe_image = None
        self.bird = None
        self.pipeTop = None
        self.pipeBot = None
        self.pipeWidth = 0
        self.centerX = 0
        self.pipeHeight = 0
        self.randPipeList = []
        self.count = 0
        self.gameOver = False
        self.ground = None
        self.pastPipes = []
        self.checkPointSpeed = []
        self.checkPointSize = []
        self.pipe_timer = 150
        self.frame_count = 0
        self.birdSpriteList = arcade.SpriteList()
        self.pipeSpriteList = arcade.SpriteList()
        self.groundSpriteList = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()

    # called whenever the player presses Space and will update the Bird Sprite (which has an if statement testing if Space is being pressed which will make the bird jump if True)
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.bird.update(symbol)

    # setting up the variables/objects for every image/sprite prior to the game starting/updating
    def setup(self):
        self.background = arcade.load_texture("images/BackGround.png")
        self.all_sprites_list = arcade.SpriteList()
        self.bird = Bird("images/bird2.0.png", 0.15)
        self.pipeTop = Pipe("images/topPipe.png", 1)
        self.pipeBot = Pipe("images/bottomPipe.png", 1)
        self.ground = Ground("images/NewGround.png", 1, SCREEN_WIDTH//2)
        self.birdSpriteList.append(self.bird)
        self.all_sprites_list.append(self.bird)
        self.pipeSpriteList.append(self.pipeTop)
        self.pipeSpriteList.append(self.pipeBot)
        self.all_sprites_list.append(self.pipeTop)
        self.all_sprites_list.append(self.pipeBot)
        self.groundSpriteList.append(self.ground)
        self.all_sprites_list.append(self.ground)


    # rendering the screen
    def on_draw(self):
        arcade.start_render()
        self.draw_game()

    # drawing background as well as drawing the new locations for every sprite after every update
    def draw_game(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.pipeSpriteList.draw()
        self.groundSpriteList.draw()
        self.birdSpriteList.draw()
        arcade.draw_text(self.count, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, font_name = 'Kenny Blocks Font', bold = True,font_size=40, anchor_x="center")

    # most important method, updates the game and actually brings the sprites to life
    def update(self, delta_time):

        # testing if the bird is dead, if it's not then the bird needs to be updated
        if not self.bird.is_dead:
            self.all_sprites_list.update()

            # testing if the counter is even, if it is then the scroll_speed needs to be increased (making the game harder)
            if self.count % 2 == 0 and self.count != 0 and self.count not in self.checkPointSpeed:
                self.checkPointSpeed.append(self.count)
                global SCROLL_SPEED
                global SCROLL_INCREASE
                SCROLL_SPEED += SCROLL_INCREASE

            # Makes difference between pipes smaller and smaller every 5 pipes. Works just fine but sets a cap on how far the player can reach unless you place a cap on how small the difference can be. Not sure if I want to keep it.
            # if self.count+1 % 5 == 0 and self.count+1 != 0 and self.count+1 not in self.checkPointSize:
            #     self.checkPointSize.append(self.count+1)
            #     print(self.checkPointSize)
            #     global HEIGHT_DIFF
            #     HEIGHT_DIFF -= 5

            # testing location of pipe and if the bird has passed the right side of the pipe the counter will increase
            if self.pipeSpriteList[1].right < self.bird.left:

                # creating a list of pipes the bird has passed to prevent double counting (updates make counting hard)
                if self.pipeSpriteList[1] not in self.pastPipes:
                    self.pastPipes.append(self.pipeSpriteList[1])
                    self.count += 1

                    # once the bird passes a second pipe the first will be removed from list (saving memory)
                    if len(self.pastPipes) > 1:
                        self.pastPipes.pop(0)

            # creating more ground sprites every so often to make it appear as if ground is infinite
            if self.groundSpriteList[-1].center_x < 0:
                self.ground = Ground("images/NewGround.png", 1, self.ground.right + (self.ground.width//2)-10)
                self.groundSpriteList.append(self.ground)
                self.all_sprites_list.append(self.ground)

            # same concept as teh ground sprites (need to create more to make it appear as if the pipes are never ending too)
            if self.pipeTop.center_x < SCREEN_WIDTH//1.5:
                self.pipeTop = Pipe("images/topPipe.png", 1)
                self.pipeBot = Pipe("images/bottomPipe.png", 1)
                self.pipeSpriteList.append(self.pipeTop)
                self.pipeSpriteList.append(self.pipeBot)
                self.all_sprites_list.append(self.pipeTop)
                self.all_sprites_list.append(self.pipeBot)

            # testing if the bird has hit the ceiling, ground, or a pipe and if it has then the bird is dead and will no longer perform the updates from above)
            if self.bird.collides_with_list(self.all_sprites_list) or self.bird.center_y >= SCREEN_HEIGHT or self.bird.center_y <= self.ground.top:
                self.bird.is_dead = True

        # once the bird is dead the updating will be moved to here
        else:

            # testing if the bird has reached the ground yet (the bird will fall once it dies until it reaches the ground)
            if self.bird.center_y <= self.ground.top:
                if self.count > HIGH_SCORES[-1]:
                    HIGH_SCORES.append(self.count)
                    HIGH_SCORES.pop(0)
                gameOverView = gameOver()
                self.window.show_view(gameOverView)

                # reset default scroll speed
                SCROLL_SPEED = 2
                # HEIGHT_DIFF only used if you use the pipe height change updates (is not being used as of right now)
                HEIGHT_DIFF = 75

            # if the bird hasn't reached the ground then it will continue to update falling
            else:
                self.bird.update()

# drawing the final View (game over Screen)
class gameOver(arcade.View):
    def __init__(self):
        super().__init__()

    # drawing game over image and high score counter
    def on_draw(self):
        arcade.draw_text("High Score", SCREEN_WIDTH//2, 175, arcade.color.GOLD , font_name='Kenny Blocks Font', bold = True, font_size=30, anchor_x="center")
        arcade.draw_text(HIGH_SCORES[0], SCREEN_WIDTH//2, 125,
                         arcade.color.GOLD, font_name='Kenny Blocks Font', bold=True, font_size=35, anchor_x="center")
        arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH // 2 - 296 // 2, SCREEN_HEIGHT // 2, 296, 264, arcade.load_texture(
            "images/gameOver.png"))

        # creating a high score text file to save the players all-time high score (even across program plays)
        pathHighScore = pathlib.Path("HighScore")

        # testing if the high score text file already exists (if not creating the text file)
        if not pathlib.Path("HighScore").is_file():
            HSFileCreate = open("HighScore", "w")
            HSFileCreate.write('0')
            HSFileCreate.close()

        # reading and updating high score text file if necessary
        HSFileRead = open("HighScore", "r")
        totalHS = int(HSFileRead.read())
        HSFileRead.close()
        if HIGH_SCORES[0] > totalHS:
            HSFileWrite = open("HighScore", "w")
            HSFileWrite.write(str(HIGH_SCORES[0]))
            HSFileWrite.close()

    # resets the game after the player presses space
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            game_view = StartingScreen()
            self.window.show_view(game_view)


# main method and runs all major Views/Windows
def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Flappy Bird")
    startingView = StartingScreen()
    window.show_view(startingView)
    arcade.run()


main()
