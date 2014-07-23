import src.net as net
import src.const as const

class Student:
    def __init__(self, id="", farm=None):
        self.client_id = id
        self.points = 0
        self.first_name = ""
        self.last_name = ""
        self.farm = farm

    def serialize(self, packet):
        packet.write("Student")
        packet.write(self.client_id)
        packet.write(self.points)
        packet.write(self.first_name)
        packet.write(self.last_name)

    def deserialize(self, packet):
        student = packet.read()
        self.client_id = packet.read()
        self.points = packet.read()
        self.first_name = packet.read()
        self.last_name = packet.read()
        

class Teacher:
    def __init__(self, id, server=None, farm=None):
        self.client_id = id
        self.first_name = ""
        self.last_name = ""
        self.points = 0 # So Teacher is same as Student
        self.server = server
        self.farm = farm
        
    def serialize(self, packet):
        packet.write("Teacher")
        packet.write(self.client_id)
        packet.write(self.first_name)
        packet.write(self.last_name)
        packet.write(self.server)

    def deserialize(self, packet):
        teacher = packet.read()
        self.client_id = packet.read()
        self.first_name = packet.read()
        self.last_name = packet.read()
        self.server = packet.read()
        
    def set_student_points(self, student, points):
        packet = net.Packet()
        packet.write(const.packet_add_points)
        packet.write(points)
        self.server.send(student.client_id, packet)
        
    def add_to_student_points(self, student, points):
        packet = net.Packet()
        packet.write(const.packet_add_points)
        packet.write(points)
        self.server.send(student.client_id, packet)