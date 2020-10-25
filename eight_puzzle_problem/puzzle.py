import copy
from eight_puzzle_problem.constants import BLANK


class PuzzleParity:

    data_linear: list

    def is_solvable(self, goal_state):
        """
            If parity of GOAL == parity of current state, then puzzle is solveable.
            I am determining parity by the oddness/evenness of the inversions.
            I am determining inversion counts by comparing every title to the one after it,
            if before > after, then I add one to inversion.
        """
        # -- Remove BLANK Title -- #
        goal_state_linear = [i for i in goal_state.data_linear if i != BLANK]
        data_linear = [i for i in self.data_linear if i != BLANK]

        # -- Calculate inversions for data -- #
        data_inversions = 0
        for x in range(len(data_linear)):
            for y in range(x+1, len(data_linear)):
                if data_linear[x] > data_linear[y]:
                    data_inversions += 1

        # -- Calculate inversions for goal -- #
        goal_state_inversions = 0
        for x in range(len(goal_state_linear)):
            for y in range(x + 1, len(goal_state_linear)):
                if goal_state_linear[x] > goal_state_linear[y]:
                    goal_state_inversions += 1

        # -- If both parities are even/even or odd/odd, then puzzle is solveable    -- #
        return (data_inversions % 2 == 0) == (goal_state_inversions % 2 == 0)


class PuzzleState(PuzzleParity):

    def __init__(self):
        self.data = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.data_linear = None
        self.blank_location = None
        self.parent = None
        self.g = 0  # Level

    def __hash__(self):
        return hash(str(self.data))

    def __repr__(self):
        return str(self.data_linear)

    def __eq__(self, other):
        return self.data == other.data

    def add_to_data(self, x, y, text: int or str):
        self.data[y][x] = text
        if isinstance(text, str):
            self.blank_location = (x, y)

    def lock_data(self):
        self.__set_data_linear__()

    def __set_data_linear__(self):
        self.data_linear = list()
        for x in range(3):
            for y in range(3):
                t = self.data[x][y]
                self.data_linear.append(t)

    def generate_neighbors(self):
        """
            Find available Neighbors. The order is Clockwise.
        """
        neighbors = [
            self.is_neighbor_right(),
            self.is_neighbor_down(),
            self.is_neighbor_left(),
            self.is_neighbor_up(),
        ]

        return [n for n in neighbors if n is not None]

    def is_neighbor_up(self):
        """     Attempted to get neighbor 'up'    """
        x, y = self.blank_location
        if self.__is_direction_in_scope__(x=x, y=y-1) is not True:
            return
        neighbor = PuzzleState()
        neighbor.data = copy.deepcopy(self.data)
        neighbor.add_to_data(x, y, text=self.data[y-1][x])
        neighbor.add_to_data(x, y-1, text=self.data[y][x])
        neighbor.parent = self
        neighbor.g = self.g + 1
        neighbor.lock_data()
        return neighbor

    def is_neighbor_down(self):
        """     Attempted to get neighbor 'down'    """
        x, y = self.blank_location
        if self.__is_direction_in_scope__(x=x, y=y+1) is not True:
            return
        neighbor = PuzzleState()
        neighbor.data = copy.deepcopy(self.data)
        neighbor.add_to_data(x, y, text=self.data[y+1][x])
        neighbor.add_to_data(x, y+1, text=self.data[y][x])
        neighbor.parent = self
        neighbor.g = self.g + 1
        neighbor.lock_data()
        return neighbor

    def is_neighbor_left(self):
        """     Attempted to get neighbor 'left'    """
        x, y = self.blank_location
        if self.__is_direction_in_scope__(x=x-1, y=y) is not True:
            return
        neighbor = PuzzleState()
        neighbor.data = copy.deepcopy(self.data)
        neighbor.add_to_data(x, y, text=self.data[y][x-1])
        neighbor.add_to_data(x-1, y, text=self.data[y][x])
        neighbor.parent = self
        neighbor.g = self.g + 1
        neighbor.lock_data()
        return neighbor

    def is_neighbor_right(self):
        """     Attempted to get neighbor 'right'    """
        x, y = self.blank_location
        if self.__is_direction_in_scope__(x=x+1, y=y) is not True:
            return
        neighbor = PuzzleState()
        neighbor.data = copy.deepcopy(self.data)
        neighbor.add_to_data(x, y, text=self.data[y][x+1])
        neighbor.add_to_data(x+1, y, text=self.data[y][x])
        neighbor.parent = self
        neighbor.g = self.g + 1
        neighbor.lock_data()
        return neighbor

    @staticmethod
    def __is_direction_in_scope__(x, y):
        # -- Check if new location is in bounds of 3 x 3 -- #
        if x < 0 or x >= 3:
            return False
        elif y < 0 or y >= 3:
            return False
        return True

    def calculate_misplaced_titles(self, goal_state) -> int:
        """     Counts number of titles off from given GOAL STATE       """
        return sum(
            1
            for curr, goal in zip(self.data_linear, goal_state.data_linear)
            if curr != goal
        )

    def calculate_manhattan_distance(self, goal_state):
        """     Number of Squares to DESIRED GOAL       """
        # -- Convert BLANK into a 0 -- #
        goal_linear = [i if i != BLANK else 0 for i in goal_state.data_linear]
        data_linear = [i if i != BLANK else 0 for i in self.data_linear]

        manhattan_distance = 0
        for i in range(1, 9):
            # -- Find the index of where each number is located -- #
            d = data_linear.index(i)
            g = goal_linear.index(i)
            # -- Determine coordinates on a 3x3 matrix -- #
            x1 = d % 3
            x2 = g % 3
            y1 = int(d / 3)
            y2 = int(g / 3)
            # -- Subtract x's and y's, then add absolute value of result
            manhattan_distance += abs(x1 - x2) + abs(y1 - y2)

        return manhattan_distance


GOAL_STATE = PuzzleState()
GOAL_STATE.data = [
        [1, 2, 3],
        [8, BLANK, 4],
        [7, 6, 5],
    ]
GOAL_STATE.lock_data()
