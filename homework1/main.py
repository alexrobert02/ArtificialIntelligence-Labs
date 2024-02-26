import time
from GameState import GameState


def main():
    initial_state = GameState([2, 7, 5, 0, 8, 4, 3, 1, 6])

    # IDDFS
    start_time = time.time()
    solution, max_depth = initial_state.iddfs()
    end_time = time.time()
    print("IDDFS:")
    print_solution_info(solution, max_depth, start_time, end_time)
    print()

    # Greedy with Manhattan Distance Heuristic
    start_time = time.time()
    solution, max_depth = initial_state.greedy_search(GameState.manhattan_distance)
    end_time = time.time()
    print("Greedy with Manhattan Distance Heuristic:")
    print_solution_info(solution, max_depth, start_time, end_time)
    print()

    # Greedy with Hamming Distance Heuristic
    start_time = time.time()
    solution, max_depth = initial_state.greedy_search(GameState.hamming_distance)
    end_time = time.time()
    print("Greedy with Hamming Distance Heuristic:")
    print_solution_info(solution, max_depth, start_time, end_time)
    print()

    # Greedy with Custom Heuristic
    start_time = time.time()
    solution, max_depth = initial_state.greedy_search(GameState.my_heuristic)
    end_time = time.time()
    print("Greedy with Custom Heuristic:")
    print_solution_info(solution, max_depth, start_time, end_time)


def print_solution_info(solution, max_depth, start_time, end_time):
    if solution is not None:
        print("Solution found:")
        print(solution.vect[1:])
        print("Moves:", solution.moves)  # Print the moves leading to the solution
        print("Max depth:", max_depth)
        time_taken = end_time - start_time
        print(f"Time taken to find the solution: {time_taken} seconds")
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()
