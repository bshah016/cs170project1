#https://docs.python.org/3/howto/sorting.html
#https://docs.python.org/3/library/functions.html#zip
#^ Used these as a reference, but they didn't seem too useful compared to what I found on stack overflow
#https://www.geeksforgeeks.org/python-program-for-heap-sort/
#^ Tried to use this to sort the nodes list so the nodes list could be sorted based off of the combo of h(n) and g(n), but again, didn't really work

#define your solution states here
import queue
import copy
import collections
from shutil import move
#https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b
import pyfiglet
#https://pypi.org/project/termcolor/
from termcolor import colored
from datetime import datetime

#global variables for the goal states
ZERO = []
EIGHT = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
FIFTEEN = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
TFOUR = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]]

SAMPLE_EIGHT = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
SAMPLE_FIFTEEN = [[0, 1, 2, 3], [5, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]]
SAMPLE_TFOUR = [[14, 5, 9, 2, 18], [8, 23, 19, 12, 17], [15, 0, 10, 20, 4], [6, 11, 21, 1, 7], [24, 3, 16, 22, 13]]


INVALID_EIGHT = [[1, 2, 3], [4, 0, 5], [6, 8, 7]]


PUZZLE_TYPE = ZERO
PROBLEM = ZERO

#global variable for the number of nodes expanded, so we can reference it later on
NUM_NODES = 0



#A lot of this code is similar to the interface given in the assignment pdf
# I tried to make it more unique by addings ome custom styling and whatnot
# But as far as the way the starting of the puzzle is concerned,
# I give credit to Eamonn Keogh (and if it's a real example, the person that wrote the report)
# for the print statements and my inspiration for them in main()
def main():
    global SAMPLE_EIGHT
    global SAMPLE_FIFTEEN
    global SAMPLE_TFOUR
    choice = 4
    problem = []

    # result = pyfiglet.figlet_format("My  8\nPuzzle\nSolver", font = "doh", width = 5000)
    print("Welcome To:")
    result = pyfiglet.figlet_format("My  N", font = "banner3-D")
    print(colored(result, 'blue'))
    result = pyfiglet.figlet_format("Puzzle", font = "banner3-D")
    print(colored(result, 'green'))
    result = pyfiglet.figlet_format("Solver", font = "banner3-D")
    print(colored(result, 'yellow'))
    result = pyfiglet.figlet_format(":-)", font = "banner3-D")
    print(colored(result, 'cyan'))
    print("By: Brij Shah")
    #     print(""" By: Brij Shah
    #          ______
    #        /|_||_\`.__
    #       (   _    _ _/
    #    ====`-(_)--(_)-'
        
    #     """)

    while choice != 0:
        global PUZZLE_TYPE
        global ZERO
        global EIGHT
        global FIFTEEN
        global TFOUR
        global PROBLEM
        global SOLUTION
        while PUZZLE_TYPE == ZERO:
            print("\nType: \n(1) to use a 8 puzzle \n(2) to use a 15 puzzle \n(3) to use a 24 puzzle\nChoice: ")
            puzzle_type = input()
            puzzle_type = int(  puzzle_type )
            if puzzle_type == 1:
                PUZZLE_TYPE = EIGHT
                PROBLEM = SAMPLE_EIGHT
            elif puzzle_type == 2:
                PUZZLE_TYPE = FIFTEEN
                PROBLEM = SAMPLE_FIFTEEN
            elif puzzle_type == 3:
                PUZZLE_TYPE = TFOUR
                PROBLEM = SAMPLE_TFOUR
            else:
                print('Please enter a valid choice\n')
                PUZZLE_TYPE = ZERO
        print("\nType: \n(1) to use a default puzzle \n(2) to create your own \n(0) to quit\nChoice: ")
        choice = input()
        choice = int( choice )
        if choice == 1:
            problem = PROBLEM #just change this to one of the sample puzzles above for higher order puzzles
            choice = 0
        elif choice == 2:
            if PUZZLE_TYPE == EIGHT:
                problem = printMenuEight()
            elif PUZZLE_TYPE == FIFTEEN:
                problem = printMenuFift()
            elif PUZZLE_TYPE == TFOUR:
                problem = printMenuTf()
            choice = 0
        else:
            print("*** Please enter a valid choice!! ***")

    # print(problem)
    print("Select algorithm. \n (1) Uniform Cost Search \n (2) Misplaced Tile Heuristic \n (3) Manhattan Distance Heuristic\n (4) Linear Conflict\nChoice: ")
    algNum = input()
    qfunct = int( algNum )
    generalsearch(problem, qfunct)

