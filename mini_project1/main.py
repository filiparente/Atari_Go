from go import *

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

def display(board):

    mystr = ""
    for row in board:
        mystr = ''.join([str(get_group_player(i)) for i in row])
        print(mystr)
        mystr = ""
    print("\n")

def get_group_player(group_number):
    if group_number == 0:
        return 0

    if group_number % 2 == 0:
        return 2
    else:
        return 1

def convert_to_tuple(mystr):
    a = (int(mystr[1]), int(mystr[3]), int(mystr[5]))
    return a



# file_path = "/Users/simaomoraessarmento/Dropbox/IST/S1/IA/Artificial_Intelligence_IST/mini_project1/examples/test_05.txt"
file_path = "/Users/ManuelSerraNunes/Desktop/Tecnico_5_1S/IA/Artificial_Intelligence_IST/mini_project1/examples/test_aplhago.txt"
file = open(file_path)


game = Game()
s = game.load_board(file)

new_state = s

i = 1

while not game.terminal_test(new_state):

    if not(i % 2 == 0):
        mystr = input("Next action: ")
        action = convert_to_tuple(mystr)
    else:
        action = alphabeta_cutoff_search(new_state, game, d=4, cutoff_test=None, eval_fn=None)

    new_state = game.result(new_state, action)

    display(new_state.group_board)

    i += 1





