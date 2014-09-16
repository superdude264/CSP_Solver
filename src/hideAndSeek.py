import sys
from string import split
import numpy
import random
import time

def main():

    # Control Variables.
    ITER = 100
    friends = 8
    VAR_SELECTION_FUNC = selectUnassignedVariable_Random
    SHOW_DATA = True
    PRETTY_PRINT = True
    
    try:
        # for friends in range(4, 16):
        countData = []
        timeData = []
        grid = buildRandomGrid(friends)

#         print "Iter: %d" % ITER
#         print "Friends: %d" % FRIENDS
#         print "Var Selection: %s" % VAR_SELECTION_FUNC

        # for _ in range(ITER):
        t1 = time.clock()
        csp = (grid.copy(), friends)
        assignments, callCount = backtrackingSearch(csp, VAR_SELECTION_FUNC)
        t2 = time.clock()

        oneBasedAssignments = map(lambda x: (x[0] + 1, x[1] + 1), assignments)
        if SHOW_DATA:
            if PRETTY_PRINT:
                # print "Backtracks: %d" % callCount
                for assign in oneBasedAssignments:
                    print "%d %d" % assign
            else:
                print callCount, oneBasedAssignments

        countData.append(callCount)
        timeData.append(t2 - t1)

#         print "Backtrack Mean: %f" % numpy.mean(countData)
#         print "Backtrack Variance: %f" % numpy.var(countData)
#         print "Time Mean (s): %f" % numpy.mean(timeData)
#         print "Time Variance: %f" % numpy.var(timeData)

        # print "%d,%f,%f,%f,%f" % (friends, numpy.mean(countData), numpy.var(countData), numpy.mean(timeData), numpy.var(timeData))

        return 0
    except Exception as e:
        print e
        return 5

def backtrackingSearch(csp, varSelectionFunc):
    grid, reqAssignments = csp
    assignments = []
    callCount = 0

    for tilePos in varSelectionFunc(csp):
        x, y = tilePos
        callCount = callCount + 1

        # Check completeness.
        if len(assignments) == reqAssignments:
            return (assignments, callCount)

        # Assign value.
        if grid[x][y] == 0:
            grid[x][y] = 1
            assignments.append(tilePos)

        # Check consistency.
        if not isConsistent(csp, tilePos):
            grid[x][y] = 0
            assignments.remove(tilePos)

def selectUnassignedVariable_Iterative(csp):
    grid = csp[0]
    for x, row in enumerate(csp[0]):
        for y, col in enumerate(row):
            tileVal = grid[x][y]
            if tileVal == 0: yield (x, y)

def selectUnassignedVariable_Random(csp):
    grid, n = csp
    while True:
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        tileVal = grid[x][y]
        if tileVal == 0: yield (x, y)

def isConsistent(csp, var):
    grid = csp[0]
    x, y = var
    if not isAxisConsistent(grid[x]): return False
    if not isAxisConsistent(grid[:, y]): return False
    return True

def isAxisConsistent(axisTiles):
    peopleInSight = 0
    for tileVal in axisTiles:
        if tileVal > 0: peopleInSight = peopleInSight + 1
        if tileVal < 0: peopleInSight = 0
        if peopleInSight >= 2:
            return False
    return True

def buildCspFromFile():
    fileName = sys.argv[1]
    lines = [line.strip() for line in open(fileName)]
    numFriends = int(split(lines[0])[0])
    lines.pop(0)

    grid = numpy.zeros(numFriends ** 2).reshape((numFriends, numFriends))
    for line in lines:
        x, y = map(int, split(line))
        grid[x - 1][y - 1] = -1

    return (grid, numFriends)

# Builds an N x N grid w/ 2N-1 trees, where N is the number of friends.
def buildRandomGrid(numFriends):
    grid = numpy.zeros(numFriends ** 2).reshape((numFriends, numFriends))
    
    treeCount = 0
    while treeCount < 2 * numFriends - 1:
        x = random.randint(0, numFriends - 1)
        y = random.randint(0, numFriends - 1)
        if grid[x][y] == 0:
            grid[x][y] = -1
            treeCount = treeCount + 1
    
    return grid

if __name__ == "__main__":
    sys.exit(main())