#most of the code here was inspired by the starter code given on the first page of the pdf, but I did do some things differently
#for instance, if we do reach a goal, we do not return node, instead we print out node's info, as I think that is more useful
# It also seemed that in expanded, we wanted to update the node count and parent node accordingly,
# but I couldn't figure out how to do that, so I just did it using a new children array, then iterated through that
def generalsearch(problem, qfunct):
    global NUM_NODES
    global PUZZLE_TYPE
    NUM_NODES = 0
    hn = 0

    makenode = make_node(problem)
    nodes = make_queue(makenode)
    visited = make_queue(makenode)
    nodenum = 0
    queue = 1
    max_queue = 1
    #for the timestamps used here and in the goal state code block, I used:
    # https://pynative.com/python-get-time-difference/
    #and
    # https://www.geeksforgeeks.org/get-current-timestamp-using-python/
    first = datetime.now()
    while True:
        #https://www.geeksforgeeks.org/get-current-timestamp-using-python/
        #^Used this to figure out how to get time stamps for duration of program
        #this was a problem for the NUM_NODES, used this link to help me out with sorting the vector:
        #to show that i didn't just copy it and I do understand it, I'll explain it here:
        #when you zip the two lists, they get merged into a list of tuples. 
        #so for example, {1, 2, 3} and {'a', 'b', 'c'} zipped would become {{1, a}, {2, b}, {3, c}}
        #then, it creates a new resulting array based on the zipped array
        #this new array that is stored, is then separated and then now the nodes array is stored properly.
        #https://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        if qfunct == 2 or qfunct == 3: #not Uniform cost search
            weights = []
            for newnode in nodes:
                weight = newnode.depth + newnode.hn
                weights.append(weight)
            nodes = [x for _, x in sorted(zip(weights, nodes), key=lambda pair: pair[0])]

        if len(nodes) == 0:
            print("Failure\n")
            return
        nodenum += 1
        node = nodes[0]
        # used this for some help on how to do this:
        # https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index
        nodes.pop(0)
        queue -= 1
        if goal_test(node):
            second = datetime.now()
            time = second - first
            print('State to expand has a g(n) of ' + str(node.depth) + ', an h(n) of ' + str(node.hn) + '.\n And it looks like: \n')
            if PUZZLE_TYPE == EIGHT:
                drawBoardEight(node.problem)
            elif PUZZLE_TYPE == FIFTEEN:
                drawBoardFift(node.problem)
            elif PUZZLE_TYPE == TFOUR:
                drawBoardTf(node.problem) #!!!
            print('\nTotal number of nodes expanded: ' + str(NUM_NODES))
            print('Depth of the node in the tree was: ' + str(node.depth))
            #https://stackoverflow.com/questions/4362491/how-do-i-check-the-difference-in-seconds-between-two-dates
            #^Used this for the total_seconds() method
            if time.total_seconds() < 0.1:
                diff = 'less than a tenth of a second'
            else:
                #for rounding, so we don't get spurious precision, I used this as a reference:
                #https://www.w3schools.com/python/ref_func_round.asp
                diff = 'approximately ' + str(round(time.total_seconds(), 1)) + ' seconds'
            print('Time it took to complete was: ' + diff)
            print('Max queue size was: ' + str(max_queue) + ' nodes')
            print("Success\n")
            return
            # return node
        # if NUM_NODES != 0:
        print('State to expand has a g(n) of ' + str(node.depth) + ', an h(n) of ' + str(node.hn) + '.\n And it looks like: \n')
        # print(str(node.problem))  # UN-comment this out if you want to print out a higher order puzzle
        #only for 8 puzzle
        if PUZZLE_TYPE == EIGHT:
            drawBoardEight(node.problem)
        elif PUZZLE_TYPE == FIFTEEN:
            drawBoardFift(node.problem)
        elif PUZZLE_TYPE == TFOUR:
            drawBoardTf(node.problem) #!!!!
        expanded = expand(node, visited, qfunct)
        

        # essentially, what this does is it checks all the possible operators that were returned from the expanded() function
        # calculates the heuristic for each child nodes problem
        # then adds them into the queue, as well as the visited array, so that way we can keep track of them
        # update other neccessary values
        for childnode in expanded:
            if childnode.problem not in visited: #had to add this check because I was getting some incorrect depth value for some test cases
                queue += 1
                hn = 0
                if qfunct == 2:
                    hn = misplaced(childnode.problem)
                if qfunct == 3:
                    hn = manhattan(childnode.problem)
                childnode.depth = node.depth + 1
                childnode.hn = hn
                nodes.append(childnode)
                visited.append(childnode.problem)
                NUM_NODES += 1
        # else:
        #     expanded.pop(childnode)
        #update max if we need to
        if queue > max_queue:
            max_queue = queue
        queue += 1
        max_queue = len(nodes)

