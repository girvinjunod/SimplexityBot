import random
from time import time

from src.constant import ShapeConstant, GameConstant
from src.utility import place, check_streak
from src.model import State, Board, Player
from src.ai.tree import Node, createTree

from src.ai.objective import countObjective

from typing import Tuple, List


WIN_SCORE = 10000
LOSE_SCORE = -10000

class Minimax:
    def __init__(self, max_depth = 5):
        self.max_depth: int = max_depth

    def minimaxAlphaBeta(
        self, node: Node, depth: int, isMaximizing: bool, alpha: int, beta: int
    ):
        if not node :
            return None

        #Kalo ketemu daun
        if node.depth == self.max_depth: #BASIS
            return countObjective(node.state, True) # musuh

        #REKURENS
        if isMaximizing:
            maxVal = LOSE_SCORE

            for child in node.children:
                if child : # check if not null
                    currVal = self.minimaxAlphaBeta(child, depth + 1, False, alpha, beta)
                    if (abs(child.value) != 10000):
                        child.value = currVal 
                    maxVal = max(maxVal, child.value)
                    alpha = max(alpha, maxVal)
                    if alpha >= beta:
                        # maxVal = WIN_SCORE
                        break
            return maxVal
        else:
            minVal = WIN_SCORE

            for child in node.children:
                if child : 
                    currVal = self.minimaxAlphaBeta(child, depth + 1, True, alpha, beta)
                    if (abs(child.value) != 10000):
                        child.value = currVal
                    minVal = min(minVal, child.value)
                    beta = min(beta, minVal)
                    if alpha >= beta:
                        # minVal = LOSE_SCORE
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
        createTree(root, 5)
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
        
        # if (state.round == 6) :
        #     print("print tree :")
        #     root.printTree()

        # root.printTree()
        return (colToMove, shapeToMove)