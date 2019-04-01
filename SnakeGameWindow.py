import pyglet
from pyglet.window import key
from pyglet.gl import *
from Snake import Snake

class SnakeGameWindow(pyglet.window.Window):

    def __init__(self):
        super(SnakeGameWindow, self).__init__()
        self.thickness = 20
        self.maxX = self.width // self.thickness
        self.maxY = self.height // self.thickness
        self.game_is_over = False


        self.snake = Snake(self)
        pyglet.clock.schedule_interval(lambda dt: self.update(dt), 1/10.0)
        self.score_label = pyglet.text.Label("Score: 0",
                                font_size=18,
                                bold=True,
                                color=(0,0,0,128),
                                x=self.width, y=self.height,
                                anchor_x="right", anchor_y="top")
        self.game_over_label = pyglet.text.Label("Game over!",
                                font_size=36,
                                color=(0,0,0,255),
                                x=self.width//2, y=self.height//2,
                                anchor_x="center", anchor_y="center")
        self.restart_label = pyglet.text.Label("Press R to restart",
                                font_size=24,
                                color=(0,0,0,255),
                                x=self.width//2, y=0,
                                anchor_x="center", anchor_y="bottom")


    def on_key_press(self, symbol, modifiers):
        if symbol == key.W or symbol == key.UP:
            self.snake.change_direction(0, 1)
        elif symbol == key.A or symbol == key.LEFT:
            self.snake.change_direction(-1, 0)
        elif symbol == key.S or symbol == key.DOWN:
            self.snake.change_direction(0, -1)
        elif symbol == key.D or symbol == key.RIGHT:
            self.snake.change_direction(1, 0)
        elif self.game_is_over and symbol == key.R:
            self.snake.setup()
            self.game_is_over = False
    
    def update(self, dt):
        if not self.game_is_over:
            self.snake.update(dt)

    def game_over(self):
        self.game_is_over = True



    def on_draw(self):
        glClearColor(1, 1, 1, 1)
        self.clear()
        self.snake.draw()

        if self.game_is_over:
            self.game_over_label.draw()
            self.restart_label.draw()
        else:
            self.score_label.text = f"Score: {self.snake.size}"
            self.score_label.draw()


        

        
if __name__ == '__main__':
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()  
    window = SnakeGameWindow()
    pyglet.app.run()


  