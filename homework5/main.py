from QLearning import QLearning


def main():
    num_rows = 7
    num_cols = 10
    start_state = [3, 0]
    goal_state = [3, 7]
    num_episodes = 5000
    max_steps = 100
    wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

    q_learning = QLearning(num_rows, num_cols, start_state, goal_state, wind)
    q = q_learning.learning(num_episodes, max_steps)
    path = q_learning.get_path()
    policy = q_learning.get_policy()
    print('Q:\n', q)
    print('path:\n', path)
    print('policy:\n', policy)


if __name__ == '__main__':
    main()
