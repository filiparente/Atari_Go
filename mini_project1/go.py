class Group:
    """
    This class stores the necessary values for the group identification, namely:

        - 'elements' - list of (i,j) elements in the group
        - 'liberties' - set of (i,j) liberties of the group
        - 'n_liberties' - number of liberties of the group

    """
    def __init__(self, initial_element):
        """

        :param initial_element: tuple with point coordinates
        """
        self.elements = [initial_element]
        self.liberties = set()
        self.n_liberties = 0

    def add_element(self, element):
        """
        Adds a list of elements (list of tuples) to the group.
        """
        self.elements.extend(element)

    def add_liberty(self, liberty):
        """
        Adds liberty one by one. If size changes, it means
        liberty was not yet on the set and therefore number
        of liberties must be incremented
        """
        previous_len = len(self.liberties)
        self.liberties.add(liberty)  # only adds to the set if the element is not present already
        updated_len = len(self.liberties)

        if previous_len < updated_len:
            self.n_liberties += 1

    def update_liberties(self, row, col, board):
        """
        This function calculates the liberties for the given point,
        and updates the corresponding group information regarding so.

        :param row: row point position
        :param col: col point position
        :param board: matrix with board pieces
        :param group_board: matrix with board groups
        :param player: next player to move
        :param groups: dictionary with groups' information
        """

        # check all 4 neighbors. If the neighbor is empty (= 0) its a liberty

        if row - 1 >= 0:
            if board[row - 1][col] == 0:
                self.add_liberty((row - 1, col))
        if row + 1 < len(board):
            if board[row + 1][col] == 0:
                self.add_liberty((row + 1, col))
        if col - 1 >= 0:
            if board[row][col - 1] == 0:
                self.add_liberty((row, col - 1))
        if col + 1 < len(board):
            if board[row][col + 1] == 0:
                self.add_liberty((row, col + 1))

    def merge_groups(self, player, groups, left_neighbor_group):
        """
        This function is responsible for merging two connected groups initially
        identified as separated components.

        :param row: row point position
        :param col: col point position
        :param player: next player to move
        :param groups: dictionary with groups' information
        :param left_neighbor_group: group to merge
        :param group_board: matrix with board groups

        :return board elements to update on the board
        """

        # 1) merge elements
        elements_to_merge = groups[player][left_neighbor_group].elements
        self.add_element(elements_to_merge)

        # 2) merge liberties (liberties count is updated internally)
        liberties_to_merge = groups[player][left_neighbor_group].liberties
        for liberty in liberties_to_merge:
            self.add_liberty(liberty)

        return elements_to_merge


class State:
    """
    This class stores the necessary values for the state definition

    - player - defines next player to move
    - group_board - displays the board with the component's groups
    - groups - dictionary with a Group structure for player 1 and player 2
    - counters - dictionary with group counter for player 1 and player 2

    Note:
    1) player's counters are necessary when adding more groups, to avoid overwritting
    groups already created
    2) To access player N group structure or counter, just use N as key. (e.g: groups[1] returns
    group structure for player 1)
    3) to make it more intuitive, groups for player 1 are odd, whereas groups for player 2 are even
    """

    def __init__(self, player, size, initial_board):
        self.player = player
        self.size = size

        group_board, player_groups, player_counters = self.initialize_groups(initial_board)
        self.group_board = group_board
        self.groups = player_groups
        self.counters = player_counters

    def initialize_groups(self, initial_board):
        """
        This function receives the initial board and returns the state parameters

        :param initial_board: initial board configuration read from file
        :return: group_board: board with component labels
                 player_groups: dict with groups for each player
                 player_counters: key counter for each player
        """

        """
        Component identification goes as follows:
        1) Look for a group neighbor on the row above. If existent, join group.
        2) Look for a group neighbor on the col on the left. If existent:
            2.1) If neighbor was found both on top and left, then merge left group
                 w/ top group
            2.2) If only left neighbor was found, then join current point to left
                 group.
        3) If no neighbor was found (same player piece in any of the neighboring points)
           then a new group is created
        """

        # a matrix containing the number of the group each point belongs to or 0 (for empty)
        group_board = [[0] * len(initial_board) for i in range(len(initial_board))]
        # the groups for player 1 and for player 2
        groups = {1: dict(), 2: dict()}
        # counter for the group names. player 1: odd numbers; player 2: even numbers
        counters = {1: 1, 2: 2}

        for row in range(len(initial_board)):
            for col in range(len(initial_board)):

                player = initial_board[row][col]

                # Check if current point is occupied. If not, it just skips to next point
                if initial_board[row][col] != 0:

                    if row - 1 >= 0:
                        top_neighbor = initial_board[row - 1][col]
                        top_neighbor_group = group_board[row - 1][col]

                        if top_neighbor_group != 0 and top_neighbor == player:
                            # updates group board
                            group_board[row][col] = top_neighbor_group
                            # adds element to group structure
                            new_elements = [(row, col)]
                            groups[player][group_board[row][col]].add_element(new_elements)

                    if col - 1 >= 0:
                        left_neighbor = initial_board[row][col - 1]
                        left_neighbor_group = group_board[row][col - 1]

                        if left_neighbor_group != 0 and left_neighbor == player:
                            # verifies if groups must be merged (condition 2.1)
                            # by checking group_board[row][col] != 0, we ensure a group has been
                            # attributed before
                            if group_board[row][col] != 0 and left_neighbor_group != group_board[row][col]:
                                # updates left neighbor's group elements
                                group = group_board[row][col]
                                elements_to_merge = groups[player][group].merge_groups(player, groups, left_neighbor_group)

                                # removes old group from dictionary
                                groups[player].pop(left_neighbor_group)
                                # updates group board
                                for old_element_row, old_element_col in elements_to_merge:
                                    group_board[old_element_row][old_element_col] = group_board[row][col]

                            # no neighbor on top, just join left neighbor's group (condition 2.2)
                            elif group_board[row][col] == 0:
                                # updates group board
                                group_board[row][col] = left_neighbor_group
                                # adds element to group structure
                                new_elements = [(row, col)]
                                groups[player][group_board[row][col]].add_element(new_elements)

                    # if no merging neighbors were found, than just creates a new group
                    if group_board[row][col] == 0:
                        group_board[row][col] = counters[player]
                        groups[player][counters[player]] = Group((row, col))
                        counters[player] += 2

                    # Finally, add information about group's liberties to the structure
                    group = group_board[row][col]
                    groups[player][group].update_liberties(row, col, initial_board)

        return group_board, groups, counters

    def update_state(self):
        """
        This function updates the state representation after a change in the state

        """


