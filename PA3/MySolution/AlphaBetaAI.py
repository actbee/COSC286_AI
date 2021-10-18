# Author: Xuedan ZOU
# Date: 10/09/2021

import chess
from math import inf
from time import sleep
import random
from MinimaxAI import MinimaxAI

class AlphaBetaAI():
    def __init__(self, depth):
        self.depth_max = depth
        self.MIN = -100000000
        self.MAX = 100000000
        self.board = chess.Board()
        self.choice = random.choice(list(self.board.legal_moves))
        # this value is used to save the chosen behavior's heuristic value
        self.saved_besthur = 0
        self.turn = chess.WHITE
        # to count the number of calls
        self.cost = 0

    def choose_move(self, board):
        self.board = board
        # to save WHITE or BLACK to current MinimaxAI
        self.turn = board.turn
        self.cost = 0
        self.saved_besthur = self.alpha_beta()
        best_move = self.choice
        sleep(1)  # I'm thinking so hard.
        print("AlphaBeta AI recommending move " + str(best_move))
        print("The number of calls it made to alphabeta is " + str(self.cost))
        return best_move

    # alpha_beta search method is in general similar with minimax method
    def alpha_beta(self, depth=0, maxnode=True, alpha=-100000000, beta=100000000):
        '''
        # used for test
        if depth == 0:
            print(list(self.board.legal_moves))
        '''
        self.cost += 1

        if depth == self.depth_max or self.board.is_game_over() == True:
            return self.heuristic()

        if maxnode == True:
            # we should reorder the sequence of chidren
            next_moves = self.move_ordering(list(self.board.legal_moves), maxnode)
            value = self.MIN

            for move in next_moves:
                self.board.push(move)
                res = self.alpha_beta(depth + 1, False, alpha, beta)
                self.board.pop()
                if value < res:
                    value = res
                    if depth == 0:
                        self.choice = move
                # alpha = max(alpha,value)
                if value >= alpha:
                    alpha = value
                # there is no need to expand child if beta<= new alpha
                if beta <= alpha:
                  break

            return value

        else:
            next_moves = self.move_ordering(list(self.board.legal_moves), maxnode)
            value = self.MAX

            for move in next_moves:
                self.board.push(move)
                res = self.alpha_beta(depth + 1, True, alpha, beta)
                self.board.pop()
                if value > res:
                    value = res
                if value <= beta:
                    beta = value
                if beta <= alpha:
                    break

            return value


    def heuristic(self):

        # to see if the game is over now
        if self.board.is_game_over():
            # if this turn's side is over, this turn fails
            if self.board.is_checkmate():
                # to see if this turn is the MinimaxAI's turn
                if self.board.turn == self.turn:
                    # AI failed
                    return self.MIN
                else:
                    return self.MAX
            elif self.board.is_stalemate():
               return 0
            else:
               return 0

        # count the number of each type of chess for both BLACK and WHITE
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        # to check it is which turn
        if self.turn == chess.WHITE:
            material = 1 * (wp - bp) + 3 * (wn - bn) + 3 * (wb - bb) + 5 * (wr - br) + 9 * (wq - bq)
        else:
            material = 1 * (bp - wp) + 3 * (bn - wn) + 3 * (bb - wb) + 5 * (br - wr) + 9 * (bq - wq)
       # print(material)
        return material



    # we improve our alpha beta efficiency by re-ordering the children nodes
    def move_ordering(self, moves, maxnode=True):
       pairs = []
       for move in moves:
           self.board.push(move)
           heuristic_value = self.heuristic()
           self.board.pop()
           pair = (move, heuristic_value)
           pairs.append(pair)
       # print("pairs: "+"\n")
       # print(pairs)
       # sorted from low to great if we are minnode
       if maxnode == False:
            pairs.sort(
               key = lambda x : x[1] ,
               reverse = False
            )
       else:
           pairs.sort(
               key=lambda x: x[1],
               reverse=True
           )
       for i in range(0, len(moves)):
           moves[i] = pairs[i][0]
       # print("reordered: "+"\n")
       # print(moves)
       return moves


# used for test AlphaBetaAI
if __name__ == "__main__":
    player1 = AlphaBetaAI(3)
    player2 = MinimaxAI(3)

    # board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    # board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR")
    board = chess.Board("2b5/p1N3N1/7p/1p1p3k/2p2p2/8/PPQPPPPP/R1B1KB1R")
    print(board)
    player1.choose_move(board)
    print(board)
    player2.choose_move(board)

