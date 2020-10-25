# -- Python Libraries -- #
import time
import random
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# -- Project Library (AZ) -- #
from eight_puzzle_problem.constants import BLANK
from eight_puzzle_problem.puzzle import PuzzleState, GOAL_STATE
from eight_puzzle_problem.priority_queue import PriorityQueue


class EightPuzzleProblemGUI(tk.Canvas):
    # -- Instantiate tkinter object -- #
    window = tk.Tk()

    # -- Title -- #
    TITLE = '8 Puzzle Problem'

    # -- Size of Puzzle -- #
    COLUMNS = 3
    ROWS = 3

    # -- Constants related to PUZZLE CANVAS -- #
    TILE_WIDTH = 120
    TILE_HEIGHT = 120
    TILE_BORDER = 3
    HEIGHT = TILE_HEIGHT * COLUMNS
    WIDTH = TILE_WIDTH * ROWS
    FONT_TYPE = 'Purisa'
    FONT_SIZE = 18
    TITLE_BACKGROUND = 'SkyBlue1'
    titles_lookup = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    # -- Current Random Puzzle -- #
    initial_puzzle = None

    # -- Output Constants -- #
    brfs_scrolled_txt = None
    befs_scrolled_txt = None
    ucs_scrolled_txt = None
    a_star_scrolled_txt = None

    def __init__(self):
        # -- Add Title -- #
        self.window.title(self.TITLE)

        # Initializes Puzzle RESET/NEW options
        self.init_options_frame()

        # Initializes Algorithm Options
        self.init_informed_algorirhtms_frame()
        self.init_uninformed_algorirhtms_frame()

        # Initializes Frame that manages the Puzzle Canvas
        self.init_puzzle_frame()

        # Initializes the output frame that handles output
        # self.init_output_frame()

        # Initialize Background Puzzle Titles and random puzzle
        self.init_background()
        self.init_random_puzzle()

        self.init_brfs_output_frame()
        self.init_befs_output_frame()
        self.init_ucs_output_frame()
        self.init_a_star_output_frame()

        # -- Start Window -- #
        self.window.mainloop()

    def init_options_frame(self):
        """     These are configuration options for the PUZZLE      """
        options_frame_label = tk.LabelFrame(self.window, text="Options")
        options_frame_label.pack(side='top', anchor=tk.W, expand="yes")
        options_frame = tk.Frame(options_frame_label, width=200, height=400)
        options_frame.pack(fill='both', padx=10, pady=5, expand=True)

        new_btn = tk.Button(options_frame, text="New Puzzle", command=self.new_puzzle, bg="cornsilk3")
        new_btn.pack(side='left')

        reset_btn = tk.Button(options_frame, text="Reset Puzzle", command=self.reset_puzzle, bg="cornsilk3")
        reset_btn.pack(side='left')

    def init_informed_algorirhtms_frame(self):
        # Create left and right frames
        algo_frame_label = tk.LabelFrame(self.window, text="Informed Algorithm(s)")
        algo_frame_label.pack(side='top', anchor=tk.W, expand="yes")
        algo_frame = tk.Frame(algo_frame_label, width=200, height=400)
        algo_frame.pack(padx=10, pady=5, expand=True)

        # -- Algorithm(s) Buttons -- #
        ucs_search_btn = tk.Button(algo_frame, text="Uniform-Cost Search", command=self.ucs_search, bg="cornsilk3")
        ucs_search_btn.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X, expand='yes')
        bfs_search_btn = tk.Button(algo_frame, text="Best-First Search", command=self.befs_search, bg="cornsilk3")
        bfs_search_btn.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X, expand='yes')
        a_star_search_btn = tk.Button(algo_frame, text="A* Search", command=self.a_star_search, bg="cornsilk3")
        a_star_search_btn.pack(side=tk.BOTTOM, anchor=tk.E, fill=tk.X, expand='yes')

    def init_uninformed_algorirhtms_frame(self):
        # Create left and right frames
        algo_frame_label = tk.LabelFrame(self.window, text="Uninformed Algorithm(s)")
        algo_frame_label.pack(side='top', anchor=tk.W, expand="yes")
        algo_frame = tk.Frame(algo_frame_label, width=200, height=400)
        algo_frame.pack(padx=10, pady=5, expand=True)

        # -- Algorithm(s) Buttons -- #
        bfs_search_btn = tk.Button(algo_frame, text="Breadth First Search", command=self.brfs_search, bg="cornsilk3")
        bfs_search_btn.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X, expand='yes')

    def init_puzzle_frame(self):
        puzzle_frame_label = tk.LabelFrame(self.window, text="Puzzle")
        puzzle_frame_label.pack(side='left', fill="both", expand="yes")
        puzzle_frame = tk.Frame(puzzle_frame_label, width=200, height=400)
        puzzle_frame.pack(side='left', fill='both', padx=10, pady=5, expand=True)

        # -- Create 8 Puzzle Problem Canvas [RANDOM] -- #
        tk.Canvas.__init__(self, puzzle_frame, bg="white", height=self.HEIGHT, width=self.WIDTH)
        self.pack()

    def init_brfs_output_frame(self):
        # Create left and right frames
        output_frame_label = tk.LabelFrame(self.window, text="Breadth First Search Output")
        output_frame_label.pack(side='right', fill="both", expand="yes")
        output_frame = tk.Frame(output_frame_label)
        output_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        self.brfs_scrolled_txt = tk.scrolledtext.ScrolledText(output_frame, width=30, height=30)
        self.brfs_scrolled_txt.pack(side='right')

    def init_befs_output_frame(self):
        # Create left and right frames
        output_frame_label = tk.LabelFrame(self.window, text="Best First Search Output")
        output_frame_label.pack(side='right', fill="both", expand="yes")
        output_frame = tk.Frame(output_frame_label)
        output_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        self.befs_scrolled_txt = ScrolledText(output_frame, width=30, height=30)
        self.befs_scrolled_txt.pack(side='right')

    def init_ucs_output_frame(self):
        # Create left and right frames
        output_frame_label = tk.LabelFrame(self.window, text="UCS Output")
        output_frame_label.pack(side='right', fill="both", expand="yes")
        output_frame = tk.Frame(output_frame_label)
        output_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        self.ucs_scrolled_txt = ScrolledText(output_frame, width=30, height=30)
        self.ucs_scrolled_txt.pack(side='right')

    def init_a_star_output_frame(self):
        # Create left and right frames
        output_frame_label = tk.LabelFrame(self.window, text="A* Output")
        output_frame_label.pack(side='right', fill="both", expand="yes")
        output_frame = tk.Frame(output_frame_label)
        output_frame.pack(side='top', fill='both', padx=10, pady=5, expand=True)
        self.a_star_scrolled_txt = ScrolledText(output_frame, width=30, height=30)
        self.a_star_scrolled_txt.pack(side='right')

    def init_background(self):
        """     Initializes the Puzzle's Background Title(s)        """
        for x in range(0, self.ROWS):
            for y in range(0, self.COLUMNS):
                x1, y1, x2, y2 = self.__find_coordinates__(x, y)
                # -- Create Puzzle Squares -- #
                self.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.TITLE_BACKGROUND
                )
                # -- Add Number to Title -- #
                tk_id_text = self.create_text(
                    x1 + int(0.5 * self.TILE_WIDTH),
                    y1 + int(0.5 * self.TILE_HEIGHT),
                    font=(self.FONT_TYPE, self.FONT_SIZE),
                    text=f''
                )
                # -- Set TKID for this TEXT -- #
                self.titles_lookup[y][x] = tk_id_text

    def init_random_puzzle(self):
        """     Create a random puzzle and ensure its solveable     """
        self.initial_puzzle = None
        while True:
            options = [1, 2, 3, 4, 5, 6, 7, 8, BLANK]
            random.shuffle(options)
            self.initial_puzzle = PuzzleState()
            for x in range(0, self.ROWS):
                for y in range(0, self.COLUMNS):
                    self.initial_puzzle.add_to_data(x, y, text=options.pop(0))
            self.initial_puzzle.lock_data()
            if self.initial_puzzle.is_solvable(GOAL_STATE) is True:
                break
        self.populate_puzzle_titles(self.initial_puzzle)

    def reset_puzzle(self):
        """
            Reset Puzzle back to Original State
            Useful when wanting to run multiple algorithms on the same puzzle.
        """
        self.populate_puzzle_titles(self.initial_puzzle)

    def new_puzzle(self):
        self.init_random_puzzle()
        self.brfs_scrolled_txt.delete('1.0', tk.END)
        self.befs_scrolled_txt.delete('1.0', tk.END)
        self.ucs_scrolled_txt.delete('1.0', tk.END)
        self.a_star_scrolled_txt.delete('1.0', tk.END)

    def populate_puzzle_titles(self, puzzle):
        for x in range(0, self.ROWS):
            for y in range(0, self.COLUMNS):
                self.itemconfig(
                    self.titles_lookup[y][x],
                    text=puzzle.data[y][x]
                )

    def ucs_search(self):

        """
            Assignment Requirement.

            Summary:
                Uniform-Cost Search (UCS) implementation to solve puzzle

            Notes:
                Expands nodes out in clockwise in a cycle 'right', 'down', 'left', 'up'.
                g() = Distance from root (ie first puzzle state)
        """

        # -- Setup Timer -- #
        start = self.get_time_epoch()

        # -- OUTPUT to console -- #
        self.ucs_scrolled_txt.delete('1.0', tk.END)
        self.ucs_scrolled_txt.insert(tk.INSERT, 'Running ...\n')
        self.__waiting__()

        # -------------------- #
        # -- CORE Algorithm -- #
        # -------------------- #

        seen = set()
        queue = PriorityQueue()
        queue.add(priority=0, puzzle_state=self.initial_puzzle)
        solution_state = None
        while queue.is_empty() is False:
            # -- Get next item in queue -- #
            node = queue.pop()
            current_state = node.puzzle_state
            # -- Check for Gaol -- #
            if current_state == GOAL_STATE:
                solution_state = current_state
                break
            # -- Expand State -- #
            neighbors = current_state.generate_neighbors()
            for neighbor in neighbors:
                # -- Check if not already seen -- #
                if neighbor not in seen:
                    seen.add(neighbor)
                    # -- Priority is based g(). Upon tie, clockwise -- #
                    # -- order listed in header is deciding factor  -- #
                    priority = neighbor.g
                    queue.add(priority=priority, puzzle_state=neighbor)

        # --------------------------- #
        # -- Goal State Discovered -- #
        # --------------------------- #

        # -- Close Timer-- #
        end = self.get_time_epoch()

        # -- Perform traceback to original puzzle state -- #
        states: list = self.__parent_to_child_recur__(solution_state)

        # -- Using list of states, determine directions required -- #
        directions = self.__figure_out_directions__(states)

        # -- OUTPUT to console -- #
        self.ucs_scrolled_txt.insert(tk.INSERT, f'States Visited:  {len(seen) - 1}.\n')
        self.ucs_scrolled_txt.insert(tk.INSERT, f'Completed in {self.get_time_diff(start, end)}s.\n\n')
        self.ucs_scrolled_txt.insert(tk.INSERT, f'Sequence of moves  {len(states) - 1}.\n')

        for count, state in enumerate(states, -1):
            # -- Only move Canvas after initial state -- #
            if count >= 0:
                self.ucs_scrolled_txt.insert(tk.INSERT, f'{count + 1}.\t{directions[count]}\n')
            self.populate_puzzle_titles(state)
            self.__waiting__()

        # -- Clean possibly large list(s)/set(s) -- #
        del queue, seen

    def brfs_search(self):

        """
            Optional Algorithm.

            Summary:
                Breath-First Search (BFS) implementation to solve puzzle.

            Notes:
                Expands nodes out in clockwise in a cycle 'right', 'down', 'left', 'up'.
        """

        # -- Setup Timer -- #
        start = self.get_time_epoch()

        # -- OUTPUT to console -- #
        self.brfs_scrolled_txt.delete('1.0', tk.END)
        self.brfs_scrolled_txt.insert(tk.INSERT, 'Running ...\n')
        self.__waiting__()

        # -------------------- #
        # -- CORE Algorithm -- #
        # -------------------- #

        seen = set()
        queue = PriorityQueue()
        queue.add(priority=0, puzzle_state=self.initial_puzzle)
        solution_state = None
        while queue.is_empty() is False:
            # -- Get next item in queue -- #
            node = queue.pop()
            current_state = node.puzzle_state
            # -- Check for Gaol -- #
            if current_state == GOAL_STATE:
                solution_state = current_state
                break
            # -- Expand State -- #
            neighbors = current_state.generate_neighbors()
            for neighbor in neighbors:
                # -- Check if not already seen -- #
                if neighbor not in seen:
                    seen.add(neighbor)
                    # -- No priority here, just appending.          -- #
                    # -- Added function to priority_queue that      -- #
                    # -- allow for appending, which dramatically    -- #
                    # -- speeds up this algorithm, since add()      -- #
                    # -- is expensive.                              -- #
                    queue.append(puzzle_state=neighbor)

        # --------------------------- #
        # -- Goal State Discovered -- #
        # --------------------------- #

        # -- Close Timer-- #
        end = self.get_time_epoch()

        # -- Perform traceback to original puzzle state -- #
        states: list = self.__parent_to_child_recur__(solution_state)

        # -- Using list of states, determine directions required -- #
        directions = self.__figure_out_directions__(states)

        # -- OUTPUT to console -- #
        self.brfs_scrolled_txt.insert(tk.INSERT, f'States Visited:  {len(seen) - 1}.\n')
        self.brfs_scrolled_txt.insert(tk.INSERT, f'Completed in {self.get_time_diff(start, end)}s.\n\n')
        self.brfs_scrolled_txt.insert(tk.INSERT, f'Sequence of moves  {len(states) - 1}.\n')

        for count, state in enumerate(states, -1):
            # -- Only move Canvas after initial state -- #
            if count >= 0:
                self.brfs_scrolled_txt.insert(tk.INSERT, f'{count + 1}.\t{directions[count]}\n')
            self.populate_puzzle_titles(state)
            self.__waiting__()

        # -- Clean possibly large list(s)/set(s) -- #
        del queue, seen

    def befs_search(self):

        """
            Assignment Requirement.

            Summary:
                Best-First Search (BFS) implementation to solve puzzle.

            Notes:
                h() = Manhattan Distance (moves required by all titles to reach goal state)
        """

        # -- Setup Timer -- #
        start = self.get_time_epoch()

        # -- OUTPUT to console -- #
        self.befs_scrolled_txt.delete('1.0', tk.END)
        self.befs_scrolled_txt.insert(tk.INSERT, 'Running ...\n')
        self.__waiting__()

        # -------------------- #
        # -- CORE Algorithm -- #
        # -------------------- #

        seen = set()
        queue = PriorityQueue()
        queue.add(priority=0, puzzle_state=self.initial_puzzle)
        solution_state = None
        while queue.is_empty() is False:
            # -- Get next item in queue -- #
            node = queue.pop()
            current_state = node.puzzle_state
            # -- Check for Gaol -- #
            if current_state == GOAL_STATE:
                solution_state = current_state
                break
            # -- Expand State -- #
            neighbors = current_state.generate_neighbors()
            for neighbor in neighbors:
                # -- Check if not already seen -- #
                if neighbor not in seen:
                    seen.add(neighbor)
                    # -- Priority is based on h() -- #
                    priority = neighbor.calculate_manhattan_distance(GOAL_STATE)
                    queue.add(priority=priority, puzzle_state=neighbor)

        # --------------------------- #
        # -- Goal State Discovered -- #
        # --------------------------- #

        # -- Close Timer-- #
        end = self.get_time_epoch()

        # -- Perform traceback to original puzzle state -- #
        states: list = self.__parent_to_child_recur__(solution_state)

        # -- Using list of states, determine directions required -- #
        directions = self.__figure_out_directions__(states)

        # -- OUTPUT to console -- #
        self.befs_scrolled_txt.insert(tk.INSERT, f'States Visited:  {len(seen) - 1}.\n')
        self.befs_scrolled_txt.insert(tk.INSERT, f'Completed in {self.get_time_diff(start, end)}s.\n\n')
        self.befs_scrolled_txt.insert(tk.INSERT, f'Sequence of moves  {len(states) - 1}.\n')

        for count, state in enumerate(states, -1):
            # -- Only move Canvas after initial state -- #
            if count >= 0:
                self.befs_scrolled_txt.insert(tk.INSERT, f'{count + 1}.\t{directions[count]}\n')
            self.populate_puzzle_titles(state)
            self.__waiting__()

        # -- Clean possibly large list(s)/set(s) -- #
        del queue, seen

    def a_star_search(self):

        """
            Assignment Requirement.

            Summary:
                A* Search implementation to solve puzzle.

            Notes:
                h() = Manhattan Distance (moves required by all titles to reach goal state)
                g() = Distance from root (ie first puzzle state)
        """
        # -- Setup Timer -- #
        start = self.get_time_epoch()

        # -- OUTPUT to console -- #
        self.a_star_scrolled_txt.delete('1.0', tk.END)
        self.a_star_scrolled_txt.insert(tk.INSERT, 'Running ...\n')
        self.__waiting__()

        # -------------------- #
        # -- CORE Algorithm -- #
        # -------------------- #

        seen = set()
        queue = PriorityQueue()
        queue.add(priority=0, puzzle_state=self.initial_puzzle)
        solution_state = None
        while queue.is_empty() is False:
            # -- Get next item in queue -- #
            node = queue.pop()
            current_state = node.puzzle_state
            # -- Check for Gaol -- #
            if current_state == GOAL_STATE:
                solution_state = current_state
                break
            # -- Expand State -- #
            neighbors = current_state.generate_neighbors()
            for neighbor in neighbors:
                # -- Check if not already seen -- #
                if neighbor not in seen:
                    seen.add(neighbor)
                    # -- Priority is based on h() + g() -- #
                    priority = neighbor.calculate_manhattan_distance(GOAL_STATE) + neighbor.g
                    queue.add(priority=priority, puzzle_state=neighbor)

        # --------------------------- #
        # -- Goal State Discovered -- #
        # --------------------------- #

        # -- Close Timer-- #
        end = self.get_time_epoch()

        # -- Perform traceback to original puzzle state -- #
        states: list = self.__parent_to_child_recur__(solution_state)

        # -- Using list of states, determine directions required -- #
        directions = self.__figure_out_directions__(states)

        # -- OUTPUT to console -- #
        self.a_star_scrolled_txt.insert(tk.INSERT, f'States Visited:  {len(seen) - 1}.\n')
        self.a_star_scrolled_txt.insert(tk.INSERT, f'Completed in {self.get_time_diff(start, end)}s.\n\n')
        self.a_star_scrolled_txt.insert(tk.INSERT, f'Sequence of moves  {len(states) - 1}.\n')

        for count, state in enumerate(states, -1):
            # -- Only move Canvas after initial state -- #
            if count >= 0:
                self.a_star_scrolled_txt.insert(tk.INSERT, f'{count + 1}.\t{directions[count]}\n')
            self.populate_puzzle_titles(state)
            self.__waiting__()

        # -- Clean possibly large list(s)/set(s) -- #
        del queue, seen

    def __find_coordinates__(self, x, y) -> list:

        """     Takes one dimensional pointer and converts it to two dimensional   """

        return [
            (x * self.TILE_WIDTH) + self.TILE_BORDER,  # x1
            (y * self.TILE_HEIGHT) + self.TILE_BORDER,  # y1
            ((x + 1) * self.TILE_WIDTH) - self.TILE_BORDER,  # x2
            ((y + 1) * self.TILE_HEIGHT) - self.TILE_BORDER,  # y2
        ]

    def __waiting__(self):

        """     Sleep Function for Tkiner   """

        var = tk.IntVar()
        second = 1
        self.window.after(second * 100, var.set, 1)
        self.window.wait_variable(var)

    def __parent_to_child_recur__(self, puzzle_state):
        """     Returns a list of states from beginning to end  """
        if puzzle_state.parent is None:
            return [puzzle_state]
        return self.__parent_to_child_recur__(puzzle_state.parent) + [puzzle_state]

    @staticmethod
    def __figure_out_directions__(states: list) -> list:
        """     Given States, figure out what direction is required for each.   """
        directions = list()
        for i in range(len(states)):
            try:
                x1, y1 = states[i].blank_location
                x2, y2 = states[i+1].blank_location
                if x1 - x2 > 0:
                    # print(f'({x1},{y1}),({x2},{y2}),left')
                    directions.append('left')
                elif x1 - x2 < 0:
                    # print(f'({x1},{y1}),({x2},{y2}),right')
                    directions.append('right')
                elif y1 - y2 > 0:
                    # print(f'({x1},{y1}),({x2},{y2}),up')
                    directions.append('up')
                elif y1 - y2 < 0:
                    # print(f'({x1},{y1}),({x2},{y2}),down')
                    directions.append('down')
            except IndexError:
                return directions

    @staticmethod
    def get_time_epoch() -> float:
        return round(time.time(), 3)

    @staticmethod
    def get_time_diff(start: float, end: float) -> float:
        return round(end-start, 3)
