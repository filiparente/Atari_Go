from go import *
import numpy as np

# 1. LOAD EXAMPLE FILE
file = open("example1.txt")

# 2. INITIALIZE Go
go = Game()
board = go.load_board(file)

group_board = [[0]*len(board)]*len(board)
p1_counter = 1
p2_counter = 2


for row in range(len(board)):
    for col in range(len(board)):
        
        color = board[row][col]
        
        ## check if the current position is a piece
        if board[row][col] != 0:
            
            ## check point bellow
            #if row + 1 <= len(board):
                #if color == board[row+1][col]:

                    ## adicionar ao grupo
                    
            if row - 1 >= 0:
                if group_board[row-1][col] != 0 and board[row-1][col] == color:
                    group_board[row][col] = group_board[row-1][col]
                    print(group_board)
                    ## adicionar ao grupo

            ##if col + 1 <= len(board):
                

            if(col -1 >= 0):
                 if group_board[row][col-1] != 0 and board[row][col-1] == color:
                    group_board[row][col] = group_board[row][col-1]
                    print(group_board)
                    ## adicionar ao grupo
                
            if group_board[row][col] == 0:
                # new group
                if color == 1:
                    group_board[row][col] = p1_counter
                    print(group_board)
                    p1_counter += 2
                
                elif color == 2:
                    group_board[row][col] = p2_counter
                    print(group_board)
                    p2_counter += 2
