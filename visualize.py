import pygame
import random
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUS_SIZE = (50, 20)
STUDENT_SIZE = (3, 3)
APK_POS = (100, 200)
DFC_POS = (700, 200)
CIRCLE_RADIUS = 40
FONT_SIZE = 20

class Visualize:
    def __init__(self, env):
        self.env = env
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bus Scheduling Visualization")
        self.clock = pygame.time.Clock()

        # Load images
        self.apk_bus_image = pygame.image.load("apkbusssss.jpg")
        self.dfc_bus_image = pygame.image.load("dfcbuss.jpg")
        # Resize images to fit BUS_SIZE
        self.apk_bus_image = pygame.transform.scale(self.apk_bus_image, BUS_SIZE)
        self.dfc_bus_image = pygame.transform.scale(self.dfc_bus_image, BUS_SIZE)

        # Initialize font
        self.font = pygame.font.Font(None, FONT_SIZE)

    def draw_bus(self, bus, position, index):
        # Offset each bus slightly
        offset = index * (BUS_SIZE[1] + 5)
        adjusted_position = (position[0], position[1] + offset)
        if bus.location in ["APK", "APK-DFC"]:
            bus_image = self.apk_bus_image
        else:
            bus_image = self.dfc_bus_image
        self.screen.blit(bus_image, adjusted_position)

    def draw_student(self, position):
        pygame.draw.rect(self.screen, (0, 255, 0), (*position, *STUDENT_SIZE))

    def draw_environment(self):
        self.screen.fill((255, 255, 255))
        apk_students = len(self.env.students_at_APK)
        dfc_students = len(self.env.students_at_DFC)

        # Draw bus stops
        pygame.draw.circle(self.screen, (228, 119, 10), APK_POS, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, (228, 119, 10), DFC_POS, CIRCLE_RADIUS)

        # Bus stop names
        apk_text = self.font.render("APK", True, (0, 0, 0))
        dfc_text = self.font.render("DFC", True, (0, 0, 0))
        self.screen.blit(apk_text, (APK_POS[0] - apk_text.get_width() // 2, APK_POS[1] - apk_text.get_height() // 2))
        self.screen.blit(dfc_text, (DFC_POS[0] - dfc_text.get_width() // 2, DFC_POS[1] - dfc_text.get_height() // 2))

        # Draw students at APK
        for i in range(apk_students):
            self.draw_student((APK_POS[0], APK_POS[1] + CIRCLE_RADIUS + 5 + i * (STUDENT_SIZE[1] + 5)))

        # Draw students at DFC
        for i in range(dfc_students):
            self.draw_student((DFC_POS[0], DFC_POS[1] + CIRCLE_RADIUS + 5 + i * (STUDENT_SIZE[1] + 5)))

        # Draw buses
        apk_bus_index = 0
        dfc_bus_index = 0
        for bus in self.env.buses:
            if bus.location == "APK":
                self.draw_bus(bus, APK_POS, apk_bus_index)
                apk_bus_index += 1
            elif bus.location == "DFC":
                self.draw_bus(bus, DFC_POS, dfc_bus_index)
                dfc_bus_index += 1
            elif bus.location == "APK-DFC":
                mid_position = (((APK_POS[0] + DFC_POS[0]) // 30) * bus.bus_driving_time, APK_POS[1])
                self.draw_bus(bus, mid_position, 0)
            elif bus.location == "DFC-APK":
                mid_position = (((APK_POS[0] + DFC_POS[0]) // 30)* (30 - bus.bus_driving_time), DFC_POS[1])
                self.draw_bus(bus, mid_position, 0)

    def run(self, agent):
        running = True
        state = self.env.reset()
        total_reward = 0
        done = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            actions = agent.choose_action(state)
            next_state, reward, done = self.env.step(actions)
            state = next_state
            total_reward += reward
            print(f"Actions: {actions}, State: {state}, Reward: {reward}")

            self.draw_environment()
            pygame.display.flip()
            self.clock.tick(60)
            time.sleep(1)

        pygame.quit()
        print(f"Total Reward: {total_reward}")
