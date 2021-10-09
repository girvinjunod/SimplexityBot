from src.model import Piece, Board, State, Player
from src.constant import ColorConstant, ShapeConstant, GameConstant
from src.utility import is_out, place

# def getEmptyAdj(state: State, row: int, col: int):
#     """
#     [DESC]
#         Funtion to get empty adjacent cells
#     [PARAMS]
#         state : State -> current state
#         row, col : int -> current cell
#     [RETURN]
#         Array of Tuple[row, col]: adjacent cells direction
#     """
#     adj_cell = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
#     ret = []

#     for cell in adj_cell:
#         if (
#             (row + cell[0] >= state.board.row or col + cell[1] < 0 or col + cell[1] >= state.board.col)
#             or (state.board[row + cell[0], col + cell[1]].shape == ShapeConstant.BLANK)
#         ):
#             ret.append(cell)

#    return ret

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
    curPlayer = state.players[(state.round + (1 if isCurPlayer else 0)) % 2]
    enemyPlayer = state.players[(state.round + (0 if isCurPlayer else 1)) % 2]

    objVal = 0
    listStreak = []

    for col in range(state.board.col) :
        # Initiating list row idx
        listRowIdx = []
        for row in range(state.board.row-1,-1,-1) :
            if state.board[row,col].shape != ShapeConstant.BLANK :
                ret = getEmptyAdj(state, row, col)
                if ret :
                    listRowIdx.append(row)
        
        # Counting Streak
        for rowIdx in listRowIdx :
            tmpAdjCell = getEmptyAdj(state, rowIdx, col)
            for cell in tmpAdjCell :
                # Streak count on shape
                streak = 1
                tmpRow = rowIdx
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
                tmpRow = rowIdx
                tmpCol = col
                while True :
                    try :
                        if state.board[tmpRow, tmpCol].color == curPlayer.color :
                            multiplier = 1
                        elif state.baord[tmpRow, tmpCol].color == enemyPlayer.color :
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

# def getTopRow(state, col):
#     """
#     [DESC]
#         Function to get index of top row
#     [PARAMS]
#         state : State -> current state
#         col : Int -> column to get top row
#     [RETURN]
#         int : index of top row of col
#     """
    
#     if state.board[0, col].shape == ShapeConstant.BLANK:
#         return 0

#     idx = 1
#     while state.board.board[idx + 1][col].shape != ShapeConstant.BLANK:
#         idx += 1
#         if idx == state.board.row - 1:
#             return -1

#     return idx


# def countStreak(
#     state: State,
#     row: int,
#     col: int,
#     playerShape: ShapeConstant,
#     playerColor: ColorConstant,
# ):
#     """
#     [DESC]
#         Function to count cell streaks
#     [PARAMS]
#         state: State -> current state
#         row, col: int -> current cell
#     [RETURN]
#         int -> streaks value
#     """
#     ownStreak = [0,1,4,100,1000]
#     enemyStreak = [0,-1,-1000,-1000,-1000]
#     score = 0
#     currShape = state.board[row, col].shape
#     currColor = state.board[row, col].color

#     # CHECK FOR EVERY EMPTY ADJACENT CELLS (FIND PERIMETER PIECES)
#     for cell in getEmptyAdj(state, row, col):
#         direction = (cell[0] * -1, cell[1] * -1)
#         # COUNT BASED ON SHAPE
#         streak = 1
#         while (
#             not is_out(state.board, row + (direction[0] * streak), col + (direction[1] * streak))
#             and currShape
#             == state.board[
#                 row + (direction[0] * streak), col + (direction[1] * streak)
#             ].shape
#         ):
#             streak += 1
        
#         score += (enemyStreak[min(streak,4)-1] if playerShape != currShape else ownStreak[min(streak,4)-1])

#         # COUNT BASED ON COLOR
#         streak = 1
#         while (
#             not is_out(state.board, row + (direction[0] * streak), col + (direction[1] * streak))
#             and currColor
#             == state.board[
#                 row + (direction[0] * streak), col + (direction[1] * streak)
#             ].color
#         ):
#             streak += 1

#         score += (enemyStreak[min(streak,4)-1] if playerColor != currColor else ownStreak[min(streak,4)-1])
    
#     return score


# def countObjective(state: State, isCurPlayer: bool = True):
#     """
#     [DESC]
#         Function to count objective value for the state
#     [PARAMS]
#         state: State -> current state
#     [RETURN]
#         int objective value for the state
#     """

#     objValue = 0
#     curPlayer = state.players[(state.round + (1 if isCurPlayer else 0)) % 2]

#     for row in range(state.board.row):
#         for col in range(state.board.col):
#             if (state.board[row, col].shape != ShapeConstant.BLANK):
#                 objValue += countStreak(state, row, col, curPlayer.shape, curPlayer.color)

#     return objValue
