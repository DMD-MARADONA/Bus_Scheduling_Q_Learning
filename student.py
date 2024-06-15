class Student:
    def __init__(self, location, waiting_time, xposition, yposition):
        self.location = location         # Bus locatio
        self.waiting_time = waiting_time    # Time the bus has been idle
        self.xposition = xposition
        self.yposition = yposition
    def count_time(self):
        self.waiting_time+1
    
    def get_waiting_time(self):
        return self.waiting_time