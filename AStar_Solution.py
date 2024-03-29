# Lab 05
# A* Search Graph Implementation
# By: Daniel Thai and Travis Chamness
# Date: 09/22/21

import sys

#Stores the Maze
maze = []
#Holds starting position and will be first node on fringe
startNode = None
#Goal node holds goal position, only representative
goalNode = None
#Data structure that holds potential nodes for expansion
fringe = []
#Data structure that holds nodes which have already been visited
visited = []
#Upon reaching goal Path is populated with the path taken
path = []
#The cost of the path taken stored as an integer
pathCost = None
#Stolen from Lab 4 - Credit to Daniel Ramirez
#The pattern of movements: Up, Down, Left, then Right
ULDR  = [[-1,0],[0,-1],[1,0],[0,1]]
#The node currently being expanded
currentNode = None
#Selection of Graph or Tree implementation
SELECTION = 0
#Literal R representing Robot in Initial Maze
ROBOT = 'R'
#Literal D representing Diamond in Initial Maze
DIAMOND = 'D'

class node:
    def __init__(self,parent,data,cost,children, forwardCost, move):
        self.parent = parent # Points to the parent node in the state chart
        self.data = data # Represents the [Row][Col] position of the node
        self.cost = cost # The cost as determined by the cumulative cost of the path taken to this tile on the maze
        self.forwardCost = forwardCost # The cost determined by the heuristic function
        self.children = [] # The children states of this  node
        self.move = move # The move to get from the previous node to this node

def create_map():
    # map_name = input("Enter map name(try \"mazeMap.txt\"): ")
    map_name = "labGivenMaze.txt"
    # map_name = "maze1.txt"
    file = open(map_name, "r")

    maze = []
    line = []
    while 1:
        char = file.read(1)
        if not char:
            break
        elif char == '1':
            line.append(1)
        elif char == '3':
            line.append(3)
        elif char == '6':
            line.append(6)
        elif char == ROBOT:
            line.append(ROBOT)
        elif char == DIAMOND:
            line.append(DIAMOND)
        elif char == '-':
            line.append('-')
        elif char == '\n':
            maze.append(line)
            line = []
    if line:
        maze.append(line)
    file.close()
    return maze


def initialization():
    global maze
    global startNode
    global goalNode
    global fringe

    maze = create_map() #Builds maps for us via txt file
    find_goal_start = True
    startNode, goalNode = print_maze_id_start_goal(find_goal_start)
    # Grab the future cost for the start node
    startNode = heuristic_function(startNode)
    fringe = [startNode]

# "Print maze and ID the Start and Goal"
# Allows user to print a maze, and on request of a Boolean True find_goal_start parameter, return the start and goal nodes.
def print_maze_id_start_goal(find_goal_start = False):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == ROBOT:
                startNode = node(None,[i,j],0,None, None, None)
            elif val == DIAMOND:
                goalNode = node(None, [i,j], 0, None, 0, None)
            print(val, end=' ')
        print()
    if find_goal_start:
        return startNode, goalNode #returns the goal and start node if requested by user via parameter
    else:
        return ""  #effectively return nothing

# Determine lowest cost node available in fringe and return current node, if no smaller node exists, or the new smallest node.
def lowestCostNode():
    global fringe
    global currentNode

    nodeIndex = None
    maxCost = sys.maxsize 
    smallestCostNode = node(None, None, 0, None, maxCost, None)
    for index,iterNode in enumerate(fringe):
        # F(n) = G(n) + H(n) : A* algorithm - if f(n) of iternode < f(n) for current smallest cost node
        if (iterNode.forwardCost + iterNode.cost) < (smallestCostNode.forwardCost + smallestCostNode.cost): 
            #update the smallest node to the iterNode
            smallestCostNode = iterNode
            #Store the index for removal from fringe
            nodeIndex = index

    if(smallestCostNode.forwardCost == maxCost):
        #All nodes left have been visited
        return currentNode
    else:
        #Pop the node ID'd in the f(n) comparison for loop from fringe and return it
        fringe.pop(nodeIndex)
        return smallestCostNode

def goalTest():
    global goalNode
    global currentNode
    if currentNode.data == goalNode.data:
        return True
    else:
        return False

def successor_function():
    #this will go inside the while loop in main()
    global currentNode
    global fringe
    global ULDR
    global visited

    for direction, moves in enumerate(ULDR):
        #If the move doesn't result in being on a wall
        if maze[currentNode.data[0]+moves[0]][currentNode.data[1] + moves[1]] != '-':
            child = node(currentNode, [currentNode.data[0]+moves[0],currentNode.data[1] + moves[1]], None, None, None, None)
            if direction == 0:
                child.move = 'U'
            elif direction == 1:
                child.move = 'L'
            elif direction == 2:
                child.move = 'D'
            elif direction == 3:
                child.move = 'R'
            else:
                print("Invalid Direction")
            #Heuristic function call added to child creation process
            child = heuristic_function(child)
            # Robot and Diamond both account for 0 cost, but must be handled respecitively as 0 cost
            if maze[child.data[0]][child.data[1]] != 'R' and maze[child.data[0]][child.data[1]] != 'D':
                child.cost = currentNode.cost + maze[child.data[0]][child.data[1]]
            else:
                #Else the most is Diamond or Robot and incur 0 cost to child
                child.cost = currentNode.cost
            currentNode.children.append(child)
            fringe.append(child)
    #after finding all children of currentNode, place it in visited if Graph Implementation Selected
    if SELECTION == 1:
        visited.append(currentNode)

def in_visited():
    global visited
    global currentNode

    in_visited = False
    for node in visited:
        if currentNode.data == node.data:
            in_visited = True
        if in_visited:
            break
    return in_visited

# No Change from UCS implementation
def populate_path():
    global currentNode
    global pathCost
    global path

    pathCost = currentNode.cost
    while currentNode != None:
        if currentNode.move != None:
            path.insert(0,currentNode.move)
        currentNode = currentNode.parent

# Heuristic Function:
# Calculates manhattan distance from a node to the goal node.
def heuristic_function(node):
    global goalNode
    # F(n) = G(n) + H(n) : A* algorithm
    node.forwardCost = abs(goalNode.data[0] - node.data[0]) + abs(goalNode.data[1] - node.data[1])
    return node

def a_star_solution():
    global currentNode
    global fringe
    global currentNode
    global path
    initialization()
    while fringe:
        currentNode = lowestCostNode()
        goalFound = goalTest()
        if not goalFound:
            if SELECTION == 1 and not in_visited(): 
                successor_function()    
            elif SELECTION == 2:
                successor_function()
        elif goalFound:
            populate_path()
            break
    print(path)
    print("Cost of Plan:",pathCost)
    return path, pathCost

def solution_host():
    global SELECTION

    while SELECTION != 1 and SELECTION != 2:
        SELECTION = int(input("Seletion Menu for A* Implementation \nSelect either 1 or 2 for corresponding implementations \n1: GRAPH Implementation \n2: Tree Implementation\n"))
    a_star_solution()

    
solution_host()