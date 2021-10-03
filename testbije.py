import random
import time

from src.constant import ShapeConstant, GameConstant
from src.utility import place
from src.model import State, Board, Player
from src.ai.tree import Node, createTree

from src.ai.objective import countObjective

from typing import Tuple, List


class Minimax:
    def __init__(self, max_depth = 4):
        self.max_depth: int = max_depth

    def minimaxAlphaBeta(
        self, node: Node, depth: int, isMaximizing: bool, alpha: int, beta: int
    ):
        if not node :
            return None

        #Kalo ketemu daun
        if node.depth == self.max_depth:
            return countObjective(node.state, False) #musuh

        if isMaximizing:
            maxVal = -999
            for child in node.children:
                if child : # check if not null
                    currVal = self.minimaxAlphaBeta(child, depth + 1, False, alpha, beta)
                    child.value = currVal 
                    maxVal = max(maxVal, currVal)
                    alpha = max(alpha, maxVal)
                    if alpha >= beta:
                        break
            return maxVal
        else:
            minVal = 999
            for child in node.children:
                if child : 
                    currVal = self.minimaxAlphaBeta(child, depth + 1, True, alpha, beta)
                    child.value = currVal 
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
        start = time.time()

        # print(state.board)

        # Make tree
        root = Node(1, state, -999)
        createTree(root, self.max_depth)
        self.minimaxAlphaBeta(root, 1, True, -999, 999)

        childStateIdxToMove = 0
        bestObjVal = -999
        for i in range(14):
            if root.children[i] and (root.children[i].value > bestObjVal): 
                bestObjVal = root.children[i].value
                childStateIdxToMove = i

        print("chosen state : " + str(childStateIdxToMove))
        colToMove = childStateIdxToMove // 2
        if childStateIdxToMove % 2 == 0:
            shapeToMove = ShapeConstant.CROSS
        else:
            shapeToMove = ShapeConstant.CIRCLE
        
        # root.printTree()
        end = time.time()
        print(end - start)
        return (colToMove, shapeToMove)


if __name__ == "__main__":
    algo = Minimax(5)

    board = Board(6,7)
    # print(board)
    n_quota = 6*7
    quota = [
        {
            ShapeConstant.CROSS: n_quota // 2,
            ShapeConstant.CIRCLE: n_quota - (n_quota // 2),
        },
        {
            ShapeConstant.CROSS: n_quota - (n_quota // 2),
            ShapeConstant.CIRCLE: n_quota // 2,
        },
    ]
    players = [
        Player(GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR, quota[0]),
        Player(GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR, quota[1]),
    ]
    print(players[0].shape, players[0].color)
    state = State(board, players, 1)
    place(state, 0, GameConstant.PLAYER2_SHAPE, 1)
    place(state, 1, GameConstant.PLAYER1_SHAPE, 0)
    place(state, 0, GameConstant.PLAYER2_SHAPE, 1)
    place(state, 1, GameConstant.PLAYER1_SHAPE, 0)
    root = Node(1,state,0)

    # print(state.board)

    createTree(root, 3)

    # algo.minimaxAlphaBeta(root, 1, True, -999, 999)
    print(algo.find(state, 0, 5))
    # print("root: " + str(root))
    # for nodeC in root.children :
    #     if nodeC:
    #         print("Layer 2 : " + str(nodeC))
    #         for nodeX in nodeC.children :
    #             if nodeX :
    #                 print("Layer 3 : " + str(nodeX))
    #         print()
