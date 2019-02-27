import random
import sys
import copy
import time

class Player_final:

    def __init__(self):

        self.default = (0,4,4)
        self.max_depth = 4
        self.Time_limit = 4.7
        self.symbol = None
        self.count_block_win = {'p': 0,'o': 0}
        self.next_move = (0,0,0)
        self.alpha = -100000000.0
        self.beta = +100000000.0
        self.tic = 0
        self.toc = 0 

    def move(self,gameboard,old_move,player_symbol):

        if old_move == (-1,-1,-1):
            return (0,4,4)
        self.tic  = time.time()
        if player_symbol == 'o':
            opponent_symbol = 'x'
        else:
            opponent_symbol = 'o'

        # temp = gameboard.small_boards_status
        # print(temp[0])

        self.count_block_win['p'] = sum(blocks.count(player_symbol) for blocks in gameboard.small_boards_status[0])
        self.count_block_win['p'] += sum(blocks.count(player_symbol) for blocks in gameboard.small_boards_status[1])
        self.count_block_win['o'] = sum(blocks.count(opponent_symbol) for blocks in gameboard.small_boards_status[0])
        self.count_block_win['o'] += sum(blocks.count(opponent_symbol) for blocks in gameboard.small_boards_status[1])

        self.symbol = player_symbol
        temp_board = copy.deepcopy(gameboard)
        # print(temp_board.find_valid_move_cells(old_move))
        # temp_block = copy.deepcopy(gameboard.small_boards_status)

        self.toc = (time.time()-self.tic)

        prev_move = (0,0,0)
        self.max_depth = 3

        while(self.toc < self.Time_limit):
            self.next_move = prev_move
            prev_move = self.minimax(temp_board,old_move,True,player_symbol,opponent_symbol,0,self.alpha,self.beta,-1,-1,-1)

            self.max_depth += 1
            self.toc = (time.time() - self.tic)

        Coordinates = (self.next_move[1],self.next_move[2],self.next_move[3])
        print(self.next_move[0])
        # cells = gameboard.find_valid_move_cells(old_move)
        return Coordinates
    

    def minimax(self, board, old_move, maxnode, player_flag, opponent_flag, depth, alpha, beta,best_board,best_row, best_col):
        if depth == self.max_depth:
            # print("in")
            utility = self.get_utility(board,player_flag,opponent_flag)
            # print(utility)
            return (utility,best_board,best_row,best_col)

        else:

            available_moves = board.find_valid_move_cells(old_move)
            # random.shuffle(available_moves)
            # print(available_moves)

            if len(available_moves) == 0:
                utility = self.get_utility(board,player_flag,opponent_flag)
                return (utility,best_board,best_row,best_col)

            # print(depth)
            # counter = 0
            for move in available_moves:
                # counter+=1
                current_board = copy.deepcopy(board)
                # print("papa\n")
                # current_board.print_board()
                # sign = player_flag

                if maxnode:
                    sign = player_flag
                elif not maxnode:
                    sign = opponent_flag

                current_board.update(old_move,move,sign)

                if maxnode == True:
                    minnode = False
                else:
                    minnode = True

                utility = self.minimax(current_board,move,minnode,player_flag,opponent_flag,depth+1,alpha,beta,best_board,best_row,best_col)

                if maxnode == True:
                    if utility[0] > alpha:
                        alpha = utility[0]
                        best_board,best_row,best_col = (move[0],move[1],move[2])
                else:
                    if utility[0] < beta:
                        beta = utility[0]
                        best_board,best_row,best_col = (move[0],move[1],move[2])
                
                if alpha > beta:
                    break

                # if (time.time() - self.tic) > self.Time_limit:
                #     return (utility,best_board,best_row,best_col)

            if maxnode:
                return (alpha,best_board,best_row,best_col)
            else:
                return (beta,best_board,best_row,best_col)



        
    

    def get_utility(self, board,player_flag, opponent_flag):
        gain = 0

        player_curr = sum(blocks.count(player_flag) for blocks in board.small_boards_status)
        opponent_curr = sum(blocks.count(opponent_flag) for blocks in board.small_boards_status)

        # print(self.count_block_win['p'])
        if self.count_block_win['p'] < player_curr and self.count_block_win['o'] == opponent_curr:
            gain += 50
        elif self.count_block_win['p'] < player_curr and self.count_block_win['o'] < opponent_curr:
            gain -= 50
        elif self.count_block_win['p'] < player_curr and (player_curr - self.count_block_win['p']) < (opponent_curr - self.count_block_win['o']):
            gain -= 20

        return gain