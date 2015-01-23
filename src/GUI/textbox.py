import sfml as sf
import src.res as res
from src.GUI.element import SpriteElement

from src.rect import contains

class Textbox(SpriteElement):
    def __init__(self, pos, width, default_text, input):
        super().__init__(pos, "textbox", 1, 1, input)
        self.sprite.scale(sf.Vector2(width/self.sprite.texture.width, 1))
        
        self.text_offset = sf.Vector2(7, 3)
        self.local_bounds = sf.Rectangle(pos, sf.Vector2(width, self.sprite.texture.height))
        
        self.typing = False
        self.overlapping = False # if the text goes out the textbox
        self.default_text = default_text
        self.last_text = default_text # the last text entered
        self.text = sf.Text(default_text, res.font_farmville, 20)
        self.text.position = self.local_bounds.position
        self.text.color = sf.Color.BLACK
        
        input.add_text_handler(self)
        
    def on_text_entered(self, unicode):
        if unicode != 8 and unicode != 13 and self.typing is True and not self.overlapping: # not backspace, text still inside box
            self.text.string += chr(unicode)
            self.last_text = self.text.string
            if self.text.string[0][0] == " " and len(self.text.string) != 1: # first letter is a space - nothing
                self.text.string = self.text.string[-1:]
                print("yolo")
        elif unicode == 8 and self.typing is True: # You press backspace
            if len(self.text.string) > 1:
                self.text.string = self.text.string[:-1] # delete last letter of string
                if self.overlapping:
                    self.overlapping = False
                self.last_text = self.text.string
            elif len(self.text.string) <= 1:
                self.text.string = " "
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if contains(self.local_bounds, sf.Vector2(x, y)):
            self.typing = True
            if self.text.string == self.default_text: # if it's the default text, get rid of it
                self.text.string = " "
        elif not contains(self.local_bounds, sf.Vector2(x, y)):
            self.typing = False
            if self.text.string == " ": # if you unclick it and there's nothing there, make it the default text
                self.text.string = self.default_text

    #
    #
    # TEXTBOX CANNOT CONTAIN NO STRING
        
    def draw(self, target):
        super().draw(target)
        target.draw(self.text)
        
    def update(self, dt):
        super().update(dt)
        
        if self.text.position != (self.local_bounds.position + self.text_offset):
            self.text.position = (self.local_bounds.position + self.text_offset)
            
        if self.text.local_bounds.width+self.text_offset.x+17 > self.local_bounds.width:
            self.overlapping = True
