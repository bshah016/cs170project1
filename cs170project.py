
#define your solution states here
import queue
import copy
from shutil import move


EIGHT = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
FIFTEEN = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
FIFTEEN = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]]
NUM_NODES = 0


def main():
    choice = 5
    problem = []
    while choice != 0:
        print("Welcome to my 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own, or 0 to quit")
        choice = int( input() )
        if choice == 1:
            problem = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
            choice = 0
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
            choice = 0
        else:
            print("Please enter a valid choice")

    # print(problem)
    algNum = input(print("Select algorithm. (1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhattan Distance Heuristic"))
    qfunct = int( algNum )
    print(generalsearch(problem, qfunct))

def generalsearch(problem, qfunct):
    global NUM_NODES
    NUM_NODES = 0
    hn = 0

    makenode = make_node(problem)
    nodes = make_queue(makenode)
    visited = make_queue(makenode)
    nodenum = 0
    while True:
        #this was a problem for the NUM_NODES, used this link to help me out with sorting the vector:
        #to show that i didn't just copy it, I'll explain it here:
        #when you zip the two lists, they get merged into a list of tuples. 
        #so for example, {1, 2, 3} and {'a', 'b', 'c'} zipped would become {{1, a}, {2, b}, {3, c}}
        #then, it creates a new resulting array based on the zipped array
        #this new array that is stored, is then separated and then now the nodes array is stored properly.
        #https://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        if qfunct != 1:
            weights = []
            for newnode in nodes:
                weight = newnode.depth + newnode.hn
                weights.append(weight)
            nodes = [x for _, x in sorted(zip(weights, nodes), key=lambda pair: pair[0])]

        if len(nodes) == 0:
            return "failure"
        nodenum += 1
        node = nodes.pop(0)
        if goal(node):
            print('Total number of nodes expanded: ' + str(NUM_NODES))
            print('Depth of the node in the tree was: ' + str(node.depth))
            return "Success"
            # return node
        if NUM_NODES != 0:
            print('State to expand has a g(n) of ' + str(node.depth) + ', an h(n) of ' + str(node.hn) + '.\n And it looks like: \n' + str(node.problem))
        expanded = expand(node, visited, qfunct)
        
        for childnode in expanded:
            if qfunct == 2:
                hn = misplaced(childnode.problem)
            if (qfunct == 3):
                hn = manhattan(childnode.problem)
            childnode.depth = node.depth + 1
            childnode.hn = hn
            node.expanded += 1
            nodes.append(childnode)
            visited.append(childnode.problem)
            NUM_NODES += 1
        # else:
        #     expanded.pop(childnode)

def expand(node, visited, qfunct):
    global NUM_NODES
    children = []
    x = 0
    y = 0
    for i in range(len(node.problem)):
        for j in range(len(node.problem)):
            if int(node.problem[i][j]) == 0:
                x = i
                y = j
    #only operators are moving the 0 up, down, left right
    hn = 0
    if qfunct == 2:
        hn = misplaced(node.problem)
    if (qfunct == 3):
        hn = manhattan(node.problem)
    
    if x > 0: #not on top row, so we can move it up
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
    global EIGHT
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
    global EIGHT
    goalstate = EIGHT #choose your goal state from the global variables
    num_misplaced = 0

    for i in range(len(problem)):
        for j in range(len(problem)):
            if int(problem[i][j]) != int(goalstate[i][j]) and int(problem[i][j]) != 0:
                num_misplaced = num_misplaced + 1
    return num_misplaced

def uniform(problem):
    return 0
    

def goal(node):
    global EIGHT
    goalstate = EIGHT #change this depending on what type of puzzle you have
    if node.problem == goalstate:
        return True
    else:
        return False

    
class Node:
    def __init__ (self, problem):
        self.hn = 0
        self.depth = 0
        self.problem = problem
        self.flag = False
        self.expanded = 0



main()


    
