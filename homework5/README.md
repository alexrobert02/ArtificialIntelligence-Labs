# Reinforcement Learning

### Homework
Consider an agent that can move in an environment (a 7x10 grid). The agent can move up, down, left or right. The starting point of the agent, respectively its destination, are shown in the figure below: S start (cell (3,0)), respectively G goal (cell (3,7)). There is a wind that can modify the resultant next state for a desired action. In the middle region, the agent is moved up by the wind. The wind strength is plotted below each column and represents the number of cells by which the position is changed. For example, if the agent is in cell (3,8) and the action is left, then the next state of the agent will be (4,7). The reward is -1 for all transitions. An episode ends when the agent reaches the goal. Implement the Q-learning algorithm to identify the path the agent should take.

**Requirements**:
1. Initialization of the Q table, the algorithm parameters and the initial state.
2. For a state s, identify the next state s' by applying an action a.
3. The Q-learning algorithm
    * selects the action with the highest Q value in state s'
    * update the Q values
    * update the current state
    * repeat
4. Show the policy determined by the algorithm.