class Game:
    """
    This class implements the Atari Go game.

    While Go scoring is based on both surrounded territory and captured stones,
    the Atari Go finishes when the first stone is captured. More information on
    Atari Go can be found here:
        https://senseis.xmp.net/?CaptureGo

    This class assumes the following:
        - players: Players are represented with the integers 1 for black and 2 for white
        - actions: Actions are represented as a tuple (p,i,j) where:
                - p ∈ {1, 2} is the player
                - i ∈ {1, . . . , N} is the row
                - j ∈ {1, . . . , N} is the column
                (assuming that (1,1) corresponds to the top left position and the size of the board is N)
        - states:

    Note: A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test.
    """

    def to_move(self, s):
        """Returns the player to move next given the state s."""
        return s.player

    def terminal_test(self, s):
        """Returns a boolean of whether state s is terminal."""
        return not self.actions(s)

    def utility(self, s, player):
        """Returns the payoff of state s if it is terminal (1 if p wins, -1
        if p loses, 0 in case of a draw), otherwise, its evaluation with respect
        to player p.
        To calculate the evaluation it uses the alpha beta cut
        off search, described further below"""
        raise NotImplementedError

    def actions(self, s):
        """Returns a list of valid moves at state s."""

        # iterate board

            # if position == 0:

                # if any neighbor is empty:
                    # add point to list of allowed actions
                    # continue to next point

                # if any neighbor is the same color and has 1+ liberties:
                    # add point to list of allowed actions
                    # continue to next point

                # if any neighbor is the other color and has only 1 liberty: (suicide+kill play)
                    # add point to list of allowed actions

        # return actions

        raise NotImplementedError

    def result(self, s, a):
        """Return the state that results from making action a from state s.

        Generates next state and verifies if it is terminal."""

        raise NotImplementedError

    def display(self, s):
        """Print or otherwise display the state."""
        print(s)

    def load_board(self, file):
        """Loads a board from an opened file and returns the corresponding state"""

        # 1. First line should contain:
        #   - size of board
        #   - next player to move
        line1 = file.readline()
        size, player = map(int, line1.split(' '))
        print('Board size: {}x{}'.format(size, size))
        print('Next player to move: ', player)

        # 2. Load board into matrix
        board = []
        for row in range(size):
            board_row = file.readline().split('\n')[0]
            board.append([int(point) for point in board_row])

        print(board)

        # 3. Initialize state
        s = State(player, size, initial_board=board)

        return s

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


# SEARCH algorithm (manually imported into the project, see source in description):
def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """
    From: "https://github.com/aimacode/aima-python/blob/master/games.py"

    Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    """
    infinity = float('inf')

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                                         game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action
