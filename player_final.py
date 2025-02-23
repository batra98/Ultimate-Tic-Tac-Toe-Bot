import random
import sys
import copy
import time

class Player_final:

    def __init__(self):

        self.default = (0,4,4)
        self.max_depth = 2
        self.Time_limit = 2
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

        temp = gameboard.big_boards_status
        # print(temp)

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
        self.max_depth = 2

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
            utility_profit = self.get_utility(board,player_flag,opponent_flag)
            # print(utility_profit)
            return (utility_profit,best_board,best_row,best_col)

        else:

            available_moves = board.find_valid_move_cells(old_move)
            random.shuffle(available_moves)
            # print(available_moves)

            if len(available_moves) == 0:
                utility_profit = self.get_utility(board,player_flag,opponent_flag)
                return (utility_profit,best_board,best_row,best_col)

            # print(depth)
            # counter = 0
            for move in available_moves:
                # print(move)
                # counter+=1
                current_board = copy.deepcopy(board)
                # print("papa\n")
                # sign = player_flag

                
                sign = player_flag
                if not maxnode:
                    sign = opponent_flag

                current_board.update(old_move,move,sign)
                # current_board.print_board()

                # if maxnode == True:
                #     utility = self.minimax(current_board,move,False,player_flag,opponent_flag,depth+1,alpha,beta,best_board,best_row,best_col)
                    
                # else:
                #     utility = self.minimax(current_board,move,True,player_flag,opponent_flag,depth+1,alpha,beta,best_board,best_row,best_col)
                    

                # print minnode

                # utility = self.minimax(current_board,move,minnode,player_flag,opponent_flag,depth+1,alpha,beta,best_board,best_row,best_col)

                if maxnode == True:
                    utility = self.minimax(current_board,move,False,player_flag,opponent_flag,depth+1,alpha,beta,best_board,best_row,best_col)

                    if utility[0] > alpha:
                        alpha = utility[0]
                        best_board,best_row,best_col = (move[0],move[1],move[2])
                else:
                    utility = self.minimax(current_board,move,True,player_flag,opponent_flag,depth+1,alpha,beta,best_board,best_row,best_col)

                    if utility[0] < beta:
                        beta = utility[0]
                        best_board,best_row,best_col = (move[0],move[1],move[2])
                # print(utility)
                if alpha >= beta:
                    break

                if (time.time() - self.tic) > self.Time_limit:
                    return (utility,best_board,best_row,best_col)

            if maxnode:
                return (alpha,best_board,best_row,best_col)
            else:
                return (beta,best_board,best_row,best_col)
            # print(utility)
            # return utility



        
    

    def get_utility(self, board, player_flag, opponent_flag):

        profit = 0

        scale = 100.0
        utility_block = [[0 for b in range(9)] for c in range(2)]
        utility_board = [0 for c in range(2)]

        for i in range(2):
            my_board = board.big_boards_status[i]
            for j in range(9):
                utility_block[i][j] = self.check_pattern_block(my_board, j, player_flag, opponent_flag)
                utility_block[i][j] /= scale

        for i in range(2):
            small_board = board.small_boards_status[i]
            utility_board[i] = self.check_pattern_board(small_board, i, utility_block, player_flag, opponent_flag)

        # for i in range(2):
        #     print(utility_block[i])

        # print("\n")



        temp_small = [item for sublist in board.small_boards_status for item in sublist]

        player_curr = sum(blocks.count(player_flag) for blocks in temp_small)
        opponent_curr = sum(blocks.count(opponent_flag) for blocks in temp_small)

        # print(self.count_block_win['p'],player_curr)
        if self.count_block_win['p'] < player_curr and self.count_block_win['o'] == opponent_curr:
            profit += 50
        elif self.count_block_win['p'] < player_curr and self.count_block_win['o'] < opponent_curr:
            profit -= 50
        elif self.count_block_win['p'] < player_curr and (player_curr - self.count_block_win['p']) < (opponent_curr - self.count_block_win['o']):
            profit -= 20

        return profit + utility_board[0] + utility_board[1]

    def check_pattern_board(self, board, board_idx, utility_block, player_flag, opponent_flag):
        
        profit = 0

        for itr_y in range(3):
            util_val = 0
            empty = 0
            player = 0
            enemy = 0
            for itr_x in range(3):
                util_val += utility_block[board_idx][itr_x * 3 + itr_y]
                if board[itr_y][itr_x] == '-':
                    empty += 1
                elif board[itr_y][itr_x] == player_flag:
                    player += 1
                elif board[itr_y][itr_x] == opponent_flag:
                    enemy += 1

            profit += self.get_mult(util_val)
            profit += self.calc_total(player, enemy)

        for itr_x in range(3):
            util_val = 0
            empty = 0
            player = 0
            enemy = 0
            for itr_y in range(3):
                util_val += utility_block[board_idx][itr_x * 3 + itr_y]
                if board[itr_y][itr_x] == '-':
                    empty += 1
                elif board[itr_y][itr_x] == player_flag:
                    player += 1
                elif board[itr_y][itr_x] == opponent_flag:
                    enemy += 1

            profit += self.get_mult(util_val)
            profit += self.calc_total(player, enemy)

        util_val = 0
        empty = 0
        player = 0
        enemy = 0    

        for itr in range(3):

            util_val += utility_block[board_idx][itr * 3 + itr]

            if board[itr][itr] == '-':
                empty += 1
            elif board[itr][itr] == player_flag:
                player += 1
            elif board[itr][itr] == opponent_flag:
                enemy += 1

        profit += self.get_mult(util_val)
        profit += self.calc_total(player, enemy)

        util_val = 0
        empty = 0
        player = 0
        enemy = 0    

        for itr in range(3):

            util_val += utility_block[board_idx][itr * 2 + 2]
            index_y = itr
            index_x = 2 - itr

            if board[index_y][index_x] == '-':
                empty += 1
            elif board[index_y][index_x] == player_flag:
                player += 1
            elif board[index_y][index_x] == opponent_flag:
                enemy += 1

        profit += self.get_mult(util_val)
        profit += self.calc_total(player, enemy)

        return profit    


    def check_pattern_block(self, board, block_idx, player_flag, opponent_flag):
        profit = 0

        x_idx = ( block_idx % 3 ) * 3
        y_idx = ( block_idx / 3 ) * 3

        for itr_y in range(y_idx, y_idx + 3):
            empty = 0
            player = 0
            enemy = 0
    
            for itr_x in range(x_idx, x_idx + 3):
                if board[itr_y][itr_x] == '-':
                    empty += 1
                elif board[itr_y][itr_x] == player_flag:
                    player += 1
                elif board[itr_y][itr_x] == opponent_flag:
                    enemy += 1

            profit = self.calc_pattern(player, enemy, profit)

        
        for itr_x in range(x_idx, x_idx + 3):
            empty = 0
            player = 0
            enemy = 0
    
            for itr_y in range(y_idx, y_idx + 3):
                if board[itr_y][itr_x] == '-':
                    empty += 1
                elif board[itr_y][itr_x] == player_flag:
                    player += 1
                elif board[itr_y][itr_x] == opponent_flag:
                    enemy += 1

            profit = self.calc_pattern(player, enemy, profit)

        empty = 0
        player = 0
        enemy = 0    

        for itr in range(3):
            index_y = y_idx + itr
            index_x = x_idx + itr

            if board[index_y][index_x] == '-':
                empty += 1
            elif board[index_y][index_x] == player_flag:
                player += 1
            elif board[index_y][index_x] == opponent_flag:
                enemy += 1

        profit = self.calc_pattern(player, enemy, profit)

        empty = 0
        player = 0
        enemy = 0    

        for itr in range(3):
            index_y = y_idx + itr
            index_x = x_idx + 2 - itr

            if board[index_y][index_x] == '-':
                empty += 1
            elif board[index_y][index_x] == player_flag:
                player += 1
            elif board[index_y][index_x] == opponent_flag:
                enemy += 1

        profit = self.calc_pattern(player, enemy, profit)


        return profit
    


    def calc_pattern(self, num_player, num_enemy, profit):

        # print (num_player, num_enemy)
        player_dict = {
            0 : 0,
            1 : 1,
            2 : 10,
            3 : 100,
        }

        enemy_dict = {
            0 : 0,
            1 : -1,
            2 : -10,
            3 : -100,
        }
        
        profit += player_dict[num_player]
        profit += enemy_dict[num_enemy]

        return profit

    def get_mult(self, util_val):
        increment = 0

        if util_val >= 3:
            increment = 100
            increment += (util_val - 3) * 900

        if 2 <= util_val < 3:
            increment = 10
            increment += (util_val - 2) * 90

        if 1 <= util_val < 2:
            increment = 1
            increment += (util_val - 1) * 9

        if -1 <= util_val < 1:
            increment = util_val

        if -2 <= util_val < -1:
            increment = -1
            increment -= (abs(util_val) - 1) * 9

        if -3 <= util_val < -2:
            increment = -2
            increment -= (abs(util_val) - 2) * 90

        if util_val < -3:
            increment = -100
            increment -= (abs(util_val) - 3) * 900

        return increment

    def calc_total(self, num_player, num_enemy):
        
        increment = 0

        player_dict = {
            0 : 0,
            1 : 10,
            2 : 100,
            3 : 1000,
        }

        enemy_dict = {
            0 : 0,
            1 : -10,
            2 : -100,
            3 : -1000,
        }
        
        increment += player_dict[num_player]
        increment += enemy_dict[num_enemy]

        return increment

        



