import random
import copy
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List

from objective import getTopRow



class LocalSearch:
    def __init__(self):
        pass

    #ngitung heuristik untuk tiap pilihan trus ambil aja
    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        
        best_movement = self.hillclimbing(state)

        return best_movement

    def hillclimbing(self, state: State):
        #for every state, count objective, get max or min value from state, return that state
        listofmoves = [[0,ShapeConstant.CROSS], [0,ShapeConstant.CIRCLE],
        [1,ShapeConstant.CROSS], [1,ShapeConstant.CIRCLE],
        [2,ShapeConstant.CROSS], [2,ShapeConstant.CIRCLE],
        [3,ShapeConstant.CROSS], [3,ShapeConstant.CIRCLE],
        [4,ShapeConstant.CROSS], [4,ShapeConstant.CIRCLE],
        [5,ShapeConstant.CROSS], [5,ShapeConstant.CIRCLE],
        [6,ShapeConstant.CROSS], [6,ShapeConstant.CIRCLE],
        ]
        listofstates = {}
        for i in range(len(listofmoves)):
            temp = copy.deepcopy(state) #copy to temp state
            row = getTopRow(temp, listofmoves[i][0])
            if row != -1: #jika tidak udh full rownya
                temp.board.set_piece(row, listofmoves[i][0], listofmoves[i][1])
                heuristic = 0 #ini ganti dapet nilai heuristic brp
                listofstates[i] = heuristic
        
        ekstrim = 0 #ini ganti max atau min
        ans = [random.randint(0, 7), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])]
        for i in listofstates:
            value = listofstates[i]
            if (value > ekstrim): #ini ganti lebih besar atau lebih kecil
                ekstrim = value
                ans = listofmoves[i]

        return ans

