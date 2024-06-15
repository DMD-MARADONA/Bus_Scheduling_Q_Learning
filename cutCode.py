# Training the agent
def train_agent(env, agent, episodes=1000):
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

buses = [Bus(90, "APK"), Bus(90, "DFC")]
env = World(buses, busy_level=8)
state_size = 3  # (len(students_at_APK), len(students_at_DFC), bus locations)
action_size = 2
agent = QLearningAgent(state_size, action_size)

#train_agent(env, agent)