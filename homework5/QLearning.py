import numpy as np


class QLearning:
    def __init__(self, num_rows, num_cols, start_state, goal_state, wind,
                 num_actions=4, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_actions = num_actions
        self.start_state = start_state
        self.goal_state = goal_state
        self.wind = wind
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = np.zeros((num_rows, num_cols, num_actions))
        self.visited_states = set()

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.randint(0, self.num_actions)
        else:
            action = np.argmax(self.Q[state[0], state[1], :])
        return action

    def update_table(self, state, action, reward, next_state):
        self.Q[state[0], state[1], action] += self.alpha * (
                    reward + self.gamma * np.max(self.Q[next_state[0], next_state[1], :]) -
                    self.Q[state[0], state[1], action])

    def take_action(self, state, action):
        wind_effect = self.wind[state[1]]  # Vântul pe coloana actuală
        if action == 0:
            next_state = [max(0, state[0] - 1 - wind_effect), state[1]]
        elif action == 1:
            next_state = [max(0, state[0] - wind_effect), min(state[1] + 1, self.num_cols - 1)]
        elif action == 2:
            next_state = [max(0, state[0] + 1 - wind_effect), state[1]]
        else:
            next_state = [max(0, state[0] - wind_effect), max(0, state[1] - 1)]

        next_state[0] = min(next_state[0], self.num_rows - 1)

        if tuple(next_state) in self.visited_states:  # Verificare pentru ciclu
            reward = -2  # Penalizare pentru ciclu
        else:
            self.visited_states.add(tuple(next_state))  # Adăugăm starea curentă în stările vizitate
            # Calcularea recompensei
            distance_to_goal = abs(next_state[0] - self.goal_state[0]) + abs(next_state[1] - self.goal_state[1])
            prev_distance_to_goal = abs(state[0] - self.goal_state[0]) + abs(state[1] - self.goal_state[1])
            distance_to_goal += wind_effect

            if distance_to_goal < prev_distance_to_goal:
                reward = 2
            else:
                reward = -1 * (distance_to_goal - prev_distance_to_goal)

        return next_state, reward

    def learning(self, num_episodes, max_steps):
        for episode in range(num_episodes):
            state = self.start_state
            for step in range(max_steps):
                action = self.choose_action(state)
                next_state, reward = self.take_action(state, action)
                self.update_table(state, action, reward, next_state)
                state = next_state
                if tuple(state) == tuple(self.goal_state):
                    break
        return self.Q

    def get_path(self):
        state = list(self.start_state)
        path = [state]
        for step in range(self.num_rows * self.num_cols):
            action = np.argmax(self.Q[state[0], state[1], :])
            next_state, _ = self.take_action(state, action)
            state = next_state
            path.append(state)
            if tuple(state) == tuple(self.goal_state):
                break
        return path

    def get_policy(self):
        policy = np.zeros((self.num_rows, self.num_cols))
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                policy[row, col] = np.argmax(self.Q[row, col, :])
        return policy
