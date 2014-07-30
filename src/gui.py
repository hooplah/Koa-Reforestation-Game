import sfml as sf
import src.res as res
from src.rect import contains
from src.input_system import MouseHandler
from src.spritesheet import SpriteSheet
        
class Button:
    def __init__(self, pos, type, frames, frames_per_row, input): # assumes it's all in one picture
        self.sprite = SpriteSheet(res.textures[type])
        self.sprite.init(frames, frames_per_row)
        self.sprite.position = pos
        
        self.rectangle = self.sprite.local_bounds
        self.rectangle.position = pos
        
        self.input = input
        input.add_mouse_handler(self)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        pass
    
    def on_mouse_button_released(self, button, x, y):
        self.sprite.set_frame(0) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.rectangle, sf.Vector2(position.x, position.y)):
            self.sprite.set_frame(1) # hover
        else:
            self.sprite.set_frame(0) # up
            
    def draw(self, target):
        target.draw(self.sprite)

class TextBox:
    def __init__(self, pos):
        pass

class Window:
    def __init__(self, pos, width, height, color):
        self.vertices = sf.VertexArray(sf.Quads, 4)
        # Set Position
        self.vertices[0].position = sf.Vector2(pos.x, pos.y)
        self.vertices[1].position = sf.Vector2(width, pos.y)
        self.vertices[2].position = sf.Vector2(width, height)
        self.vertices[3].position = sf.Vector2(pos.x, height)
        # Set Color
        for i in range(0, 4):
            self.vertices[i].color = color
