import random
import numpy as np
from bus import Bus
from world import World

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}
    # Convert state into string key
    def get_state_key(self, state):
        return str(state)
    # Selects an action to take given state using epsilon-greedy strategy
    def choose_action(self, state):
        state_key = self.get_state_key(state)
        if random.uniform(0, 1) < self.exploration_rate:
            return [random.choice([0, 1]) for _ in range(len(state[2]))]
        else:
            return self.decode_action(self.get_best_action(state_key), len(state[2]))

    def encode_action(self, actions):
        return sum([a * (2 ** i) for i, a in enumerate(actions)])

    def decode_action(self, encoded_action, num_buses):
        return [(encoded_action >> i) & 1 for i in range(num_buses)]

    def get_best_action(self, state_key):
        if state_key not in self.q_table:
            self.q_table[state_key] = [0] * (2 ** self.action_size)
        return np.argmax(self.q_table[state_key])
    # Update the Q-values in the Q-table
    def update_q_table(self, state, actions, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        action_index = self.encode_action(actions)

        if state_key not in self.q_table:
            self.q_table[state_key] = [0] * (2 ** self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = [0] * (2 ** self.action_size)

        best_next_action = np.argmax(self.q_table[next_state_key])
        td_target = reward + self.discount_factor * self.q_table[next_state_key][best_next_action]
        td_error = td_target - self.q_table[state_key][action_index]
        self.q_table[state_key][action_index] += self.learning_rate * td_error

    def decay_exploration(self):
        self.exploration_rate *= self.exploration_decay