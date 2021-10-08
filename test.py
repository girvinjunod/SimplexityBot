from src.model import State, Board, Player
from src.utility import place
from src.constant import GameConstant, ShapeConstant
from src.ai.objective import countObjective
from src.ai.local_search import LocalSearch

import random
import copy



def hillclimbing(state: State, n_player: int):
    # for every state, count objective, get max or min value from state, return that state
    # cek kuota
    playerquota = state.players[n_player].quota
    circle = playerquota[ShapeConstant.CIRCLE]
    cross = playerquota[ShapeConstant.CROSS]
    # isi semua kemungkinan move
    listofmoves = []
    for i in range(state.board.col):
        if cross > 0:
            listofmoves.append([i, ShapeConstant.CROSS])
        if circle > 0:
            listofmoves.append([i, ShapeConstant.CIRCLE])
    # print(listofmoves)
    listofstates = {}
    for i in range(len(listofmoves)):
        temp = copy.deepcopy(state)  # copy to temp state

        valid = place(temp, n_player, listofmoves[i][1], listofmoves[i][0])
        # print(temp.board)
        if valid != -1:
            heuristic = countObjective(temp)  # ini ganti dapet nilai heuristic brp
            listofstates[i] = heuristic

    print(listofstates)
    ronde = state.round
    if ronde % 2 == 1:
        maks = True
    else:
        maks = False

    ekstrim = listofstates[0]  # ini ganti max atau min
    ans = [
        random.randint(0, 7),
        random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]),
    ]
    if maks:
        for i in listofstates:
            value = listofstates[i]
            if value > ekstrim:
                print(value)
                ekstrim = value
                ans = listofmoves[i]
    else:
        for i in listofstates:
            value = listofstates[i]
            if value < ekstrim:
                ekstrim = value
                ans = listofmoves[i]
    print("ans",ans)
    return ans


if __name__ == "__main__":
    board = Board(6, 7)
    # print(board)
    n_quota = 7 * 6
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
    state = State(Board(6, 7), players, 1)
    place(state, 1, GameConstant.PLAYER1_SHAPE, 1)
    print(state.board)
    print(countObjective(state))
    print(state.board[3,1].shape)

    place(state, 1, GameConstant.PLAYER1_SHAPE, 1)
    print(state.board)
    print(countObjective(state))
    print(state.board[3,1].shape)

    place(state, 1, GameConstant.PLAYER1_SHAPE, 1)
    print(state.board)
    print(countObjective(state))
    print(state.board[3,1].shape)

    place(state, 0, GameConstant.PLAYER2_SHAPE, 2)
    print(state.board)
    print(countObjective(state))
    print(state.board[3,1].shape)
    
    place(state, 0, GameConstant.PLAYER2_SHAPE, 3)
    print(state.board)
    print(countObjective(state))
    print(state.board[3,1].shape)
    # print(countObjective(state))
