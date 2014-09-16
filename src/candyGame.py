import sys
import numpy
from copy import deepcopy
import time

DEPTH_LIMIT = 2
AB_DEPTH_LIMIT = 3

g_BlueNodesExpanded = 0
g_GreenNodesExpanded = 0

def main():
    try:
        for fileName in ["AlmondJoy", "Ayds", "Bit-O-Honey", "Mounds", "ReesesPieces"]:
            board = buildBoard(fileName + ".txt")
            state = State(board, Player.BLUE)

            print
            print "==== %s %s vs. %s ====" % (fileName, "AB", "AB")
            print
            print state.board
            print

            blueMoveCount = 0
            blueTime = 0.0

            greenMoveCount = 0
            greenTime = 0.0

            while True:
                # Blue
                t1 = time.clock()
                blueMove = AB_SEARCH_BLUE(state)
                # blueMove = MINIMAX_DECISION_BLUE(state)
                t2 = time.clock()

                state = RESULT(state, blueMove)
                blueMoveCount += 1
                blueTime += (t2 - t1)
                print "Blue: %s" % blueMove

                if gameOver(state): break

                # Green
                t1 = time.clock()
                greenMove = AB_SEARCH_GREEN(state)
                # greenMove = MINIMAX_DECISION_GREEN(state)
                t2 = time.clock()

                state = RESULT(state, greenMove)
                greenMoveCount += 1
                greenTime += (t2 - t1)
                print "Green: %s" % greenMove

                if gameOver(state): break

            print
            print state.board
            print
            print "Blue:"
            print "\t Points: %d" % totalPoints(state, Player.BLUE)
            print "\t Nodes: %d" % g_BlueNodesExpanded
            print "\t Avg Nodes/Move: %f" % (g_BlueNodesExpanded / blueMoveCount)
            print "\t Avg Time/Move (s): %f" % (blueTime / blueMoveCount)
            print "Green:"
            print "\t Points: %d" % totalPoints(state, Player.GREEN)
            print "\t Nodes: %d" % g_GreenNodesExpanded
            print "\t Avg Nodes/Move: %f" % (g_GreenNodesExpanded / greenMoveCount)
            print "\t Avg Time/Move (s): %f" % (greenTime / greenMoveCount)
            print
    except Exception as e:
        print e
        return 5

def totalPoints(state, player):
    points = 0
    for _ , tile in numpy.ndenumerate(state.board):
        if tile.owner == player: points += tile.points
    return points

def gameOver(state):
    for _ , tile in numpy.ndenumerate(state.board):
        if tile.owner == Player.NONE: return False
    return True

def AB_SEARCH_BLUE(state):  # Returns an action.
    a = AB_MAX_VALUE(state, 0, -1000, 1000)[1]
    return a

def AB_SEARCH_GREEN(state):  # Returns an action.
    a = AB_MIN_VALUE(state, 0, -1000, 1000)[1]
    return a

def AB_MAX_VALUE(state, depth, alpha, beta):  # Returns a utility value.
    global g_BlueNodesExpanded
    g_BlueNodesExpanded += 1

    if AB_CUTOFF_TEST(state, depth): return (EVAL(state), None)
    v = -1000
    action = None
    for a in ACTIONS(state):
        # v = max(v, AB_MIN_VALUE(RESULT(state, a), depth + 1, alpha, beta))
        maybeV = AB_MIN_VALUE(RESULT(state, a), depth + 1, alpha, beta)[0]
        if maybeV > v:
            v = maybeV
            action = a
        if v >= beta: 
            return (v, a)
        alpha = max(alpha, v)
    return (v, action)

def AB_MIN_VALUE(state, depth, alpha, beta):  # Returns a utility value.
    global g_GreenNodesExpanded
    g_GreenNodesExpanded += 1

    if AB_CUTOFF_TEST(state, depth): return (EVAL(state), None)
    v = 1000
    action = None
    for a in ACTIONS(state):
        # v = min(v, AB_MAX_VALUE(RESULT(state, a), depth + 1, alpha, beta))
        maybeV = AB_MAX_VALUE(RESULT(state, a), depth + 1, alpha, beta)[0]
        if maybeV < v:
            v = maybeV
            action = a
        if v <= alpha: 
            return (v, a)
        beta = min(beta, v)
    return (v, action)

