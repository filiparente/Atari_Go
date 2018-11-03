from go import *

#file_path = "/Users/simaomoraessarmento/Dropbox/IST/S1/IA/Artificial_Intelligence_IST/mini_project1/examples/test_05.txt"
file_path = "/Users/ManuelSerraNunes/Desktop/Tecnico_5_1S/IA/Artificial_Intelligence_IST/mini_project1/examples/test_05_long.txt"
file = open(file_path)


game = Game()
s = game.load_board(file)
act = game.actions(s)


alphabeta_cutoff_search(s, game, d=4, cutoff_test=None, eval_fn=None)

