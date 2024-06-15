import random
from student import Student
class World: 
    def __init__(self, buses, busy_level, max_wait_time = 45, distance_time = 30):
        self.buses = buses
        self.busy_level = busy_level
        self.max_wait_time = max_wait_time
        self.distance_time = distance_time
        self.students_at_APK = []
        self.students_at_DFC = []
        self.time_count = 0
    # Reset the world
    def reset(self):
        self.students_at_APK.clear()
        self.students_at_DFC.clear()
        self.time_count = 0
        for bus in self.buses:
            bus.update_location(random.choice(["APK", "DFC"]))
            bus.reset_drive_time()
        return self.get_state()

    def step(self, action):
        self.time_count += 1
        reward = 0

        # Generating students, waiting time represents a student, starts at zero
        random_number = random.randint(0, self.busy_level)
        for i in range(random_number):
            if random.randint(0, 1) == 0:
                self.students_at_APK.append(0)
            else:
                self.students_at_DFC.append(0)

        # Update waiting times and check for longest wait time
        longest_wait = 0
        self.students_at_APK = [t + 1 for t in self.students_at_APK]
        self.students_at_DFC = [t + 1 for t in self.students_at_DFC]
        if self.students_at_APK:
            longest_wait = max(self.students_at_APK)
        if self.students_at_DFC: #longest wait at APK vs Longest Wait in DFC
            longest_wait = max(longest_wait, max(self.students_at_DFC))

        # Negative reward for longest wait time
        if longest_wait > self.max_wait_time:
            reward -= (longest_wait - self.max_wait_time)

        # Schedule buses based on action value, reward and remove students
        for i, bus in enumerate(self.buses):
            if action[i] == 1:  # Schedule bus to DFC
                reward += -10
                if bus.location == "APK":
                    bus.update_location("APK-DFC")
                    reward += min(len(self.students_at_APK), bus.capacity)  # Reward for students goingOnbord
                    self.students_at_APK = self.students_at_APK[bus.capacity:] # Removing students upto capacity
                elif bus.location == "DFC": # Schedule bus to DFC
                    bus.update_location("DFC-APK")
                    reward += min(len(self.students_at_DFC), bus.capacity)
                    self.students_at_DFC = self.students_at_DFC[bus.capacity:]
        # Moving buses
        for bus in self.buses:
            if bus.location in ["APK-DFC", "DFC-APK"]:
                bus.bus_driving_time += 1
                if bus.bus_driving_time == self.distance_time:  # If bus has arrived, Update location
                    if bus.location == "APK-DFC":
                        bus.update_location("DFC")
                    else:
                        bus.update_location("APK")
                    bus.reset_drive_time()

        state = self.get_state()
        return state, reward, self.time_count >= 300
    # The state of the world.
    def get_state(self):
            return (
                len(self.students_at_APK),
                len(self.students_at_DFC),
                [bus.location for bus in self.buses]
            )