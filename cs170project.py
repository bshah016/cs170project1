
#define your solution states here
EIGHT = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
FIFTEEN = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
FIFTEEN = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]]


def main():
    choice = 5
    problem = []
    while choice != 0:
        print("Welcome to my 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own, or 0 to quit")
        choice = int( input() )
        if choice == 1:
            problem = [1, 2, 3, 4, 5, 6, 0, 7, 8]
        elif choice == 2:
            print("Enter your puzzle, using a zero to represent the blank.")
            print("Please only enter valid 8-puzzles.")
            print("Enter the puzzle demilimiting the numbers with a space. (0 indicates the blank space)")
            print("Type RETURN only when finished with the row.")

            firstRow = input(print("First Row:"))
            secondRow = input(print("Second Row:"))
            thirdRow = input(print("Third Row:"))

            firstRow.split(' ')
            secondRow.split(' ')
            thirdRow.split(' ')

            problem = [firstRow, secondRow, thirdRow]

        else:
            print("Please enter a valid choice")

    algNum = input(print("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhattan Distance Heuristic"))
    qfunct = int( algNum )
    generalsearch(problem, qfunct)

def generalsearch(problem, qfunct):

    while goal(problem) == False:
        if qfunct == 1:
            problem = misplaced(problem)
        if (qfunct == 2):
            problem = manhattan(problem)
        if qfunct == 0:
            problem = uniform(problem)
        print(problem)
        if goal(problem):
            print("Goal state found!")

def manhattan(problem):
    goalstate = EIGHT #choose your goal state from the global variables
    manhattandist = 0
    x = 0
    y = 0
    goal_x = 0
    goal_y = 0

    #took inspiration from: https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/
    #calculating current position for each value, then retrieving goal state's value
    #using the formula from the link, adds the abs value of actual - expected for each x and y coordinate
    #re sums that into the manhattan distance calculation
    for a in range(1, 9): #have to change this range if you change the type of puzzle. For 15 puzzle, would have to be 1 to 16, for 24 puzzle, would have to be 1 to 25, etc
        for i in range(len(problem)):
            for j in range(len(problem)):
                if problem[i][j] == a:
                    x = i
                    y = j
                if goalstate[i][j] == a:
                    goal_x = i
                    goal_y = j

        manhattandist = manhattandist + abs(x - goal_x) + abs(y - goal_y)
    return manhattandist


def misplaced(problem):
    goalstate = EIGHT #choose your goal state from the global variables
    num_misplaced = 0

    for i in range(len(problem)):
        for j in range(len(problem)):
            if problem[i][j] != goalstate [i][j] and problem[i][j] != 0:
                num_misplaced = num_misplaced + 1
    return num_misplaced
    

def goal(problem):
    goalstate = EIGHT #change this depending on what type of puzzle you have
    if problem == goalstate:
        return True
    else:
        return False

    


main()


    
