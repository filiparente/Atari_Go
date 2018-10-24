from go import *

# 1. LOAD EXAMPLE FILE
file = open("example1.txt")

# 2. INITIALIZE Go
go = Game()
go.load_board(file)
