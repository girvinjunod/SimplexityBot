import copy
import time
from src.model import State,Board,Player
from src.utility import place, is_win
from src.constant import GameConstant, ShapeConstant

WIN_SCORE = 10000
LOSE_SCORE = -10000

class Node:
    def __init__(self, depth: int, state: State, value: int) -> None:
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
                win_condition = is_win(xState.board)

                # if (xState.round>=7 and xrow==5 and i==1):
                #     print("DIBAWAH INI PRINT", str(xState.round))
                #     print(win_condition, xState.board[xrow, i].shape)
                #     print(xState.board)

                value = 0
                if win_condition != None:
                    # print(win_condition)
                    shape, color = win_condition
                    winner =  ((self.state.players[1].shape == shape) 
                        and (self.state.players[1].color == color)) 
                    value = WIN_SCORE if winner else LOSE_SCORE
                self.children.append(Node(self.depth+1, xState, value)) 
            else :
                self.children.append(None)
                

            oBoard = copy.deepcopy(self.state.board)
            oPlayers = copy.deepcopy(self.state.players)
            oState = State(oBoard, oPlayers, self.state.round+1)
            orow = place(oState, (self.state.round+1)%2, ShapeConstant.CIRCLE, i)

            if (orow >= 0):
                win_condition = is_win(oState.board)

                # if (oState.round>=7 and orow==5 and i==1):
                #     print("DIBAWAH INI PRINT", str(oState.round))
                #     print(win_condition, oState.board[orow, i].shape)
                #     print(oState.board)
                
                value = 0
                if win_condition != None:
                    # print(win_condition)
                    shape, color = win_condition
                    winner =  ((self.state.players[1].shape == shape) 
                        and (self.state.players[1].color == color)) 
                    value = WIN_SCORE if winner else LOSE_SCORE
                self.children.append(Node(self.depth+1, xState, value)) 
            else :
                self.children.append(None)
    
    # def getLeaves(self):
    def printTree(self):
        if len(self.children)==0:
            print(self.depth*"   " + str(self.value))
        else:
            print(self.depth*"   " + str(self.value))
            # if self.value == 40:
            if (self.depth >= 2):
                for node in self.children:
                    if node :
                        node.printTree()
            else:
                self.children[11].printTree()
        

    def __str__(self) :
        res = "Depth : " + str(self.depth) + " | "
        res += "Value : " + str(self.value) + "\n"
        return res


def createTree(node: Node, maxDepth: int):
    # if abs(node.value)<1000:
    #     node.initChild()
    # current: Node = node
    # stack: Node.Array = current.children
    # n_child: int = 0
    # while True:
    #     current = stack.pop()
    #     if not current.children and current.depth < maxDepth and abs(current.value)<1000:
    #         current.initChild()
    #         stack.append(current)

    #         current = current.children[0]
    #     else:
    #         n_child += 1
    #         if (n_child < 6):
    #             current = stack.pop()
    #             current = current.children[n_child]
    #             # stack.append(current.children[n_child])
    #         else:
    #             n_child = 0
    #             current = None
    #     break

    if node and node.depth < maxDepth:
        if abs(node.value) < 10000: 
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
        