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
         self.path_cost=0
    def __lt__(self, other):
        return self.path_cost < other.path_cost
    def pos(self):
        return (self.x, self.y)


moves = [[-1,0], [1,0], [0,-1], [0,1]]

def bfs(problem):
    node_queue = deque()
    start_node = Node(startx, starty)
    node_queue.append(start_node)
    visited = [[False] * Rows for i in range (Columns)]
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
            if newx >= 0 and newx < Columns and newy >= 0 and newy < Rows and not visited[newx][newy] and problem[newx][newy] != 'X':
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
        problem[currentnode.y][currentnode.x] = '*'
        currentnode = currentnode.parent
        while currentnode:
            problem[currentnode.y][currentnode.x] = '*'
            currentnode = currentnode.parent
        return problem
    return -1

def cost(Node1, Node2):
    if Node1.height - Node2.height > 0:
        return 1 + Node1.height - Node2.height
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
                new_node.path_cost = currentcost + cost(currentnode, new_node)
                node_queue.put((new_node.path_cost, counter, new_node))
                counter+=1
            
                
        
    if found_end:
        problem[currentnode.y][currentnode.x] = '*'
        currentnode = currentnode.parent
        while currentnode:
            problem[currentnode.y][currentnode.x] = '*'
            currentnode = currentnode.parent
        return problem
    return -1

def manhattan(current_pos, end_pos):
    return ((abs(end_pos[0]-current_pos[0]))+ (abs(end_pos[1]-current_pos[1])))


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
    node_queue.put((0, counter, start_node))
    counter += 1
    visited = [[False] * Columns for i in range (Rows)]
    visited[start_node.y][start_node.x] = True
    found_end = False
    while not node_queue.empty():
        next = node_queue.get()
        currentcost, _, currentnode = next
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
                if sys.argv[3] == "euclidean":
                    new_cost = currentcost + cost(currentnode, new_node)
                    heuristic_cost = euclidean((newx, newy), (endx, endy)) 
                    total_cost = new_cost + heuristic_cost
                    node_queue.put((total_cost, counter, new_node))
                elif sys.argv[3] == "manhattan":
                    new_cost = currentcost + cost(currentnode, new_node)
                    heuristic_cost = manhattan((newx, newy), (endx, endy))
                    total_cost = new_cost + heuristic_cost
                    node_queue.put((total_cost, counter, new_node))
                counter+=1
            
                
        
    if found_end:
        problem[currentnode.y][currentnode.x] = '*'
        currentnode = currentnode.parent
        while currentnode:
            problem[currentnode.y][currentnode.x] = '*'
            currentnode = currentnode.parent
        return problem
    return -1


algorithm = sys.argv[2]
if(algorithm == "bfs"):
    bfs_solve = bfs(map)
    for row in bfs_solve:
        print(' '.join(row))
elif algorithm == "ucs":
    ucs_solve = ucs(map)
    for row in ucs_solve:
        print(" ".join(row))
elif algorithm == "astar":
    astar_solve = astar(map)
    for row in astar_solve:
        print(" ".join(row))



    
        

