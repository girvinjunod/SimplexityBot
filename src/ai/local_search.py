import random
import copy
import time

from random import randrange
from src.constant import ShapeConstant
from src.model import State
from src.utility import place
from src.ai.objective import countObjective
from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        pass

    # ngitung heuristik untuk tiap pilihan trus ambil aja
    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        best_movement = self.hillclimbing(state, n_player, thinking_time)

        return best_movement

    def hillclimbing(self, state: State, n_player: int, thinking_time: float):
        start = time.time()
        # for every state, count objective, get max or min value from state, return that state
        # cek kuota
        playerquota = state.players[n_player].quota
        circle = playerquota[ShapeConstant.CIRCLE]
        cross = playerquota[ShapeConstant.CROSS]
        # isi semua kemungkinan move
        listofmoves = []
        for i in range(state.board.col):
            if cross > 0:
                listofmoves.append([i, ShapeConstant.CROSS])
            if circle > 0:
                listofmoves.append([i, ShapeConstant.CIRCLE])
        # print(listofmoves)

        
        listofstates = {}
        for i in range(len(listofmoves)):
            end = time.time()
            if (end - start > thinking_time):
                return listofmoves[random.randrange(0, len(listofmoves))]
            temp = copy.deepcopy(state)  # copy to temp state

            valid = place(temp, n_player, listofmoves[i][1], listofmoves[i][0])
            if valid != -1:
                heuristic = countObjective(temp)  # ini ganti dapet nilai heuristic brp
                listofstates[i] = heuristic

        # print(listofstates)
        # ronde = state.round
        # if ronde % 2 == 1:
        #     maks = True
        # else:
        #     maks = False

        ekstrim = listofstates[0]
        ans = listofmoves[0]

        for i in listofstates:
            value = listofstates[i]
            if value > ekstrim:
                ekstrim = value
                ans = listofmoves[i]

        print("ans",ans,listofstates)
        return ans
