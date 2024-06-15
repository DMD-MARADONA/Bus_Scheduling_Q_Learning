import random
from bus import Bus
from world import World
from QLearningAgent import QLearningAgent
from utility import save_q_table, load_q_table
from visualize import Visualize

def train_agent(env, agent, episodes=500):
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            actions = agent.choose_action(state)
            next_state, reward, done = env.step(actions)
            agent.update_q_table(state, actions, reward, next_state)
            state = next_state
            total_reward += reward
            

        agent.decay_exploration()
        print(f"Episode {episode+1}/{episodes}, Total Reward: {total_reward}")

    save_q_table(agent.q_table)

def use_trained_agent(env, agent):
    visualizer = Visualize(env)
    visualizer.run(agent)

if __name__ == "__main__":

    #Admin Ifomation
    buses = []
    num_buses = int(input("Enter the number of buses: "))
    for i in range(num_buses):
        print(f"\nEnter details for Bus {i+1}:")
        bus_capacity = int(input("Enter Capacity: "))
        bus_location = input("Enter Location: ")
        bus = Bus(bus_capacity,bus_location)
        buses.append(bus)
    
    env = World(buses, int(input("Enter Busy level: ")))
    state_size = 3  # (len(students_at_APK), len(students_at_DFC), bus locations)
    action_size = num_buses
    agent = QLearningAgent(state_size, action_size)

    # Train the agent
    train_agent(env, agent)

    # Load the trained Q-table
    q_table = load_q_table()
    agent.q_table = q_table

    # Use the trained agent for scheduling buses with visualization
    use_trained_agent(env, agent)