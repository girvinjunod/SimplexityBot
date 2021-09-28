import copy
import time
from src.model import State,Board,Player
from src.utility import place
from src.constant import GameConstant, ShapeConstant

class Node:
    def __init__(self, depth, state: State, value) -> None:
        self.depth : int = depth
        self.state : State = state
        self.children : Node.array = []
        self.value : int = value
    
    def initChild(self) -> None:
        for i in range(self.state.board.col):
            xBoard = copy.deepcopy(self.state.board)
            xPlayers = copy.deepcopy(self.state.players)
            xState = State(xBoard, xPlayers, self.state.round+1)
            xrow = place(xState, (self.state.round+1)%2, ShapeConstant.CROSS, i)
            if (xrow >= 0):
                self.children.append(Node(self.depth+1, xState), 0) 
            else :
                self.children.append(None)
                

            oBoard = copy.deepcopy(self.state.board)
            oPlayers = copy.deepcopy(self.state.players)
            oState = State(oBoard, oPlayers, self.state.round+1)
            orow = place(oState, (self.state.round+1)%2, ShapeConstant.CIRCLE, i)
            if (orow >= 0):
                self.children.append(Node(self.depth+1, oState), 0)
            else :
                self.children.append(None)
    
    # def getLeaves(self):

def createTree(node: Node, maxDepth: int):
    if node.depth < maxDepth:
        node.initChild()
        
        for aNode in node.children:
            createTree(aNode,maxDepth)


if __name__=="__main__":
    start = time.time()
    board = Board(7, 6)
    # print(board)
    n_quota = 7*6
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
        Player(
            GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR, quota[0]
        ),
        Player(
            GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR, quota[1]
        ),
    ]
    root = Node(1, State(Board(7,6), players, 1))
    print(root.state.players[0].quota)
    createTree(root,5)
    
    # level1: Node = root.children[2]
    # level2: Node = level1.children[0]
    # level3: Node = level2.children[0]
    # print(level2.state.board)

    # print(aNode.children)
    end = time.time()
    print(end-start)
    # print(root.state.board)
        