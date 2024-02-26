# Game theory

### Homework
Implement a program capable of playing "[Number Scrabble](https://en.wikipedia.org/wiki/Number_Scrabble)". Two players alternately choose a number between 1 and 9 without repeating a number previously chosen by either player. The player who has chosen from the beginning of the game three numbers that add up to a total of 15 wins. If no more numbers can be chosen and no player has won, the game ends in a draw. 

Example: A:3 B:9 A:5 B:7 A:2 B:8 A:4 B:1 A:6 A wins (6+5+4)

**Requirements**:
1. Represent a state, initializing it, checking the final state.
2. Implement the transition and its validation.
3. Implement a heuristic.
4. Implement the MinMax strategy for player B anticipating at least two opponent moves.

**Useful resources**:
* https://realpython.com/tic-tac-toe-ai-python/
