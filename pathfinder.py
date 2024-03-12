import sys
from collections import deque
with open(sys.argv[1], "r") as file:
    firstline = file.readline().split()
    Rows = int(firstline[0])
    Columns = int(firstline[1])
    
    secondline = file.readline().split()
    startx = int(secondline[0])-1
    starty = int(secondline[1])-1
    thirdline = file.readline().split()
    endx = int(thirdline[0])-1
    endy = int(thirdline[1])-1

    map = [list(map(str,file.readline().split())) for row in range(Rows)]

class Node:
    def __init__(self, x, y):
         self.x = x
         self.y = y
         self.parent = None
         self.height = 0
         self.rock = False
         
def bfs(problem):
    node_queue = deque()
    start_node = Node(startx, starty)
    node_queue.append(start_node)
  
    move_count = 0
    moves = [[-1,0], [1,0], [0,-1],[0,1]]
    visited = [[False] * Rows for i in range (Columns)]
    visited[start_node.x][start_node.y] = True
    deeper_nodes = 0
    atdepth_nodes =1
    found_end = False
    while len(node_queue):
        currentnode = node_queue.popleft()
        x, y = currentnode.x, currentnode.y
        if x == endx and y == endy:
            found_end=True
            break
        for dx, dy in moves:
            newx = x + dx
            newy = y + dy
            if newx >= 0 and newx < Columns and newy >= 0 and newy < Rows and not visited[newx][newy] and problem[newx][newy] != 'X':
                new_node = Node(newx, newy)
                new_node.parent = currentnode
                node_queue.append(new_node)
                visited[newx][newy]= True
                deeper_nodes+=1
        atdepth_nodes-=1
        if atdepth_nodes == 0:
            atdepth_nodes = deeper_nodes
            
            deeper_nodes =0
            move_count +=1
    if found_end:
        problem[currentnode.x][currentnode.y] = '*'
        currentnode = currentnode.parent
        while currentnode:
            problem[currentnode.x][currentnode.y] = '*'
            currentnode = currentnode.parent
        return problem
    return -1


algorithm = sys.argv[2]
if(algorithm == "bfs"):
    bfs_solve = bfs(map)
    for row in bfs_solve:
        print(' '.join(row))



    
        

