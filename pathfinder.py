import sys
from collections import deque
from queue import PriorityQueue
with open(sys.argv[1], "r") as file:
    firstline = file.readline().split()
    Rows = int(firstline[0])
    Columns = int(firstline[1])
    
    secondline = file.readline().split()
    starty = int(secondline[0])-1
    startx = int(secondline[1])-1
    thirdline = file.readline().split()
    endy = int(thirdline[0])-1
    endx = int(thirdline[1])-1

    map = [list(map(str,file.readline().split())) for row in range(Rows)]

class Node:
    def __init__(self, x, y):
         self.x = x
         self.y = y
         self.parent = None
         self.height = 0
         self.rock = False
    def pos(self):
        return (self.x, self.y)


moves = [[-1,0], [1,0], [0,-1], [0,1]]
def print_problem(problem, currentnode):
    problem[currentnode.y][currentnode.x] = '*'
    currentnode = currentnode.parent
    while currentnode:
        problem[currentnode.y][currentnode.x] = '*'
        currentnode = currentnode.parent
    for row in problem:
        print(' '.join(row))

def bfs(problem):
    node_queue = deque()
    start_node = Node(startx, starty)
    node_queue.append(start_node)
    visited = [[False] * Columns for i in range (Rows)]
    visited[start_node.y][start_node.x] = True
    deeper_nodes = 0
    atdepth_nodes =1
    found_end = False
    while len(node_queue):
        currentnode = node_queue.popleft()
        x, y = currentnode.x, currentnode.y
        if x == endx and y == endy:
            found_end=True
            break
        for dy, dx in moves:
            newx = x + dx
            newy = y + dy
            if newx >= 0 and newx < Columns and newy >= 0 and newy < Rows and not visited[newy][newx] and problem[newy][newx] != 'X':
                new_node = Node(newx, newy)
                new_node.parent = currentnode
                node_queue.append(new_node)
                visited[newy][newx]= True
                deeper_nodes+=1
        atdepth_nodes-=1
        if atdepth_nodes == 0:
            atdepth_nodes = deeper_nodes
            
            deeper_nodes =0
        
    if found_end:
        print_problem(problem, currentnode)
    else:
        print("null")
        return -1

def cost(Node1, Node2):
    diff = Node2.height - Node1.height
    if diff > 0:
        return (1 + diff)
    else:
        return 1


def ucs(problem):
    node_queue = PriorityQueue()
    start_node = Node(startx, starty)
    counter =0
    start_node.height = int(problem[starty][startx])
    node_queue.put((0, counter, start_node))
    counter += 1
    visited = [[False] * Columns for i in range (Rows)]
    visited[start_node.y][start_node.x] = True
    found_end = False
    while not node_queue.empty():
        currentcost, _, currentnode = node_queue.get()
        x, y = currentnode.x, currentnode.y
        visited[y][x]=True
        if x == endx and y == endy:
            found_end=True
            break
        for dy, dx in moves:
            newx = x + dx
            newy = y + dy
            if newx >= 0 and newx < Columns and newy >= 0 and newy < Rows and problem[newy][newx] != 'X' and not visited[newy][newx]:
                new_node = Node(newx, newy)
                new_node.parent = currentnode
                new_node.height = int(problem[newy][newx])
                new_cost = currentcost + cost(currentnode, new_node)
                node_queue.put((new_cost, counter, new_node))
                counter+=1
            
                
        
    if found_end:
        print_problem(problem, currentnode)
    else:
        print("null")
        return -1

def manhattan(current_pos, end_pos):
    x_dist = abs(end_pos[0]-current_pos[0])
    y_dist = abs(end_pos[1]-current_pos[1])
    return (x_dist + y_dist)


def euclidean(current_pos, end_pos):
    a = abs(end_pos[0]-current_pos[0])
    b = abs(end_pos[1]-current_pos[1])
    c = ((a**2)+(b**2))**0.5
    return c

def astar(problem):
    node_queue = PriorityQueue()
    start_node = Node(startx, starty)
    counter =0
    start_node.height = int(problem[starty][startx])
    if sys.argv[3] == "euclidean":
        heuristic_cost = euclidean((startx, starty), (endx, endy)) 
    elif sys.argv[3] == "manhattan":
        heuristic_cost = manhattan((startx, starty), (endx, endy))
    node_queue.put((0, heuristic_cost, counter, start_node))
    counter += 1
    visited = [[False] * Columns for i in range (Rows)]
    visited[start_node.y][start_node.x] = True
    found_end = False
    while not node_queue.empty():
        currentcost, _,  _, currentnode = node_queue.get()
        x, y = currentnode.x, currentnode.y
        visited[y][x]= True
        if x == endx and y == endy:
            found_end=True
            break
        for dy, dx in moves:
            newx = x + dx
            newy = y + dy
            if newx >= 0 and newx < Columns and newy >= 0 and newy < Rows and problem[newy][newx] != 'X' and not visited[newy][newx]:
                new_node = Node(newx, newy)
                new_node.parent = currentnode
                new_node.height = int(problem[newy][newx])
                g = currentcost + cost(currentnode, new_node)
                if sys.argv[3] == "euclidean":
                    h = euclidean((newx, newy), (endx, endy)) 
                elif sys.argv[3] == "manhattan":
                    h = manhattan((newx, newy), (endx, endy))
                f = g + h
                node_queue.put((g, f, counter, new_node))
                counter+=1
    if found_end:
        print_problem(problem, currentnode)
    else:
        print("null")
        return -1


algorithm = sys.argv[2]
if(algorithm == "bfs"):
    bfs(map)
elif algorithm == "ucs":
    ucs(map)
elif algorithm == "astar":
    astar(map)


    
        

