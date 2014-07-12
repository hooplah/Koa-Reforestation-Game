import src.net as net

class Student:
    def __init__(self, id=""):
        self.client_id = id
        self.points = 0
        self.first_name = ""
        self.last_name = ""

    def serialize(self, packet):
        packet.write(self.client_id)
        packet.write(self.points)
        packet.write(self.first_name)
        packet.write(self.last_name)

    def deserialize(self, packet):
        self.client_id = packet.read()
        self.points = packet.read()
        self.first_name = packet.read()
        self.last_name = packet.read()