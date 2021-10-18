# Author: Xuedan ZOU
# Date: 10/09/2021

# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from InteractiveDeepeningAI import InteractiveDeepeningAI
from ChessGame import ChessGame


import sys


player1 = InteractiveDeepeningAI(3)
# player1 = AlphaBetaAI(3)
# player1 = MinimaxAI(3)
# player2 = MinimaxAI(3)
player2 = RandomAI()

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()

print(game)
print("The result is: "+game.board.result())

#print(hash(str(game.board)))
