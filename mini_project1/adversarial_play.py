from go import *


infinity = 9999

class GameAdversary(Game):

    def utility(self, s, player):
        """Returns the payoff of state s if it is terminal (1 if p wins, -1
        if p loses, 0 in case of a draw), otherwise, its evaluation with respect
        to player p.
        To calculate the evaluation it uses the alpha beta cut
        off search, described further below

        s.player - player that is going to play this round
        player - being evaluated
        """
        k = 0.4

        if s.draw == -1:  # terminal test not yet run
            self.terminal_test(s)
        if s.draw == 1:
            return 0

        # calculate liberties of group with less liberties
        own_min = infinity
        own_liberties = 0
        for group in s.groups[player].values():
            own_liberties += group.n_liberties
            if group.n_liberties < own_min:
                own_min = group.n_liberties

        other_min = infinity
        other_liberties = 0
        for group in s.groups[3-player].values():
            other_liberties += group.n_liberties
            if group.n_liberties < other_min:
                other_min = group.n_liberties

        # verifies suicidal kill
        if other_min == 0 and own_min == 0:
            if s.player != player:
                return 1
            else:
                return -1

        # regular win
        if other_min == 0:
            return 1
        # regular death
        if own_min == 0:
            return -1

        own_group_min = s.groups_min_size[player]

        return (own_min - other_min) / (own_min + other_min)
        #return (lambda * (own_min/(own_min+other_min)) + (1-lambda)* ((own_min-other_min)/(own_min+other_min)))
        # return ((own_liberties-other_liberties)/(own_liberties+other_liberties))
        #return (k * own_min - (1 - k) * other_min) / (k * own_min + (1 - k) * other_min)

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


file_path = "/Users/ManuelSerraNunes/Desktop/Tecnico_5_1S/IA/Artificial_Intelligence_IST/mini_project1/examples/test05.txt"

game = Game()
game_adversary = GameAdversary()

file = open(file_path)
new_state = game.load_board(file)
file = open(file_path)
s = game_adversary.load_board(file)

initial_player = new_state.player


for rnd in [1, 2]:

    if rnd == 1:
        first_player = game
        second_player = game_adversary
    else:
        first_player = game_adversary
        second_player = game

    new_state = s
    display(new_state.group_board)

    i = 1

    while not game.terminal_test(new_state):

        # second player plays on even rounds
        if i % 2 == 0:
            action = alphabeta_cutoff_search(new_state, second_player, d=4, cutoff_test=None, eval_fn=None)
            new_state = second_player.result(new_state, action)

        # first player plays on odd rounds
        elif i % 2 != 0:
            action = alphabeta_cutoff_search(new_state, first_player, d=4, cutoff_test=None, eval_fn=None)
            new_state = first_player.result(new_state, action)

        display(new_state.group_board)

        i += 1

    # TODO: Remember to make sure that player 1 is the first one to play in the map, to that this makes sense
    if first_player.utility(new_state, initial_player) == 1:
        print('Player Game wins!')
    else:
        print('Player GameAdversary wins!')
