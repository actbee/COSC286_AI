# Author: Xuedan ZOU
# Date: 10/09/2021

import chess
import random
from time import sleep

class RandomAI():
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        if moves:
          move = random.choice(moves)
        else:
          move = chess.Move.null()
          print("RandomAI has loosed")
        sleep(1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))
        return move
