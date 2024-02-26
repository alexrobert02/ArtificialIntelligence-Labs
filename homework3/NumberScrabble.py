class NumberScrabble:
    def __init__(self, player1, player2):
        self.matrix = [
            [2, 7, 6],
            [9, 5, 1],
            [4, 3, 8]
        ]
        self.player1_symbol = player1
        self.player2_symbol = player2
        self.winner = None
        self.available_moves = set(range(1, 10))

    def is_valid_move(self, number):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == number:
                    return True
        return False

    def make_move(self, player_symbol, number):
        if number not in self.available_moves:
            return False

        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == number:
                    self.matrix[i][j] = player_symbol
                    self.available_moves.remove(number)
                    return True

        return False

    def check_winner(self, player_symbol):
        for i in range(3):
            if all(cell == player_symbol for cell in self.matrix[i]):
                return True
        for j in range(3):
            if all(self.matrix[x][j] == player_symbol for x in range(3)):
                return True
        if all(self.matrix[x][x] == player_symbol for x in range(3)) or \
                all(self.matrix[x][2 - x] == player_symbol for x in range(3)):
            return True
        return False

    def is_final(self):
        if self.winner is not None:
            return True
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != self.player1_symbol and self.matrix[i][j] != self.player2_symbol:
                    return False
        return True

    def get_available_moves(self):
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] != self.player1_symbol and self.matrix[i][j] != self.player2_symbol:
                    available_moves.append(self.matrix[i][j])
        return available_moves

    def evaluate(self):
        # Calculate the value of the current position.
        player1_value = 0
        player2_value = 0

        for i in range(3):
            if all(self.matrix[i][j] == self.player1_symbol for j in range(3)):
                player1_value += 10
            if all(self.matrix[i][j] == self.player2_symbol for j in range(3)):
                player2_value += 10
            if all(self.matrix[j][i] == self.player1_symbol for j in range(3)):
                player1_value += 10
            if all(self.matrix[j][i] == self.player2_symbol for j in range(3)):
                player2_value += 10

        # Evaluate diagonals.
        if all(self.matrix[i][i] == self.player1_symbol for i in range(3)):
            player1_value += 10
        if all(self.matrix[i][i] == self.player2_symbol for i in range(3)):
            player2_value += 10
        if all(self.matrix[i][2 - i] == self.player1_symbol for i in range(3)):
            player1_value += 10
        if all(self.matrix[i][2 - i] == self.player2_symbol for i in range(3)):
            player2_value += 10

        return player2_value - player1_value

    def find_position(self, value):
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == value:
                    return i, j
        return None

    def minimax(self, depth, is_max):
        score = self.evaluate()
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth

        if self.is_final():
            return 0

        if is_max:
            best_score = -float('inf')
            best_move = 0
            for move in self.available_moves.copy():
                self.available_moves.remove(move)
                result = self.find_position(move)
                self.matrix[result[0]][result[1]] = self.player2_symbol
                current_score = self.minimax(depth + 1, not is_max)
                self.matrix[result[0]][result[1]] = move
                self.available_moves.add(move)
                if current_score > best_score:
                    best_score = current_score
                    best_move = move
            if depth == 0:
                return best_move
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves.copy():
                self.available_moves.remove(move)
                result = self.find_position(move)
                self.matrix[result[0]][result[1]] = self.player1_symbol
                best_score = min(best_score, self.minimax(depth + 1, is_max))
                self.matrix[result[0]][result[1]] = move
                self.available_moves.add(move)
            return best_score

    def play(self):
        while not self.is_final():
            print("Current Board:")
            for row in self.matrix:
                print(row)

            # Player A's turn
            player1_move = input("Player A's turn. Enter a number between 1 and 9: ")
            if not player1_move.isdigit():
                print("Invalid input. Please enter a valid number.")
                continue
            player1_move = int(player1_move)
            if not (1 <= player1_move <= 9):
                print("Invalid input. Please choose a number between 1 and 9.")
                continue

            if not self.is_valid_move(player1_move):
                print("Invalid move. Please choose an available number.")
                continue

            self.make_move(self.player1_symbol, player1_move)
            if self.check_winner(self.player1_symbol):
                print("Player A wins!")
                break

            if self.is_final():
                print("Game over!")
                break

            # Player B's turn
            player2_move = self.minimax(0, True)
            print("Player B's turn. Player B chooses:", player2_move)
            self.make_move(self.player2_symbol, player2_move)
            if self.check_winner(self.player2_symbol):
                print("Player B wins!")
                break

        print("Game over!")
