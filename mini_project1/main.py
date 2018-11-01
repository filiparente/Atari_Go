from go import *
import numpy as np

# 1. LOAD EXAMPLE FILE
file = open("example5.txt")

# 2. INITIALIZE Go
go = Game()
board = go.load_board(file)