def expand(node, visited, qfunct):
    # global NUM_NODES
    children = []
    [x, y] = find_zero(node.problem)
    #only operators are moving the 0 up, down, left right
    hn = 0
    if qfunct == 2:
        hn = misplaced(node.problem)
    if (qfunct == 3):
        hn = manhattan(node.problem)
    
    if x > 0: #not on top row, so we can move it up
        #https://realpython.com/copying-python-objects/
        #we need to deep copy so that way when we edit move_up, we do not change node.problem or node at all
        move_up = copy.deepcopy(node.problem)
        temp = move_up[x][y] #save the original value
        move_up[x][y] = move_up[x - 1][y] #decrement x value by 1 to signal that the space moved up
        move_up[x - 1][y] = temp #swap the values
        move_up_node = Node(move_up)
        move_up_node.hn = hn
        move_up_node.depth += 1
        if move_up_node.problem not in visited:
            children.append(move_up_node)
    if x < len(node.problem) - 1: #not on bottom row, so we can move it down
        move_down = copy.deepcopy(node.problem)
        temp = move_down[x][y]
        move_down[x][y] = move_down[x+1][y]
        move_down[x+1][y] = temp
        move_down_node = Node(move_down)
        move_down_node.hn = hn
        move_down_node.depth += 1
        if move_down_node.problem not in visited:
            children.append(move_down_node)
    if y > 0:
        move_left = copy.deepcopy(node.problem)
        temp = move_left[x][y]
        move_left[x][y] = move_left[x][y-1]
        move_left[x][y-1] = temp
        move_left_node = Node(move_left)
        move_left_node.hn = hn
        move_left_node.depth += 1
        if move_left_node.problem not in visited:
            children.append(move_left_node)
    if y < len(node.problem) - 1:
        move_right = copy.deepcopy(node.problem)
        temp = move_right[x][y]
        move_right[x][y] = move_right[x][y+1]
        move_right[x][y+1] = temp
        move_right_node = Node(move_right)
        move_right_node.hn = hn
        move_right_node.depth += 1
        if move_right_node.problem not in visited:
            children.append(move_right_node)

    # if len(children) != 0:
    #     NUM_NODES += 1
    # NUM_NODES += len(children)
    return children


def find_zero(problem):
    for i in range(len(problem)):
        for j in range(len(problem)):
            if problem[i][j] == 0:
                x = i
                y = j
    return [x, y]

def make_node(problem):
    return Node(problem)

def make_queue(node):
    pq = []
    pq.append(node)
    return pq

def remove_front(pq):
    x = pq.pop(0)
    return x

