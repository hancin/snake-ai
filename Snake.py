import pyglet
from collections import deque
import random

class Snake:
    def __init__(self, window):
        self.thickness = window.thickness
        self.window = window
        self.setup()
    
    def setup(self):
        self.tail = deque([])
        self.x_vel = 0
        self.y_vel = 1
        self.x = 0
        self.y = 0
        self.size = 0
        self.place_food()
        

    def place_food(self):
        while True:
            self.foodX = random.randint(0, self.window.maxX-1)
            self.foodY = random.randint(0, self.window.maxY-1)

            #Only exit if food doesn't collide with Snake
            if not (self.foodX == self.x and self.foodY == self.y) and all(not (self.foodX == x and self.foodY == y) for x,y in self.tail):
                break



    def change_direction(self, x_vel, y_vel):
        #block excessive movement and prevent reversing (which would be instant death)
        if abs(x_vel) == 1 and abs(self.x_vel) != abs(x_vel):
            self.x_vel = x_vel
            self.y_vel = 0
        elif abs(y_vel) == 1 and abs(self.y_vel) != abs(y_vel):
            self.x_vel = 0
            self.y_vel = y_vel


    def coords_to_rect(self, x, y):
        #we leave a small gap between squares for visibility
        return self.rect_coords(x+1, y+1, self.thickness-1, self.thickness-1)
    
    def rect_coords(self, x, y, w, h):
        """Convert a rectangle into triangle coordinates for OpenGL."""
        return (x, y,
                w+x, y,
                w+x, h+y,
                x, h+y)

    def update(self, dt):

        self.tail.append((self.x, self.y))

        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel

        #boundary check
        if self.x < 0 or self.y < 0 or self.x == self.window.maxX or self.y == self.window.maxY:
            self.window.game_over()
            return
        
        if any(self.x == x and self.y == y for x,y in self.tail):
            self.window.game_over()
            return

        if self.foodX == self.x and self.foodY == self.y:
            self.place_food()            
            self.size += 1
        else:
            self.tail.popleft()



    def draw(self):

        pyglet.gl.glColor3f(0.5, 0.05, 0.05)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
            ('v2i', self.coords_to_rect(self.foodX * self.thickness, self.foodY * self.thickness)))
            
        batch = pyglet.graphics.Batch()


        pyglet.gl.glColor3f(0.25,1,0.25)

        #tail
        for rectX, rectY in self.tail:
            batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2, 0, 2, 3],
                ('v2i', self.coords_to_rect(rectX * self.thickness, rectY * self.thickness)))


        batch.draw()

        #head
        pyglet.gl.glColor3f(0,0.5,0)
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
            ('v2i', self.coords_to_rect(self.x * self.thickness, self.y * self.thickness)))
        
