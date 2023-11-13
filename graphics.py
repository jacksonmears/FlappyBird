import arcade

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5
GRAVITY = 1

GAME_RUNNING = 1
GAME_OVER = 2



class IntroView(arcade.View):

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture('BackGround.png')


    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Press Spacebar ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("to jump ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Press Space to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def on_key_release(self, symbol, modifier):
            if symbol == arcade.key.SPACE:
                game_view = Game()
                game_view.setup()
                self.window.show_view(game_view)

class Bird(arcade.Sprite):

    def __init__(self, image, scale):
        super().__init__(image, scale)


    def update(self):
        self.center_y += self.change_y
        super(Bird, self).update()
        self.change_y -= 0.25

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.all_sprites_list = []
        self.bird = None
        self.frame_count = 0
        self.current_state = GAME_RUNNING

    def setup(self):
        self.background = arcade.load_texture('BackGround.png')
        self.all_sprites_list = arcade.SpriteList()
        self.current_state = GAME_RUNNING
        self.bird = Bird('top_pipe.png', 0.1)
        self.bird.center_x = 100
        self.bird.center_y = SCREEN_HEIGHT // 2
        self.bird.angle = 0
        self.bird.change_y = -1
        self.all_sprites_list.append(self.bird)

    def on_draw(self):
        arcade.start_render()
        self.draw_game()

    def draw_game(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.bird.draw()

    def update(self, delta_time):
        self.frame_count += 1
        self.bird.update()
# class EndView(arcade.View):


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Tic Tac Toe")
    intro_view = IntroView()
    window.show_view(intro_view)
    arcade.run()


main()
