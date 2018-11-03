from go import *


def display (board):

    for row in board:
        print(row)
        print("\n")

#file_path = "/Users/simaomoraessarmento/Dropbox/IST/S1/IA/Artificial_Intelligence_IST/mini_project1/examples/test_05.txt"
file_path = "/Users/ManuelSerraNunes/Desktop/Tecnico_5_1S/IA/Artificial_Intelligence_IST/mini_project1/examples/test_05_long.txt"
file = open(file_path)


game = Game()
s = game.load_board(file)

new_state = s

while(new_state.)
action = alphabeta_cutoff_search(new_state, game, d=4, cutoff_test=None, eval_fn=None)
new_state = game.result(s, action)

display(new_state.group_board)





