import random
import multiprocessing as mp
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
    def __init__(self, max_depth = 4):
        self.max_depth: int = max_depth

    def minimaxAlphaBeta(
        self, node: Node, depth: int, isMaximizing: bool, alpha: int, beta: int
    ):
        if not node :
            return None

        # Basis
        if node.depth == self.max_depth:
            return countObjective(node.state, True)

        # Recurence
        if isMaximizing:
            maxVal = LOSE_SCORE
            for child in node.children:
                if child :
                    currVal = self.minimaxAlphaBeta(child, depth + 1, False, alpha, beta)
                    if (abs(child.value) != 10000):
                        child.value = currVal 
                    maxVal = max(maxVal, child.value)
                    alpha = max(alpha, maxVal)
                    if alpha >= beta:
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
                        break
            return minVal

    def initRoot(self, root, return_dict):
        createTree(root, self.max_depth)
        self.minimaxAlphaBeta(root, 1, True, LOSE_SCORE, WIN_SCORE)
        return_dict["root"] = root


    def find(
        self, state: State, n_player: int, thinking_time: float
    ) -> Tuple[str, str]:

        root = Node(1, state, -999)
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
        # print("obj value depth 2 : ", end="")
        for i in range(state.board.col*2):
            # if root.children[i]:
            #     print(str(i) + ":" + str(root.children[i].value) + " | ", end="")
            if root.children[i] and (root.children[i].value > bestObjVal): 
                bestObjVal = root.children[i].value
                childStateIdxToMove = i
        # print()

        colToMove = childStateIdxToMove // 2
        if childStateIdxToMove % 2 == 0:
            shapeToMove = ShapeConstant.CROSS
        else:
            shapeToMove = ShapeConstant.CIRCLE
        return (colToMove, shapeToMove)