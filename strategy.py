import random
import time
import copy


class Strategy():

   # implement all the required methods on your own
   def __init__(self):
      self.white = "o"
      self.black = "@"
      self.ogColor = ""
      self.opColor = ""
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True
      self.WEIGHTS = [[64, -6, 4, 4, 4, 4, -6, 64],
                      [-6, -8, -2, -2, -2, -2, -8, -6],
                      [4, -2, 2, 0, 0, 2, -2, 4],
                      [4, -2, 0, 2, 2, 0, -2, 4],
                      [4, -2, 0, 2, 2, 0, -2, 4],
                      [4, -2, 2, 0, 0, 2, -2, 4],
                      [-6, -8, -2, -2, -2, -2, -8, -6],
                      [64, -6, 4, 4, 4, 4, -6, 64]]

   def best_strategy(self, board, player, best_move, running):
      depth = 2
      self.ogColor = player
      self.opColor = self.opposite_color[player]
      while running.value:

         board = board.replace("?", "")
         new_board = []
         temp_list = []
         for x in range(len(board)):
            if ((x + 1) % 8) == 0:
               temp_list.append(board[x])
               new_board.append(temp_list)
               temp_list = []
            else:
               temp_list.append(board[x])
         self.x_max, self.y_max = len(new_board), len(new_board[0])

         move, value = self.alphabeta(new_board, depth, -100000, 100000, player, True)
         # max = -9999
         # moves = self.find_moves(new_board, player)
         # best = None
         # for m in moves:
         #    if max < self.WEIGHTS[m[0]][m[1]]:
         #       max = self.WEIGHTS[m[0]][m[1]]
         #       best = m

         new_move = ((move[0] + 1) * 10) + (move[1] + 1)
         best_move.value = new_move

         depth += 1

   def random(self, board, color):
      # returns best move
      # print(color)
      if self.first_turn:
         self.x_max, self.y_max = len(board), len(board[0])
      if color == "#ffffff":
         color = "O"
      else:
         color = "@"
      all_moves = self.find_moves(board, color)
      best_move = random.choice(tuple(all_moves))
      # board = self.make_move(board, color, best_move)
      return best_move, 0

   def find_flipped(self, board, x, y, color):
      # finds which chips would be flipped given a move and color
      if board[x][y] != ".":
         return []
      flipped_stones = []
      for incr in self.directions:
         temp_flip = []
         x_pos = x + incr[0]
         y_pos = y + incr[1]
         while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if board[x_pos][y_pos] == ".":
               break
            if board[x_pos][y_pos] == color:
               flipped_stones += temp_flip
               break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
      return flipped_stones

   def find_moves(self, board, color):
      # finds all possible moves
      moves_found = {}
      for i in range(len(board)):
         for j in range(len(board[i])):
            flipped_stones = self.find_flipped(board, i, j, color)
            if len(flipped_stones) > 0:
               moves_found.update({(i, j): flipped_stones})
      self.first_turn = False
      return moves_found

   def alphabeta(self, board, depth, alpha, beta, color, maximizingPlayer):
      if depth == 0:
         return None, self.evaluate(board, color)

      moves = self.find_moves(board, color)

      if not moves:
         other_moves = self.find_moves(board, self.opposite_color[color])
         if not other_moves:
            return None, self.evaluate(board, color)
         # Game isn't done, just passing.
         else:
            return self.alphabeta(board, depth - 1, alpha, beta, self.opposite_color[color], False)

      if maximizingPlayer:
         move, value = None, -10000
         for m in moves:
            _, val = self.alphabeta(
               self.make_move(board, color, m),
               depth - 1,
               alpha,
               beta,
               self.opposite_color[color],
               False
            )

            if val > value:
               value = val
               move = m

            alpha = max(alpha, value)

            if alpha >= beta:
               return move, value

         return move, value
      else:
         move, value = None, 10000
         for m in moves:
            _, val = self.alphabeta(
               self.make_move(board, color, m),
               depth - 1,
               alpha,
               beta,
               self.opposite_color[color],
               True
            )

            if val < value:
               value = val
               move = m

            beta = min(beta, value)

            if alpha >= beta:
               return move, value

         return move, value


   def make_move(self, board, color, move):
      # returns board that has been updated
      new_board = copy.deepcopy(board)
      new_board[move[0]][move[1]] = color
      for mo in self.find_flipped(board, move[0], move[1], color):
         new_board[mo[0]][mo[1]] = color
      return new_board

   def evaluate(self, board, color, possible_moves=None):
      # returns the utility value
      myval = len(self.find_moves(board, self.ogColor))
      opponentval = len(self.find_moves(board, self.opColor))
      for i in range(len(board)):
         for j in range(len(board[i])):
            if board[i][j] == self.ogColor:
               myval += self.WEIGHTS[i][j]
            elif board[i][j] == self.opColor:
               opponentval += self.WEIGHTS[i][j]

      # my_moves = self.find_moves(board, self.ogColor)
      # opponents_moves = self.find_moves(board, self.opColor)
      # myval += len(my_moves)
      # opponentval += len(opponents_moves)

      # print("eval value: ", eval)
      return (myval - opponentval)
