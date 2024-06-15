from student import Student
class Bus(Student):
    def __init__(self, capacity, location): # , idle_time, xposition, yposition, bus_img, bus_rect
        self.capacity = capacity      # Maximum number of passengers the bus can carry
        self.location = location      # Bus location
        self.bus_driving_time = 0

    def update_location(self, new_location):
        self.location = new_location

    def reset_drive_time(self):
        self.bus_driving_time = 0