def AB_CUTOFF_TEST(state, depth):
    return depth >= AB_DEPTH_LIMIT or ACTIONS(state) == []

def MINIMAX_DECISION_BLUE(state):  # Returns an action.
    result = None
    resultVal = -1000
    for a in ACTIONS(state):
        val = MIN_VALUE(RESULT(state, a), 0)
        if val > resultVal:
            result = a
            resultVal = val

    return result

def MINIMAX_DECISION_GREEN(state): # Returns an action.
    result = None
    resultVal = 1000
    for a in ACTIONS(state):
        val = MAX_VALUE(RESULT(state, a), 0)
        if val < resultVal:
            result = a
            resultVal = val

    return result

def MAX_VALUE(state, depth):  # Returns a utility value.
    global g_BlueNodesExpanded
    g_BlueNodesExpanded += 1

    if CUTOFF_TEST(state, depth): return EVAL(state)
    v = -1000
    for a in ACTIONS(state):
        v = max(v, MIN_VALUE(RESULT(state, a), depth + 1))
    return v

def MIN_VALUE(state, depth):  # Returns a utility value.
    global g_GreenNodesExpanded
    g_GreenNodesExpanded += 1

    if CUTOFF_TEST(state, depth): return EVAL(state)
    v = 1000
    for a in ACTIONS(state):
        v = min(v, MAX_VALUE(RESULT(state, a), depth + 1))
    return v

def CUTOFF_TEST(state, depth):
    return depth >= DEPTH_LIMIT or ACTIONS(state) == []

def EVAL(state):
    blueVal = 0
    greenVal = 0
    for _ , tile in numpy.ndenumerate(state.board):
        if tile.owner == Player.BLUE: blueVal += tile.points
        elif tile.owner == Player.GREEN: greenVal += tile.points
    utility = blueVal - greenVal
    return utility

def ACTIONS(state):  # Returns the legal moves in a state.
    legalMoves = []
    for (i, j) , tile in numpy.ndenumerate(state.board):
        if tile.owner == Player.NONE:
            legalMoves.append(Action(i, j))
    return legalMoves

def RESULT(state, action):  # Returns the state after a move has been made.
    newState = deepcopy(state)
    board = newState.board
    player = newState.player
    i, j = action.row, action.col

    right = (i + 1, j)
    left = (i - 1, j)
    above = (i, j + 1)
    below = (i, j - 1)

    # The tile and possibly those right, left, above, & below it.
    board[i][j].owner = player
    if canCapture(newState, right): capture(newState, right)
    if canCapture(newState, left): capture(newState, left)
    if canCapture(newState, above): capture(newState, above)
    if canCapture(newState, below): capture(newState, below)

    # Switch players.
    newState.player = -player

    return newState

def capture(state, pos):
    row, col = pos
    state.board[row][col].owner = state.player

def canCapture(state, pos):  # Returns true if the tile specified by the position can be captured.
    board = state.board
    capturingPlayer = state.player
    row, col = pos
    if row in range(6) and col in range(6):
        tileOwner = board[row][col].owner
        if tileOwner == -capturingPlayer:
            return True
    return False

def buildBoard(fileName):
    points = numpy.loadtxt(fileName, dtype = int)
    vTile = numpy.vectorize(Tile)
    board = numpy.empty((6, 6), dtype = object)
    board[:, :] = vTile(points)
    return board

class Player:
    BLUE = 1
    GREEN = -1
    NONE = 0

    @staticmethod
    def getName(player):
        playerName = ""
        if player == Player.BLUE: playerName = 'Blue'
        elif player == Player.GREEN: playerName = 'Green'
        return playerName

class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def __str__(self):
        playerName = Player.getName(self.player)
        return "%s\nPlayer: %s\n" % (self.board, playerName)

    def __repr__(self):
        return self.__str__()

class Action:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "(%d, %d)" % (self.row, self.col)

    def __repr__(self):
        return self.__str__()

class Tile:
    def __init__(self, points):
        self.points = points
        self.owner = Player.NONE

    def __str__(self):
        colorName = "_"
        if self.owner == Player.BLUE: colorName = 'B'
        elif self.owner == Player.GREEN: colorName = 'G'
        return "<%02d, %s>" % (self.points, colorName)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    sys.exit(main())
