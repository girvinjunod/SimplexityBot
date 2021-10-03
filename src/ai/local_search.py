import random
import copy
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.utility import place
from src.ai.objective import countObjective
from typing import Tuple, List

# from src.ai.objective import getTopRow


class LocalSearch:
    def __init__(self):
        pass

    # ngitung heuristik untuk tiap pilihan trus ambil aja
    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = self.hillclimbing(state, n_player)

        return best_movement

    def hillclimbing(self, state: State, n_player: int):
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

        ekstrim = listofstates[0]  # ini ganti max atau min
        ans = listofmoves[0]

        for i in listofstates:
            value = listofstates[i]
            if value > ekstrim:
                ekstrim = value
                ans = listofmoves[i]

        print("ans",ans,listofstates)
        return ans
