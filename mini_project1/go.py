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
        raise NotImplementedError

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
        raise NotImplementedError

    def result(self, s, a):
        """Return the state that results from making action a from state s."""
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
