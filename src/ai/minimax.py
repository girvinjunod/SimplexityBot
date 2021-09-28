import random
from time import time

from src.constant import ShapeConstant, GameConstant
from src.model import State
import tree

from typing import Tuple, List

class Minimax:
    def __init__(self, max_depth):
        self.max_depth : int = max_depth

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        # self.thinking_time = time() + thinking_time
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        # return best_movement
        
        # Make tree
        root = Node(1, stat)
        createTree(root, self.max_depth)
        minimaxAlphaBeta(root, 1, true, alpha, beta)
        
        childStateIdxToMove = 0
        bestObjVal = -999
        for i in range(12):
            if (root.children[i].value > bestObjVal): 
                bestObjVal = root.children[i].value
                childStateIdxToMove = i
                
        colToMove = childStateIdxToMove / 2
        if (childStateIdxToMove % 2 == 0):
            shapeToMove = ShapeConstant.CROSS
        else :
            shapeToMove = ShapeConstant.CIRCLE
        
        
        return (colToMove, shapeToMove)
    
    def max(a: int, b: int) :
        if (a >= b): 
            return a
        else: 
            return b
        
    def min(a: int, b: int) :
        if (a <= b): 
            return a
        else: 
            return b
    
    def minimaxAlphaBeta(node: Node, depth: int, isMaximizing: bool, alpha: int, beta: int) :
        if (node.depth == self.max_depth) :
            return countObjective(node.state)
        
        if (isMaximizing) :
            maxVal = -999
            for child in node.children :
                currVal = minimaxAlphaBeta(node, depth+1, false, alpha, beta)
                child.value = currVal # hapus kalau ga pake value
                maxVal = max(maxVal, currVal)
                alpha = max(alpha, maxVal)
                if (alpha >= beta):
                    break
            return maxVal
        else :
            maxVal = 999 
            for child in node.children :
                currVal = minimax(node, depth+1, true, alpha, beta)
                child.value = currVal # hapus kalau ga pake value
                maxVal = min(maxVal, currVal) 
                beta = min(beta, maxVal)
                if (alpha >= beta):
                    break
            return maxVal