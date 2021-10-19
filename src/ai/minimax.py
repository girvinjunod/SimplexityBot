import random
import copy
import multiprocessing as mp
from time import time

from src.constant import ShapeConstant, GameConstant
from src.utility import place, is_win
from src.model import State, Board, Player

from typing import Tuple, List

WIN_SCORE = 10000
LOSE_SCORE = -10000

'''
-------------------- NODE CLASS --------------------
'''
class Node:
    def __init__(self, depth: int, state: State, value: int, n_player: int) -> None:
        self.depth : int = depth
        self.state : State = state
        self.children : Node.array = []
        self.value : int = value
        self.n_player : int = n_player
    
    def initChild(self) -> None:
        for i in range(self.state.board.col):
            xBoard = copy.deepcopy(self.state.board)
            xPlayers = copy.deepcopy(self.state.players)
            xState = State(xBoard, xPlayers, self.state.round+1)
            xrow = place(xState, (self.state.round+1)%2, ShapeConstant.CROSS, i)

            if (xrow >= 0):
                win_condition = is_win(xState.board)

                value = 0
                if win_condition != None:
                    shape, color = win_condition
                    winner =  ((self.state.players[self.n_player].shape == shape) 
                        and (self.state.players[self.n_player].color == color)) 
                    value = WIN_SCORE if winner else LOSE_SCORE
                self.children.append(Node(self.depth+1, xState, value, self.n_player)) 
            else :
                self.children.append(None)
                

            oBoard = copy.deepcopy(self.state.board)
            oPlayers = copy.deepcopy(self.state.players)
            oState = State(oBoard, oPlayers, self.state.round+1)
            orow = place(oState, (self.state.round+1)%2, ShapeConstant.CIRCLE, i)

            if (orow >= 0):
                win_condition = is_win(oState.board)
                
                value = 0
                if win_condition != None:
                    shape, color = win_condition
                    winner =  ((self.state.players[self.n_player].shape == shape) 
                        and (self.state.players[self.n_player].color == color)) 
                    value = WIN_SCORE if winner else LOSE_SCORE
                self.children.append(Node(self.depth+1, oState, value, self.n_player))
            else :
                self.children.append(None)
                
    def printTree(self):
        if len(self.children)==0:
            print(self.depth*"   " + str(self.value))
        else:
            print(self.depth*"   " + str(self.value))
            if (self.depth >= 2):
                for node in self.children:
                    if node :
                        node.printTree()
            else:
                self.children[2].printTree()
        

    def __str__(self) :
        res = "Depth : " + str(self.depth) + " | "
        res += "Value : " + str(self.value) + "\n"
        return res


def createTree(node: Node, maxDepth: int):
    node.initChild()
    current: Node = node
    stack: Node.Array = copy.copy(current.children)
    while True:
        if stack:
            current = stack.pop()
            if current and current.depth < maxDepth and abs(current.value)<WIN_SCORE:
                current.initChild()

                if (current.depth != maxDepth-1):
                    stack = copy.copy(current.children) + stack
        else:
            break

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
            objVal -= listScore[streak * -1]
        else :
            objVal += listScore[streak]

    return objVal

'''
-------------------- MINIMAX CLASS --------------------
'''
class MinimaxGroup1:
    def __init__(self, max_depth = 4):
        self.max_depth: int = max_depth

    def minimaxAlphaBeta(
        self, node: Node, depth: int, isMaximizing: bool, alpha: int, beta: int
    ):
        if not node :
            return None

        # Basis
        if node.depth == self.max_depth:
            return countObjective(node.state, isCurPlayer=False)

        # Recurence
        if isMaximizing:
            maxVal = LOSE_SCORE
            for i in range(len(node.children)):
                child = node.children[i]
                if child :
                    currVal = self.minimaxAlphaBeta(child, depth + 1, False, alpha, beta)
                    if (abs(child.value) != WIN_SCORE):
                        child.value = currVal 
                    maxVal = max(maxVal, child.value)
                    alpha = max(alpha, maxVal)
                    if alpha >= beta:
                        break
            return maxVal

        else:
            minVal = WIN_SCORE
            for i in range(len(node.children)):
                child = node.children[i]
                if child : 
                    currVal = self.minimaxAlphaBeta(child, depth + 1, True, alpha, beta)
                    if (abs(child.value) != WIN_SCORE):
                        child.value = currVal
                    minVal = min(minVal, child.value)
                    beta = min(beta, minVal)
                    if alpha >= beta:
                        break
            return minVal

    def initRoot(self, root, return_dict):
        createTree(root, self.max_depth)
        self.minimaxAlphaBeta(root, 1, True, LOSE_SCORE, WIN_SCORE)
        return_dict["root"] = root


    def find(
        self, state: State, n_player: int, thinking_time: float
    ) -> Tuple[str, str]:
        root = Node(1, state, -999, n_player)
        manager = mp.Manager()
        return_dict = manager.dict()

        p = mp.Process(target=self.initRoot, args = (root, return_dict))
        p.start()
        p.join(thinking_time)

        if p.is_alive() :
            print("Minimax algorithm is taking too long.. returning random action")
            p.kill()
            p.join()
            return (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
            
        root = return_dict["root"]
        childStateIdxToMove = 0
        bestObjVal = -999
        print("obj value depth 2 : ", end="")
        for i in range(state.board.col*2):
            if root.children[i]:
                print(str(i) + ":" + str(root.children[i].value) + " | ", end="")
            if root.children[i] and (root.children[i].value > bestObjVal): 
                bestObjVal = root.children[i].value
                childStateIdxToMove = i
        print()

        colToMove = childStateIdxToMove // 2
        if childStateIdxToMove % 2 == 0:
            shapeToMove = ShapeConstant.CROSS
        else:
            shapeToMove = ShapeConstant.CIRCLE
        return (colToMove, shapeToMove)