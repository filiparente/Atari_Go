from go import *


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