def manhattan(problem):
    global PUZZLE_TYPE
    goalstate = PUZZLE_TYPE #choose your goal state from the global variables
    manhattandist = 0
    x = 0
    y = 0
    goal_x = 0
    goal_y = 0

    #took inspiration from: https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/
    #calculating current position for each value, then retrieving goal state's value
    #using the formula from the link, adds the abs value of actual - expected for each x and y coordinate
    #re sums that into the manhattan distance calculation
    if PUZZLE_TYPE == EIGHT:
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
    elif PUZZLE_TYPE == FIFTEEN:
        for a in range(1, 16): #have to change this range if you change the type of puzzle. For 15 puzzle, would have to be 1 to 16, for 24 puzzle, would have to be 1 to 25, etc
            for i in range(len(problem)):
                for j in range(len(problem)):
                    if problem[i][j] == a:
                        x = i
                        y = j
                    if goalstate[i][j] == a:
                        goal_x = i
                        goal_y = j

            manhattandist = manhattandist + abs(x - goal_x) + abs(y - goal_y)
    elif PUZZLE_TYPE == TFOUR:
        for a in range(1, 25): #have to change this range if you change the type of puzzle. For 15 puzzle, would have to be 1 to 16, for 24 puzzle, would have to be 1 to 25, etc
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
    global PUZZLE_TYPE
    goalstate = PUZZLE_TYPE #choose your goal state from the global variables
    num_misplaced = 0

    for i in range(len(problem)):
        for j in range(len(problem)):
            if problem[i][j] != goalstate[i][j] and problem[i][j] != 0: #realized you have to exclude 0, because it will never be in the "incorrect", it is not even a tile
                num_misplaced = num_misplaced + 1
    return num_misplaced

#https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
def isSolvable(problem):
    inv_count = getInversions([i for row in problem for i in row])
    if inv_count % 2 == 0:
        return True
    else:
        return False

def getInversions(row): 
    #only for 8 puzzle
    count = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if row[j] != 0 and row[i] != 0 and row[i] > row[j]:
                count += 1
    return count

#https://www.quora.com/What-are-some-heuristics-to-solve-8-puzzle-problem-other-than-number-of-titles-out-of-place-and-Manhattan-distances
# def linearconflict(problem):
#     pass

# def countlinearconflict(problem_row, solved_row):
#     counts = [0 for x in range(size)]
#     for i, tile_1 in enumerate(problem_row):
#         if tile_1 in solved_row and tile_1 != 0:
#             solved_i = solved_row.index(tile_1)
#             for j, tile_2 in enumerate(problem_row):
#                 if tile_2 in solved_row and tile_2 != 0 and i != j:
#                     solved_j = solved_row.index(tile_2)
#                     if solved_i > solved_j and i < j:
#                         counts[i] += 1
#                     if solved_i < solved_j and i > j:
#                         counts[i] += 1
#     if max(counts) == 0:
#         return ans * 2
#     else:
#         i = counts.index(max(counts))
#         candidate_row[i] = -1
#         ans += 1
#         return count_conflicts(candidate_row, solved_row, size, ans)


def indices(val, goalstate):
    for i in range(len(goalstate)):
        for j in range(len(goalstate)):
            if goalstate[i][j] == val:
                return [i, j]
    return [-1, -1]

def goal_test(node):
    global PUZZLE_TYPE
    goalstate = PUZZLE_TYPE #change this depending on what type of puzzle you have
    # for row in range(len(node.problem)):
    #     if collections.Counter(node.problem[row]) != collections.Counter(goalstate[row]):
    #         return False
    # return True
    if node.problem == goalstate:
        return True
    else:
        return False

    
class Node:
    def __init__ (self, problem):
        self.hn = 0
        self.depth = 0
        self.problem = problem



