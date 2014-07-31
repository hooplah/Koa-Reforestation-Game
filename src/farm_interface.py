import sfml as sf
import src.net as net
import src.const as const
import src.res as res

from src.input_system import MouseHandler
from src.gui import Button
from src.gui import Textbox
from src.gui import Window
from src.rect import contains

# FarmInterface draws all the buttons and the farm currently on-screen
class FarmInterface:
    def __init__(self, client, student, farm, input):
        self.client = client
        self.student = student
        self.input = input
        self.input.add_mouse_handler(self)
        self.input.add_key_handler(self)
        
        self.load_button = Button(sf.Vector2(0, 0), "button", 3, 3, input)
        self.save_button = Button(sf.Vector2(0, 32), "button", 3, 3, input)
        
        self.textbox = Textbox(sf.Vector2(300, 300), 256, input)
        
        self.window = Window(sf.Vector2(0, 0), 256, 256, sf.Color(50, 50, 120, 255), input)
        self.window.add_child(self.load_button)
        self.window.add_child(self.save_button)
        
        self.current_farm = farm # The farm we're currently drawing
        
    def mouse_over_buttons(self, x, y): # Hack so the buttons work together
        i = 0 # the amount of buttons not pressed
        button_pressed = False
        while (i < len(self.window.children)) and button_pressed == False:
            if contains(self.window.vertices.bounds, sf.Vector2(x, y)) == False:
                i+=1
            else:
                button_pressed = True
                
        return button_pressed
    
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if not self.mouse_over_buttons(x, y):
            packet = net.Packet()
            packet.write(const.packet_request_place_item)
            packet.write("tree")
            packet.write(x)
            packet.write(y)
            self.client.send(packet)
            
    def on_mouse_button_released(self, button, x, y):
        if button == sf.Mouse.LEFT:
            if contains(self.load_button.local_bounds, sf.Vector2(x, y)) and self.current_farm != self.student.farm:
                packet = net.Packet()
                packet.write(const.packet_request_load_farm)
                packet.write(self.student.client_id)
                self.client.send(packet)
            if contains(self.save_button.local_bounds, sf.Vector2(x, y)):
                # Save user information
                packet = net.Packet()
                packet.write(const.packet_save)
                self.student.serialize(packet)
                # Save farm information
                packet.write(len(self.current_farm.land_items))
                for item in self.current_farm.land_items:
                    item.serialize(packet)
                # Send file
                self.client.send(packet)
            
    def on_mouse_moved(self, position, move):
        pass
        
    # KEYBOARD
    def on_key_pressed(self, key_code):
        pass
    
    def on_key_released(self, key_code):
        pass
        
    def update(self, dt):
        self.window.update(dt)
            
    def draw(self, target):
        points = sf.Text("0", res.font_8bit, 20)
        points.position = sf.Vector2(760, 0)
        points.string = str(self.student.points)
        target.draw(points)
        
        self.window.draw(target)
        self.textbox.draw(target)
        
        for item in self.current_farm.land_items:
            item.draw(target)