import sfml as sf
import src.net as net
import src.res as res

from src.users import Student
from src.users import Teacher
from src.farm import FarmServer

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Koa Reforestation Server")
window.key_repeat_enabled = False

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Create the server connection
    server = net.Server(30000)
          
    teacher = Teacher(server)
    farm = FarmServer(server, teacher)
        
except IOError:
    exit(1)

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

while True:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        frame_rate.string = str(frame_accum)
        dt_accum = 0
        frame_accum = 0

    # Update the server
    server.update()

    ## Draw
    
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate) # draw framerate
    farm.draw(window)
    window.display() # update the window
