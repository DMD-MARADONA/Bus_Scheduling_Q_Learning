import pickle

def save_q_table(q_table, filename='q_table.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(q_table, f)

def load_q_table(filename='q_table.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)