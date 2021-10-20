import random
import copy
import time

from random import randrange
from src.constant import ShapeConstant
from src.model import State
from src.utility import place, is_win
from typing import Tuple, List

'''

-------------------- OBJECTIVE FUNCTION --------------------

'''
def getEmptyAdj(state: State, row: int, col: int):
    """
    [DESC]
        Funtion to get empty adjacent cells
    [PARAMS]
        state : State -> current state
        row, col : int -> current cell
    [RETURN]
        Array of Tuple[row, col]: adjacent cells direction
    """
    adj_cell = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    ret = []

    for cell in adj_cell:
        try :
            if state.board[row + cell[0], col + cell[1]].shape == ShapeConstant.BLANK and row + cell[0] >= 0 and row + cell[0] < state.board.row and col + cell[1] >= 0 and col + cell[1] < state.board.col :
                ret.append(cell)
        except :
            pass

    if not(ret) :
        return []

    if (1, -1) in ret :
        try : ret.remove((0,-1))
        except :pass
        try :ret.remove((-1,-1))
        except :pass
    if (1, 1) in ret :
        try : ret.remove((0, 1))
        except : pass
        try : ret.remove((-1, 1)) 
        except : pass
    if not((1,-1) in ret) :
        if (0,-1) in ret :
            try : ret.remove((-1,-1))
            except : pass
    if not((1,1) in ret) :
        if (0,1) in ret :
            try : ret.remove((-1,1))
            except : pass

    return ret

def countObjective(state : State, isCurPlayer : bool = True) :
    '''
    [DESC]
        Count objective value given state
    [PARAMS]
        state : State -> current state
        isCurPlayer : bool -> true if is current player
    [RETURN]
        int : objective value of current state
    '''
    curPlayer = state.players[(state.round + (1 if isCurPlayer else 0)) % 2]
    enemyPlayer = state.players[(state.round + (0 if isCurPlayer else 1)) % 2]

    objVal = 0
    listStreak = []

    for col in range(state.board.col) :
        for row in range(state.board.row-1,-1,-1) :
            if state.board[row,col].shape != ShapeConstant.BLANK :
                tmpAdjCell = getEmptyAdj(state, row, col)
                if tmpAdjCell :
                    for cell in tmpAdjCell :
                        # Streak count on shape
                        streak = 1
                        tmpRow = row
                        tmpCol = col
                        while True :
                            try :
                                if state.board[tmpRow, tmpCol].shape == curPlayer.shape :
                                    multiplier = 1
                                elif state.board[tmpRow, tmpCol].shape == enemyPlayer.shape :
                                    multiplier = -1

                                if (
                                    tmpRow + (cell[0] * -1) >= 0 and 
                                    tmpRow + (cell[0] * -1) < state.board.row and 
                                    tmpCol + (cell[1] * -1) >= 0 and 
                                    tmpCol + (cell[1] * -1) < state.board.col and 
                                    state.board[tmpRow + (cell[0] * -1), tmpCol + (cell[1] * -1)].shape == state.board[tmpRow, tmpCol].shape
                                ) :
                                    streak += 1
                                    tmpRow += (cell[0] * -1)
                                    tmpCol += (cell[1] * -1)
                                else :
                                    listStreak.append(streak * multiplier)
                                    break
                            except :
                                break
                        # Streak count on color
                        streak = 1
                        tmpRow = row
                        tmpCol = col
                        while True :
                            try :
                                if state.board[tmpRow, tmpCol].color == curPlayer.color :
                                    multiplier = 1
                                elif state.board[tmpRow, tmpCol].color == enemyPlayer.color :
                                    multiplier = -1

                                if (
                                    tmpRow + cell[0] * -1 >= 0 and 
                                    tmpRow + cell[0] * -1 < state.board.row and 
                                    tmpCol + cell[1] * -1 >= 0 and 
                                    tmpCol + cell[1] * -1 < state.board.col and 
                                    state.board[tmpRow + (cell[0] * -1), tmpCol + (cell[1] * -1)].color == state.board[tmpRow, tmpCol].color
                                ) :
                                    streak += 1
                                    tmpRow += cell[0] * -1
                                    tmpCol += cell[1] * -1
                                else :
                                    listStreak.append(streak * multiplier)
                                    streak = 1
                                    break
                            except :
                                break

    listScore = [0,4,10,50,10000,10000,10000,10000]
    # Counting objective value
    for streak in listStreak :
        if streak < 0 :
            if streak <= -2 :
                objVal -= listScore[streak * -1] * 2
            else :
                objVal -= listScore[streak * -1]
        else :
            objVal += listScore[streak]

    return objVal

'''

-------------------- LOCAL SEARCH CLASS --------------------

'''
class LocalSearchGroup1:
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
        availableMoves = []
        for i in range(len(listofmoves)):
            end = time.time()
            if (end - start > thinking_time):
                return listofmoves[random.randrange(0, len(listofmoves))]
            temp = copy.deepcopy(state)  # copy to temp state

            valid = place(temp, n_player, listofmoves[i][1], listofmoves[i][0])
            if valid != -1:
                win_condition = is_win(temp.board)
                
                value = 0
                if win_condition != None:
                    shape, color = win_condition
                    winner =  ((temp.players[n_player].shape == shape) 
                        and (temp.players[n_player].color == color)) 
                    value = 10000 if winner else -10000
                if value != 0:
                    listofstates[i] = value
                else:
                    heuristic = countObjective(temp)
                    listofstates[i] = heuristic
                availableMoves.append(i)

        # print(listofstates)
        # ronde = state.round
        # if ronde % 2 == 1:
        #     maks = True
        # else:
        #     maks = False

        ekstrim = listofstates[availableMoves[0]]
        ans = listofmoves[availableMoves[0]]

        for i in listofstates:
            value = listofstates[i]
            if value > ekstrim:
                ekstrim = value
                ans = listofmoves[i]

        # print("ans",ans,listofstates)
        return ans
