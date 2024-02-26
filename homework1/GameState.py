class GameState:
    def __init__(self, vect, moves=None):
        if moves is None:
            moves = []
        if len(vect) == 9:
            self.vect = vect
            self.vect.insert(0, 9)
        else:
            print("Input vector must have a length of 9.")
        self.moves = moves

    def is_final(self):
        my_list = self.vect[1:]
        new_list = [x for x in my_list if x != 0]
        return new_list == sorted(new_list)

    def is_valid_move(self, value_of_position):
        if not self.is_final():
            if self.vect[0] != self.vect[self.index(value_of_position)] and self.is_movable(value_of_position):
                return True
        return False

    def is_movable(self, value_of_position):
        index = self.index(value_of_position)
        if index - 3 >= 0 and self.vect[index - 3] == 0:
            return True
        if index + 3 < len(self.vect) and self.vect[index + 3] == 0:
            return True
        if index - 1 >= 0 and self.vect[index - 1] == 0:
            return True
        if index + 1 < len(self.vect) and self.vect[index + 1] == 0:
            return True
        return False

    def make_move(self, value_of_position):
        if self.is_valid_move(value_of_position):
            index_zero = self.index(0)
            index_value = self.index(value_of_position)
            self.vect[index_zero], self.vect[index_value], self.vect[0] = self.vect[index_value], self.vect[index_zero], self.vect[index_value]

    def index(self, value_of_position):
        for i in range(len(self.vect)):
            if self.vect[i] == value_of_position:
                return i
        return -1

    def iddfs(self):
        original_state = self.vect.copy()
        visited_states = set()
        max_depth = 0
        while True:
            visited_states.clear()
            result = self.dfs(0, max_depth, visited_states)
            if result is not None:
                self.vect = original_state
                return result, max_depth
            max_depth += 1

    def dfs(self, depth, max_depth, visited_states):
        if depth > max_depth:
            return None
        state_hash = tuple(self.vect)
        if state_hash in visited_states:
            return None
        visited_states.add(state_hash)

        if self.is_final():
            return self

        for i in range(1, 9):
            if self.is_valid_move(i):
                self.make_move(i)
                self.moves.append(i)
                result = self.dfs(depth + 1, max_depth, visited_states)
                self.make_move(i)  # Revert the move
                self.moves.pop()
                if result is not None:
                    return result

        return None

    def manhattan_distance(self):
        distance = 0
        for i in range(1, len(self.vect)):
            if self.vect[i] != 0:
                current_row, current_col = (i - 1) // 3, (i - 1) % 3
                target_row, target_col = (self.vect[i] - 1) // 3, (self.vect[i] - 1) % 3
                distance += abs(current_row - target_row) + abs(current_col - target_col)
        return distance

    def hamming_distance(self):
        distance = 0
        for i in range(1, len(self.vect)):
            if self.vect[i] != 0 and self.vect[i] != i:
                distance += 1
        return distance

    def my_heuristic(self):
        distance = 0
        vect = self.vect[1:]
        for i in range(len(vect)):
            for j in range(i + 1, len(vect)):
                if vect[i] > vect[j] != 0 and vect[i] != 0:
                    distance += 1
        return distance

    def greedy_search(self, heuristic_function):
        priority_queue = [(self, 0)]
        visited_states = set()
        while priority_queue:
            node, depth = priority_queue.pop(0)
            if node.is_final():
                return node, depth
            next_moves = [value for value in node.vect[1:] if node.is_valid_move(value)]
            next_states = [node.generate_next_state(value) for value in next_moves if tuple(node.generate_next_state(value).vect[1:]) not in visited_states]
            next_states.sort(key=lambda x: heuristic_function(x), reverse=True)
            priority_queue.extend([(state, depth + 1) for state in next_states])
            visited_states.update([tuple(state.vect[1:]) for state in next_states])
        return None, -1

    # Add a function to generate the next state
    def generate_next_state(self, value_of_position):
        new_moves = self.moves + [value_of_position]  # Add the current move to the list of moves
        new_state = GameState(self.vect[1:], new_moves)
        new_state.make_move(value_of_position)
        return new_state
