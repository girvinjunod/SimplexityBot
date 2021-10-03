from src.model import Piece, Board, State, Player
from src.constant import ColorConstant, ShapeConstant, GameConstant
from src.utility import is_out, place


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
        if (
            (row + cell[0] >= state.board.row or col + cell[1] < 0 or col + cell[1] >= state.board.col)
            or (state.board[row + cell[0], col + cell[1]].shape == ShapeConstant.BLANK)
        ):
            ret.append(cell)

    return ret


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


def countStreak(
    state: State,
    row: int,
    col: int,
    playerShape: ShapeConstant,
    playerColor: ColorConstant,
):
    """
    [DESC]
        Function to count cell streaks
    [PARAMS]
        state: State -> current state
        row, col: int -> current cell
    [RETURN]
        int -> streaks value
    """
    ownStreak = [0,1,4,100,1000]
    enemyStreak = [0,-1,-8,-1000,-1000]
    score = 0
    currShape = state.board[row, col].shape
    currColor = state.board[row, col].color
    # CHECK FOR EVERY EMPTY ADJACENT CELLS (FIND PERIMETER PIECES)
    for cell in getEmptyAdj(state, row, col):
        direction = (cell[0] * -1, cell[1] * -1)
        # COUNT BASED ON SHAPE
        streak = 1
        while (
            not is_out(state.board, row + (direction[0] * streak), col + (direction[1] * streak))
            and currShape
            == state.board[
                row + (direction[0] * streak), col + (direction[1] * streak)
            ].shape
        ):
            streak += 1
        
        score += (enemyStreak[min(streak,4)-1] if playerShape != currShape else ownStreak[min(streak,4)-1])

        # COUNT BASED ON COLOR
        streak = 1
        while (
            not is_out(state.board, row + (direction[0] * streak), col + (direction[1] * streak))
            and currColor
            == state.board[
                row + (direction[0] * streak), col + (direction[1] * streak)
            ].color
        ):
            streak += 1

        score += (enemyStreak[min(streak,4)-1] if playerColor != currColor else ownStreak[min(streak,4)-1])
    
    return score


def countObjective(state: State, isCurPlayer: bool = True):
    """
    [DESC]
        Function to count objective value for the state
    [PARAMS]
        state: State -> current state
    [RETURN]
        int objective value for the state
    """

    objValue = 0
    curPlayer = state.players[(state.round + (1 if isCurPlayer else 0)) % 2]

    for row in range(state.board.row):
        for col in range(state.board.col):
            if (state.board[row, col].shape != ShapeConstant.BLANK):
                objValue += countStreak(state, row, col, curPlayer.shape, curPlayer.color)

    return objValue
