from ssl import OP_ENABLE_MIDDLEBOX_COMPAT
import pyglet
import random

TITLE_SIZE = 60

class GameState:
    def initialize(self):
        self.snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
        self.snake_direction = 1, 0
        self.width = 10
        self.height = 10
        self.food = [] # Adding a place for food
        self.add_food() # Random food on one position
        self.add_food() # Random food on other position
        self.alive = True 
            
    def draw(self): 
      def direction(a, b):

          if b == 'end':
              return 'end'
      
          # Coordinates according x and y values
          x_a, y_a = a
          x_b, y_b = b
      
          if x_a == x_b + 1:
              return 'left'
          elif x_a == x_b - 1:
              return 'right'
          elif y_a == y_b + 1:
              return 'bottom'
          elif y_a == y_b - 1:
              return 'top'
          else:
              return 'end'    
                  
      for coords, prev, next in zip(self.snake, ['end'] + self.snake[:-1], self.snake[1:] + ['end']): 
        x = coords[0]
        y = coords[1]
        before = direction(coords, prev)  # Shift in the direction from the previous shelf to the current one
        after = direction(coords, next)   # Shift in the direction from the actual shelf to the future one

        key = before + '-' + after            
        # This cycle lists the individual positions of the snake according to the tuple
        snake_tiles[key].blit(x * TITLE_SIZE, y * TITLE_SIZE, width = TITLE_SIZE, height = TITLE_SIZE) 
    
    
      for x, y in self.food:
        apple_image.blit(x * TITLE_SIZE, y * TITLE_SIZE, width = TITLE_SIZE, height = TITLE_SIZE)
    
    def move(self):
        if not self.alive:
            return

        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        # Checking if the snake has climbed out of the playing area (i.e. the x coordinate is less than 0 and then also a variable for height and width)
        if new_x < 0:
            self.alive = False # When it climbs, it dieds and the game stops
            self.alive = False
        if new_x >= self.width:
            self.alive = False
        if new_y >= self.height:
            self.alive = False

        new_head = new_x, new_y
        if new_head in self.snake:
            self.alive = False
        self.snake.append(new_head)

        # Eating food by a snake ( = removal of food when the head touches it)
        if new_head in self.food:
            self.food.remove(new_head)
            self.add_food()
        else:
            del self.snake [0]

    def add_food(self):
        for try_number in range(100): # Will try to add food up to 100 times
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if (position not in self.snake) and (position not in self.food): # Adds food only if coordinates are not selected in the snake or where the food is already placed
                self.food.append(position)
                return
       
# Inserting specific images for the game - green cubes in the beginning and apples - food
green_image = pyglet.image.load("green.png")
apple_image = pyglet.image.load ("apple.png")

# Dictionary and cycle for loading individual pieces of snake from directory snake-tiles
snake_tiles = {}
for start in ["bottom", "end", "left", "right", "top"]:
    for end in ["bottom", "end", "left", "right", "top", "dead", "tongue"]:
        key = start + "-" + end
        image = pyglet.image.load("snake-tiles/" + key + ".png")
        snake_tiles[key] = image

window = pyglet.window.Window()

# Creating a specific object
state = GameState()
state.initialize()
state.width = window.width // TITLE_SIZE
state.height = window.height // TITLE_SIZE

@window.event # Drawing of the snake
def on_draw():
    window.clear()
    
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    state.draw()

@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        state.snake_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        state.snake_direction = 1, 0
    if key_code == pyglet.window.key.UP:
        state.snake_direction = 0, 1
    if key_code == pyglet.window.key.DOWN:
        state.snake_direction = 0, -1

def move(dt):
    state.move()
    
pyglet.clock.schedule_interval(move, 1/3)
pyglet.app.run()