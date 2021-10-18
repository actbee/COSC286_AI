# Author: Xuedan ZOU
# Date: 10/09/2021

import chess
from math import inf
from time import sleep
import random
from AlphaBetaAI import AlphaBetaAI

class InteractiveDeepeningAI():
    def __init__(self, depth):
        self.depth_max = depth
        self.board = chess.Board()
        self.choice = random.choice(list(self.board.legal_moves))

    def choose_move(self, board):
        # always begin with the max-depth 1
        depth = 1
        move_list = []
        # we use the alphabeta search with an increasing depth value
        # interactively until it equals to our given max depth
        while(depth <= self.depth_max):
            try_player = AlphaBetaAI(depth)
            try_move = try_player.choose_move(board)
            move_list.append((try_move, try_player.saved_besthur))
            depth += 1

        # ordered by giving the greatest saved_besthur value's move first
        move_list.sort(
            key=lambda x: x[1],
            reverse=True
        )
        best_move = move_list[0][0]

        sleep(1)  # I'm thinking so hard.
        print("Interactive Deepening AI recommending move " + str(best_move))

        return best_move