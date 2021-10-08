import random
from time import time

from src.constant import ShapeConstant, GameConstant
from src.utility import place, is_win
from src.model import State, Board, Player
from src.ai.tree import Node, createTree

from src.ai.objective import countObjective

from typing import Tuple, List


class Minimax:
    def __init__(self, max_depth = 3):
        self.max_depth: int = max_depth

    def minimaxAlphaBeta(
        self, node: Node, depth: int, isMaximizing: bool, alpha: int, beta: int
    ):
        if not node :
            return None

        #Kalo ketemu daun
        if node.depth == self.max_depth:
            return countObjective(node.state, True) #musuh

        if isMaximizing:
            maxVal = -9999
            for child in node.children:
                if child : # check if not null
                    currVal = self.minimaxAlphaBeta(child, depth + 1, False, alpha, beta)
                    child.value = currVal 
                    if (abs(currVal) >= 500) :
                        break
                    maxVal = max(maxVal, currVal)
                    alpha = max(alpha, maxVal)
                    if alpha >= beta:
                        break
            return maxVal
        else:
            minVal = 9999
            for child in node.children:
                if child : 
                    currVal = self.minimaxAlphaBeta(child, depth + 1, True, alpha, beta)
                    child.value = currVal 
                    if (currVal <= -500) :
                        break
                    minVal = min(minVal, currVal)
                    beta = min(beta, minVal)
                    if alpha >= beta:
                        break
            return minVal

    def find(
        self, state: State, n_player: int, thinking_time: float
    ) -> Tuple[str, str]:
        # self.thinking_time = time() + thinking_time
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        # return best_movement

        # print(state.board)

        # Make tree
        root = Node(1, state, -999)
        createTree(root, self.max_depth)
        self.minimaxAlphaBeta(root, 1, True, -999, 999)

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

        # print("chosen state : " + str(childStateIdxToMove))
        colToMove = childStateIdxToMove // 2
        if childStateIdxToMove % 2 == 0:
            shapeToMove = ShapeConstant.CROSS
        else:
            shapeToMove = ShapeConstant.CIRCLE
        
        if (state.round == 22) :
            root.printTree()

        # root.printTree()
        return (colToMove, shapeToMove)