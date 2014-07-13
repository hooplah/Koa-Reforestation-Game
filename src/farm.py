import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.student import Student
from src.farm_interface import FarmInterface

class FarmLandItem: # something placeable on the farm (ex. trees)
    def __init__(self, path, pos, id):
        self.path = path # need path to identify when sending to server
        self.texture = sf.Texture.from_file(self.path)
        self.sprite = sf.Sprite(self.texture)
        self.sprite.position = pos
        self.position = pos
        self.id = id
        
    def draw(self, target):
        target.draw(self.sprite)

class FarmClient:
    def __init__(self, input, farm_interface, client, student):
        self.input = input
        self.farm_interface = farm_interface
        self.client = client
        self.student_owner = student # the owner of the far
        
        client.add_handler(self)
        self.input.add_mouse_handler(self.farm_interface)
        self.input.add_key_handler(self.farm_interface)
        
        self.land_items = []
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.packet_add_points:
            self.student_owner.points = packet.read()
        elif packet_id == const.packet_place_item:
            item_id = packet.read()
            pos_x = packet.read()
            pos_y = packet.read()
            item = FarmLandItem(const.items[item_id], sf.Vector2(pos_x, pos_y), item_id)
            self.land_items.append(item)
    
    def draw(self, target):
        points = sf.Text("0", res.font_8bit, 20)
        points.position = sf.Vector2(760, 0)
        points.string = str(self.student_owner.points)
        target.draw(points)
        
        for item in self.land_items:
            item.draw(target)
            
    def update(self, dt):
        self.input.handle()
            

class FarmServer:
    def __init__(self, server, teacher):
        self.server = server
        self.teacher = teacher
        
        server.add_handler(self)
        
        self.land_items = []
        
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()
        
        if packet_id == const.packet_save:
            # Read incoming packet
            save_packet = net.Packet()
            student_id = packet.read()
            points = packet.read()
            f_name = packet.read()
            l_name = packet.read()
            # Check if data is already in text file
            filename = "content/"+f_name+"_"+l_name
            file = open(filename, 'w')
            text = [f_name, " ", l_name, " ", str(points)]
            file.writelines(text)
            file.close()
            print("Saved")
        elif packet_id == const.packet_request_place_item:
            # Read incoming packet
            item_packet = net.Packet()
            item_id = packet.read()
            pos_x = packet.read()
            pos_y = packet.read()
            # Write new one to send to client to place tree
            item_packet.write(const.packet_place_item)
            item_packet.write(item_id)
            item_packet.write(pos_x)
            item_packet.write(pos_y)
            # Draw this tree 
            self.server.send(client_id, item_packet)
            item = FarmLandItem(const.items[item_id], sf.Vector2(pos_x, pos_y), item_id)
            self.land_items.append(item)
            
    def on_connect(self, client_id):
        pass
            
    def draw(self, target):
        for item in self.land_items:
            item.draw(target)
            
    def update(self, dt):
        pass
    