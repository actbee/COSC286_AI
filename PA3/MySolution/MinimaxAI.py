# Author: Xuedan ZOU
# Date: 10/09/2021

import chess
import random
from time import sleep

class MinimaxAI():
    def __init__(self, depth):
        self.depth_max = depth
        self.MIN = -100000000
        self.MAX = 100000000
        self.board = chess.Board()
        self.choice = random.choice(list(self.board.legal_moves))
        self.turn = chess.WHITE
        # to count the deepest depth of the calling process
        self.deepest = 0
        # to count the number of calls
        self.cost = 0
        # we save the board here so there is no need to initialize a new board
        # during each function call to save our costs.

        # we do need to use a separate variable to memorize the most recent
        # choice we made during the searching process.

    def choose_move(self, board):
        self.board = board
        # to save WHITE or BLACK to current MinimaxAI
        self.turn = board.turn
        # always initialize them for each choose_move
        self.deepest = 0
        self.cost = 0

        self.minimax()

        best_move = self.choice
        sleep(1)  # I'm thinking so hard.
        print("Minimax AI recommending move " + str(best_move))
        print("The deepest depth for this turn is " + str(self.deepest))
        print("The number of calls it made to minimax is "+str(self.cost))
        return best_move

    # Here we use minimax algorithm with a max depth to search for the game
    # tree. All we need to know is the current depth, whether the current node
    # is max or min, and the board's situation.
    def minimax(self, depth=0, maxnode=True):
        # if we reach the deepest depth we should return current's situation's
        # heuristic value. Besides if right now the game is over we should stop
        # expanding new nodes and also return the value.

        # we count each call!
        self.cost += 1
        # we count the deepest depth
        if depth > self.deepest:
            self.deepest = depth

        if depth == self.depth_max or self.board.is_game_over() == True:

            return self.heuristic()

        # if we are now operating a maxnode, we should try to expand all the
        # possible situations with the child node to be min node and return the
        # max of those min nodes
        if maxnode == True:
            best_value = self.MIN
            for move in list(self.board.legal_moves):
                self.board.push(move)
                res = self.minimax(depth+1, False)
                # we dont want to initialize another new board which costs a lot
                # so we just pop the previous move to return to the current's board
                self.board.pop()
                if res > best_value:
                   # we use this method to keep track of the selected node.
                   if depth == 0 :
                      self.choice = move
                   best_value = res

            return best_value

        # similarly as the min node.
        else:
            best_value = self.MAX
            for move in list(self.board.legal_moves):
                self.board.push(move)
                res = self.minimax(depth+1, True)
                self.board.pop()
                if res < best_value:
                    best_value = res
            return best_value

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