def printMenuEight():
    global INVALID_EIGHT
    problem = INVALID_EIGHT
    while isSolvable(problem) == False:
        print("------------------------------------------------------------\n")
        print("Enter your puzzle, using a zero to represent the blank.\n")
        print("Please only enter valid 8-puzzles.\n")
        print("Enter the puzzle demilimiting the numbers with a space. (0 indicates the blank space)\n")
        print("Type RETURN only when finished with the row.\n")
        print("------------------------------------------------------------\n")

        print("Enter the First Row:")
        firstRow = input()
        print("Enter the Second Row:")
        secondRow = input()
        print("Enter the Third Row:")
        thirdRow = input()
        list(firstRow)
        list(secondRow)
        list(thirdRow)
        #https://stackoverflow.com/questions/2186656/how-can-i-remove-all-instances-of-an-element-from-a-list-in-python
        firstRow = [x for x in firstRow if x != ' ']
        secondRow = [x for x in secondRow if x != ' ']
        thirdRow = [x for x in thirdRow if x != ' ']
        #not sure why I even looked it up, but I did reference it, so I'm going to put it in just in case lol
        #https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
        for i in range(len(firstRow)):
            firstRow[i] = int(firstRow[i])
            secondRow[i] = int(secondRow[i])
            thirdRow[i] = int(thirdRow[i])
        # print(len(firstRow))
        problem = [firstRow, secondRow, thirdRow]
        if isSolvable(problem) == 0:
            print('Please enter a valid 8 puzzle!!!\n')
    return problem

def printMenuFift():
    print("------------------------------------------------------------\n")
    print("Enter your puzzle, using a zero to represent the blank.\n")
    print("Please only enter valid 15-puzzles.\n")
    print("Enter the puzzle demilimiting the numbers with a space. (0 indicates the blank space)\n")
    print("Type RETURN only when finished with the row.\n")
    print("------------------------------------------------------------\n")

    print("Enter the First Row:")
    firstRow = input()
    print("Enter the Second Row:")
    secondRow = input()
    print("Enter the Third Row:")
    thirdRow = input()
    print("Enter the Fourth Row:")
    fourthRow = input()
    list(firstRow)
    list(secondRow)
    list(thirdRow)
    list(fourthRow)
    #https://stackoverflow.com/questions/2186656/how-can-i-remove-all-instances-of-an-element-from-a-list-in-python
    firstRow = [x for x in firstRow if x != ' ']
    secondRow = [x for x in secondRow if x != ' ']
    thirdRow = [x for x in thirdRow if x != ' ']
    fourthRow = [x for x in fourthRow if x != ' ']
    #not sure why I even looked it up, but I did reference it, so I'm going to put it in just in case lol
    #https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
    for i in range(len(firstRow)):
        firstRow[i] = int(firstRow[i])
        secondRow[i] = int(secondRow[i])
        thirdRow[i] = int(thirdRow[i])
        fourthRow[i] = int(fourthRow[i])
    # print(len(firstRow))
    problem = [firstRow, secondRow, thirdRow, fourthRow]
    return problem


def printMenuTf():
    print("------------------------------------------------------------\n")
    print("Enter your puzzle, using a zero to represent the blank.\n")
    print("Please only enter valid 24-puzzles.\n")
    print("Enter the puzzle demilimiting the numbers with a space. (0 indicates the blank space)\n")
    print("Type RETURN only when finished with the row.\n")
    print("------------------------------------------------------------\n")

    print("Enter the First Row:")
    firstRow = input()
    print("Enter the Second Row:")
    secondRow = input()
    print("Enter the Third Row:")
    thirdRow = input()
    print("Enter the Fourth Row:")
    fourthRow = input()
    print("Enter the Fifth Row:")
    fifthRow = input()
    list(firstRow)
    list(secondRow)
    list(thirdRow)
    list(fourthRow)
    list(fifthRow)
    #https://stackoverflow.com/questions/2186656/how-can-i-remove-all-instances-of-an-element-from-a-list-in-python
    firstRow = [x for x in firstRow if x != ' ']
    secondRow = [x for x in secondRow if x != ' ']
    thirdRow = [x for x in thirdRow if x != ' ']
    fourthRow = [x for x in fourthRow if x != ' ']
    fifthRow = [x for x in fifthRow if x != ' ']
    #not sure why I even looked it up, but I did reference it, so I'm going to put it in just in case lol
    #https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
    for i in range(len(firstRow)):
        firstRow[i] = int(firstRow[i])
        secondRow[i] = int(secondRow[i])
        thirdRow[i] = int(thirdRow[i])
        fourthRow[i] = int(fourthRow[i])
        fifthRow[i] = int(fifthRow[i])
    # print(len(firstRow))
    problem = [firstRow, secondRow, thirdRow, fourthRow, fifthRow]
    return problem



