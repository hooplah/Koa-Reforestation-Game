import sfml as sf
import src.res as res
from src.rect import contains
from src.input_system import MouseHandler
from src.spritesheet import SpriteSheet

keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class Element:
    def __init__(self, pos, type, frames, frames_per_row, input):
        self.position = pos
        self.sprite = SpriteSheet(res.textures[type])
        self.sprite.init(frames, frames_per_row)
        self.sprite.position = pos
        
        self.local_bounds = self.sprite.local_bounds
        
        self.position_dirty = True
        
        input.add_key_handler(self)
        input.add_mouse_handler(self)
        
    def on_key_pressed(self, key_code):
        pass
    
    def on_key_released(self, key_code):
        pass
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        pass
    
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        pass
            
    def draw(self, target):
        target.draw(self.sprite)
        
    def update(self, dt):
        pass

class Button(Element):
    def __init__(self, pos, type, frames, frames_per_row, input): # assumes it's all in one picture
        super().__init__(pos, type, frames, frames_per_row, input)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        self.sprite.set_frame(2) # down
    
    def on_mouse_button_released(self, button, x, y):
        self.sprite.set_frame(0) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.local_bounds, sf.Vector2(position.x, position.y)):
            self.sprite.set_frame(1) # hover
        else:
            self.sprite.set_frame(0) # up

class Textbox(Element):
    def __init__(self, pos, width, input):
        super().__init__(pos, "textbox", 1, 1, input)
        self.sprite.scale(sf.Vector2(width/self.sprite.texture.width, 1))
        
        self.local_bounds = self.sprite.local_bounds
        
        self.typing = False
        self.text = sf.Text("l", res.font_farmville, 20)
        
        input.add_text_handler(self)
        
    def on_text_entered(self, unicode):
        if unicode != 8:
            self.text += unicode;
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if contains(self.local_bounds, sf.Vector2(x, y)):
            self.typing = True
    
    def on_mouse_button_released(self, button, x, y):
        self.typing = True
        
    def on_mouse_moved(self, position, move):
        pass
        
    def draw(self, target):
        super().draw(target)
        target.draw(self.text)
        
    def update(self, dt):
        pass

class Window():
    def __init__(self, pos, width, height, color, input):
        self.vertices = sf.VertexArray(sf.PrimitiveType.QUADS, 4)
        self.width = width
        self.height = height
        # Set Position
        self.vertices[0].position = sf.Vector2(pos.x, pos.y)
        self.vertices[1].position = sf.Vector2(pos.x+self.width, pos.y)
        self.vertices[2].position = sf.Vector2(pos.x+self.width, pos.x+self.height)
        self.vertices[3].position = sf.Vector2(pos.x, pos.x+self.height)
        # Set Color
        for i in range(0, 4):
            self.vertices[i].color = color
        
        self.children = []
        self.mouse_state = 'up'
        self.recalculate_position()
        
        self.input = input
        input.add_mouse_handler(self)
        
    def make_position_dirty(self):
        self.position_dirty = True
        for child in self.children:
            child.position_dirty = True
            
        self.recalculate_position()
        
    def recalculate_position(self):
        for child in self.children:
            child.sprite.position = self.vertices[0].position + child.position
            child.local_bounds.position = child.sprite.position
            child.position_dirty = False
        self.position_dirty = False
        
    def remove_child(self, element):
        self.children.remove(element)
    
    def add_child(self, element):
        self.children.append(element)
        
    def move(self, x, y):
        self.vertices[0].position += sf.Vector2(x, y)
        self.vertices[1].position += sf.Vector2(x, y)
        self.vertices[2].position += sf.Vector2(x, y)
        self.vertices[3].position += sf.Vector2(x, y)
        self.make_position_dirty();
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        self.mouse_state = 'down'
    
    def on_mouse_button_released(self, button, x, y):
        self.mouse_state = 'up'
    
    def on_mouse_moved(self, position, move):
        if contains(self.vertices.bounds, sf.Vector2(position.x, position.y)):
            if self.mouse_state == 'down': # mouse is down
                self.move(move.x, move.y)
          
    def draw(self, target):
        target.draw(self.vertices)
        
        for child in self.children:
            child.draw(target)
            
    def update(self, dt):
        for child in self.children:
            child.update(dt)
        