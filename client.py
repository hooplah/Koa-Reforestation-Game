import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.users import Student
from src.users import Teacher
from src.farm import FarmClient
from src.farm_interface import FarmInterface
from src.input_system import InputSystem

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Koa Reforestation Client")
window.key_repeat_enabled = False

input_sys = InputSystem(window)

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Connect to server
    client = net.Client("localhost", 30000)
    
    first_name = "Lucas"
    last_name = "DeRego"
    
    # Send the server my info
    logged_in = False
    login_packet = net.Packet()
    login_packet.write(const.packet_login)
    login_packet.write(first_name)
    login_packet.write(last_name)
    client.send(login_packet)
    client.update()
    
    # Wait for confirm packet from server
    while not logged_in:
        packets = client.update()
        for packet in packets:
            packet_id = packet.read()
            if packet_id == const.packet_confirm_login:
                user_type = packet.read()
                if user_type == "Student":
                    student = Student(client.client_id)
                    student.deserialize(packet)
                    farm_interface = FarmInterface(client, student, input_sys)
                    farm = FarmClient(input_sys, farm_interface, client, student)
                    student.farm = farm
                    # Load farm if student
                    farm_packet = net.Packet()
                    #type_of_packet = farm_packet.read()
                    num_of_trees = farm_packet.read()
                    for tree in num_of_trees:
                        type = farm_packet.read()
                        x = farm_packet.read()
                        y = farm_packet.read()
                        item = FarmLandItem(type, sf.Vector2(x, y))
                        student.farm.land_items.append(item)
                elif user_type == "Teacher":
                    teacher = Teacher(client.client_id)
                    teacher.deserialize(packet)
                    farm_interface = FarmInterface(client, teacher, input_sys)
                    farm = FarmClient(input_sys, farm_interface, client, teacher)
                    teacher.farm = farm
                logged_in = True
            elif packet_id == const.packet_deny_login:
                print(packet.read())
                exit(1)

except IOError:
    exit(1)

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

# start the game loop
while window.is_open:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        frame_rate.string = str(frame_accum)
        dt_accum = 0
        frame_accum = 0

    # Update connection
    client.update()
    
    farm.update(dt)
    
    # DRAW
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate)
    farm.draw(window)
    window.display() # update the window
