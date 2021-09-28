from src.model import Piece, Board, State
from src.constant import ShapeConstant, GameConstant

def isRowEmpty(state, row):
    for i in range(state.board.col):
        if state.board[row,i] != ShapeConstant.BLANK:
            return False

    return True

def getTopRow(state, col) :
    '''
    [DESC]
        Function to get index of top row
    [PARAMS]
        state : State -> current state
        col : Int -> column to get top row
    [RETURN]
        int : index of top row of col
    '''
    
    if state.board[0, col] == ShapeConstant.BLANK:
        return 0    

    idx = 1
    while state.board[idx+1, col] != ShapeConstant.BLANK:
        idx += 1
        if (idx == state.board.row-1) :
            return -1    
    
    return idx
    
def getLeftCol(state, row) :
    '''
    [DESC]
        Function to get index of left column
    [PARAMS]
        state : State -> current state
        col : Int -> row to get left column
    [RETURN]
        int : index of left col of row
    '''
    if state.board[0][row] != ShapeConstant.BLANK:
        return 0
    elif isRowEmpty(state, row):
        return None
    
    idx = 0
    while state.board[idx][idx+1] != ShapeConstant.BLANK:
        idx += 1
    
    return idx
    
# streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
def countObjective(state: State):
        '''
        [DESC]
            Function to count objective value for the state
        [PARAMS]
            state: State -> current state
        [RETURN]
            int objective value for the state
        '''
        
        currScore = 0
        tempStreakCount = 1
        currRow = 0

        for col in range(state.board.col):
            #Count based on shape (CIRCLE)
            if state.board[currRow, col] == ShapeConstant.CIRCLE:
                # LOOP ROWS IN COLUMN TO FIND PIECE ON PERIMETER
                while state.board[currRow+1, col] != ShapeConstant.BLANK:
                    if (col == 0 and state.board[currRow + 1][col+1] == ShapeConstant.BLANK) or state.board[currRow][col-1] == ShapeConstant.BLANK or state.board[currRow+1][col].shape == ShapeConstant.BLANK or state.board[currRow][col+1].shape == ShapeConstant.BLANK or state.board[currRow-1][col-1].shape == ShapeConstant.BLANK or state.board[currRow-1][col+1].shape == ShapeConstant.BLANK :
                        #COUNT STREAK
                        #VERTICAL
                        while state.board[currRow-tempStreakCount][col] == ShapeConstant.CIRCLE :
                            currScore += 1
                            tempStreakCount += 1
                        tempStreakCount = 1
                        #DIAGONAL LOWER LEFT
                        while state.board[currRow-tempStreakCount][col-tempStreakCount] == ShapeConstant.CIRCLE :
                            currScore += 1
                            tempStreakCount += 1
                        tempStreakCount = 1
                        #DIAGONAL LOWER RIGHT
                        while state.board[currRow+tempStreakCount][col+tempStreakCount] == ShapeConstant.CIRCLE :
                            currScore += 1
                            tempStreakCount += 1
                        tempStreakCount = 1
                        #HORIZONTAL
                        while state.board[currRow][col+tempStreakCount] == ShapeConstant.CIRCLE :
                            currScore += 1
                            tempStreakCount += 1
                        tempStreakCount = 1
                
            None

        return 0