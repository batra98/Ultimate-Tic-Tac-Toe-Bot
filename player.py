"""
Class for AI bot
"""
import random
import traceback
import sys
from time import time

class Player_Cyber_Bot:
    """ 
    AI implemented 
    """
    
    def _init_(self):
        """
        Initialize variables
        """
        self.default=(1,1,1)#default move
        self.limit=23
        self.start=0

    def move(self,gameboard,oldmove,symbol):
        """
        Main code
        """
        try:
            if oldmove == (-1,-1,-1):
                return (0,4,4)
            
            self.start=time()
            # print self.start

            cells = gameboard.find_valid_move_cells(oldmove)
	    return cells[random.randrange(len(cells))]

        #
        #       preprocessing...
        #
        # for depth in range(...):
        #      minimax()
        #   return nxtmv
        #
        #
        #
        #
        #
        #
        #
        #

        
        except Exception as e:
            print 'Exception occurred ', e
            print 'Traceback printing ', sys.exc_info()
            print traceback.format_exc()