#Just something to make it look nicer :)
#ONLY FOR 8 PUZZLE BECAUSE IT'S A LITTLE HARD TO DO THIS FOR BIGGER ORDER PUZZLES
#I coded something similar to this when i did a personal project for a tic tac toe program
#thought it would look pretty cool here as well
#here's the link to my code just in case: https://github.com/bshah016/CS_Projects/blob/master/TTT.py
def drawBoardEight(problem):
    board_status = []
    for i in range(len(problem)):
        for j in range(len(problem)):
            if problem[i][j] == 0:
                board_status.append(' ')
            else:
                board_status.append(problem[i][j])
    print('\
 ???????????????????????????????????????\n\
 ??? {0} ??? {1} ??? {2} ???\n\
 ???????????????????????????????????????\n\
 ??? {3} ??? {4} ??? {5} ???\n\
 ???????????????????????????????????????\n\
 ??? {6} ??? {7} ??? {8} ???\n\
 ??????????????????????????????????????? '.format(
               board_status[0], board_status[1], board_status[2], 
               board_status[3], board_status[4], board_status[5], 
               board_status[6], board_status[7], board_status[8]))

def drawBoardFift(problem):
    board_status = []
    for i in range(len(problem)):
        for j in range(len(problem)):
            if problem[i][j] == 0:
                board_status.append('  ')
            else:
                if problem[i][j] < 10:
                    board_status.append(str(problem[i][j]) + ' ')
                else:
                    board_status.append(problem[i][j])
    print('\
 ???????????????????????????????????????????????????????????????\t\n\
 ??? {0} ??? {1} ??? {2} ??? {3} ???\t\n\
 ???????????????????????????????????????????????????????????????\t\n\
 ??? {4} ??? {5} ??? {6} ??? {7} ???\t\n\
 ???????????????????????????????????????????????????????????????\t\n\
 ??? {8} ??? {9} ??? {10} ??? {11} ???\t\n\
 ???????????????????????????????????????????????????????????????\t\n\
 ??? {12} ??? {13} ??? {14} ??? {15} ???\t\n\
 ??????????????????????????????????????????????????????????????? \t'.format(
               board_status[0], board_status[1], board_status[2], board_status[3],
               board_status[4], board_status[5], board_status[6], board_status[7],
               board_status[8], board_status[9], board_status[10], board_status[11],
               board_status[12], board_status[13], board_status[14], board_status[15]))


def drawBoardTf(problem):
    board_status = []
    for i in range(len(problem)):
        for j in range(len(problem)):
            if problem[i][j] == 0:
                board_status.append('  ')
            else:
                if problem[i][j] < 10:
                    board_status.append(str(problem[i][j]) + ' ')
                else:
                    board_status.append(problem[i][j])
    print('\
 ??????????????????????????????????????????????????????????????????????????????\t\n\
 ??? {0} ??? {1} ??? {2} ??? {3} ??? {4} ???\t\n\
 ??????????????????????????????????????????????????????????????????????????????\t\n\
 ??? {5} ??? {6} ??? {7} ??? {8} ??? {9} ???\t\n\
 ??????????????????????????????????????????????????????????????????????????????\t\n\
 ??? {10} ??? {11} ??? {12} ??? {13} ??? {14} ???\t\n\
 ??????????????????????????????????????????????????????????????????????????????\t\n\
 ??? {15} ??? {16} ??? {17} ??? {18} ??? {19} ???\t\n\
 ??????????????????????????????????????????????????????????????????????????????\t\n\
 ??? {20} ??? {21} ??? {22} ??? {23} ??? {24} ???\t\n\
 ?????????????????????????????????????????????????????????????????????????????? \t'.format(
               board_status[0], board_status[1], board_status[2], board_status[3], board_status[4],
               board_status[5], board_status[6], board_status[7], board_status[8], board_status[9],
               board_status[10], board_status[11], board_status[12], board_status[13], board_status[14],
               board_status[15], board_status[16], board_status[17], board_status[18], board_status[19],
               board_status[20], board_status[21], board_status[22], board_status[23], board_status[24],))



main()
